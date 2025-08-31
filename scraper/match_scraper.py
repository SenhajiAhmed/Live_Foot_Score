from playwright.sync_api import sync_playwright
import json

class MatchScraper:
    def __init__(self, url="https://www.sofascore.com/football//2025-07-14", output_path="data/events.json"):
        self.url = url
        self.output_path = output_path

    def _log_response(self, response):
        if "scheduled-events" in response.url and response.status == 200:
            print(f"✅ Found request: {response.url}")
            try:
                json_data = response.json()
                with open(self.output_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                print(f"✅ JSON saved to {self.output_path}")
            except Exception as e:
                print(f"❌ Error reading JSON: {e}")

    def run(self, wait_time=2000):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            page.on("response", self._log_response)
            print("➡️ Opening page...")
            page.goto(self.url)

            print("🕒 Waiting for data to load...")
            page.wait_for_timeout(wait_time)

            browser.close()
            print("🚪 Browser closed.")
