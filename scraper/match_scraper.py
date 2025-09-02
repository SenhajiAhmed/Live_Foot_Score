from playwright.sync_api import sync_playwright
import json
import time
import os
from typing import Optional, Dict, Any

class MatchScraper:
    def __init__(self, date: Optional[str] = None, output_path: str = "data/events.json"):
        """Initialize the MatchScraper.
        
        Args:
            date: The date in YYYY-MM-DD format. If None, uses current date.
            output_path: Path to save the scraped data.
        """
        # Ensure output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # If no date is provided, use today's date
        if date is None:
            from datetime import datetime
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Construct the URL with the provided or current date
        self.url = f"https://www.sofascore.com/football/{date}"
        self.output_path = output_path
        self.json_data: Optional[Dict[str, Any]] = None

    def _log_response(self, response) -> None:
        """Handle the response from the server.
        
        Args:
            response: The response object from Playwright.
        """
        if "scheduled-events" in response.url and response.status == 200:
            print(f"✅ Found request: {response.url}")
            try:
                self.json_data = response.json()
                # Ensure the directory exists before writing
                os.makedirs(os.path.dirname(os.path.abspath(self.output_path)), exist_ok=True)
                
                with open(self.output_path, "w", encoding="utf-8") as f:
                    json.dump(self.json_data, f, ensure_ascii=False, indent=4)
                print(f"✅ JSON saved to {self.output_path}")
                self.response_processed = True
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing JSON: {e}")
                self.response_processed = True
            except IOError as e:
                print(f"❌ Error writing to file: {e}")
                self.response_processed = True
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                self.response_processed = True

    def run(self, wait_time: int = 10000) -> bool:
        """Run the scraper to fetch match data.
        
        Args:
            wait_time: Maximum time to wait for the data in milliseconds.
            
        Returns:
            bool: True if data was successfully fetched and saved, False otherwise.
        """
        self.response_processed = False
        self.json_data = None
        
        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context()
                    page = context.new_page()

                    page.on("response", self._log_response)
                    print("➡️ Opening page...")
                    
                    # Navigate to the page
                    page.goto(self.url, wait_until="domcontentloaded")
                    print(f"🌐 Loaded page: {self.url}")

                    # Wait for data to be processed
                    start_time = time.time()
                    while not self.response_processed and (time.time() - start_time) * 1000 < wait_time:
                        page.wait_for_timeout(100)
                    
                    # Clean up
                    context.close()
                    browser.close()
                    print("🚪 Browser closed.")
                    
                    if not self.response_processed:
                        print("⚠️ Timed out waiting for data")
                        return False
                        
                    return self.json_data is not None

                except Exception as e:
                    print(f"❌ Browser error: {e}")
                    return False
                    
        except Exception as e:
            print(f"❌ Playwright error: {e}")
            return False
