import logging
from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist: str):
    logging.info(f"Received request for artist: {artist}")
    url = f"https://trackid.net/audiostreams?keywords={artist}"
    logging.info(f"Navigating to: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
        except Exception as e:
            logging.error(f"Initial navigation failed: {e}")
            try:
                page.reload(wait_until="domcontentloaded", timeout=10000)
            except Exception as e:
                logging.error(f"Reload failed: {e}")
                browser.close()
                raise Exception("Timed out waiting for results. Check selector or network.")

        try:
            page.wait_for_selector(".audiostream-card a", timeout=20000)
        except Exception as e:
            logging.error("Scraper failed")
            logging.error(e)
            browser.close()
            raise Exception("Timed out waiting for results. Check selector or network.")

        elements = page.query_selector_all(".audiostream-card a")
        results = [el.inner_text().strip() for el in elements]
        browser.close()

        return {"results": results}