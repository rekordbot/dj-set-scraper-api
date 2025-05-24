from playwright.sync_api import sync_playwright
import logging

def scrape_trackid_mixes(artist):
    url = f"https://trackid.net/audiostreams?keywords={artist}"
    logging.info(f"Received request for artist: {artist}")
    logging.info(f"Navigating to: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            
            # Dismiss any popup or overlay ad
            try:
                page.locator("div.fc-dialog-container button:has-text('Reject all')").click(timeout=3000)
            except:
                pass  # Ignore if not present
            
            # Now wait for the track titles
            page.wait_for_selector(".audiostream-card a", timeout=20000)
            titles = page.locator(".audiostream-card a").all_text_contents()
            browser.close()
            return {"results": titles}
        except Exception as e:
            browser.close()
            logging.error("Scraper failed", exc_info=True)
            raise Exception("Timed out waiting for results. Check selector or network.")