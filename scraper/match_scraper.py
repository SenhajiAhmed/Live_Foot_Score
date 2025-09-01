from playwright.sync_api import sync_playwright
import json
import time

class MatchScraper:
    def __init__(self, date=None, output_path="data/events.json"):
        # If no date is provided, use today's date
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Construct the URL with the provided or current date
        url = f"https://www.sofascore.com/football//{date}"
        self.url = url
        self.output_path = output_path

    def _log_response(self, response):
        if "scheduled-events" in response.url and response.status == 200:
            print(f"✅ Found request: {response.url}")
            try:
                self.json_data = response.json()
                with open(self.output_path, "w", encoding="utf-8") as f:
                    json.dump(self.json_data, f, ensure_ascii=False, indent=4)
                print(f"✅ JSON saved to {self.output_path}")
                # Set a flag to indicate we've processed the response
                self.response_processed = True
            except Exception as e:
                print(f"❌ Error reading JSON: {e}")
                self.response_processed = True  # Ensure we don't hang on error

    def run(self, wait_time=10000):  # Increased default timeout to 10 seconds
        self.response_processed = False
        self.json_data = None
        
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(headless=True)  # Run in headless mode for stability
                context = browser.new_context()
                page = context.new_page()

                page.on("response", self._log_response)
                print("➡️ Opening page...")
                page.goto(self.url, wait_until="domcontentloaded")

                # Wait for either the response to be processed or the timeout
                start_time = time.time()
                while not self.response_processed and (time.time() - start_time) * 1000 < wait_time:
                    page.wait_for_timeout(100)  # Small delay to prevent busy waiting
                
                # Clean up
                context.close()
                browser.close()
                print("🚪 Browser closed.")
                
                if not self.response_processed:
                    print("⚠️ Timed out waiting for data")
                    return False
                    
                return True

                # If response wasn't processed yet, wait the remaining time
                if not self.response_processed:
                    print("🕒 Waiting for data to load...")
                    page.wait_for_timeout(wait_time - ((time.time() - start_time) * 1000))

            except Exception as e:
                print(f"❌ An error occurred: {e}")
            finally:
                # Ensure browser is always closed
                if hasattr(self, 'browser') and self.browser:
                    try:
                        if self.browser.is_connected():
                            self.browser.close()
                            print("🚪 Browser closed.")
                    except:
                        pass  # Ignore any errors during browser closure
