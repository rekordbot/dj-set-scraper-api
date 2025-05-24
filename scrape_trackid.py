import logging
from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist: str):
    logging.info(f"Received request for artist: {artist}")
    url = f"https://trackid.net/audiostreams?keywords={artist}"
    logging.info(f"Navigating to: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ))

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=40000)
        except Exception as e:
            logging.error(f"Navigation failed: {e}")
            browser.close()
            raise Exception("Page load timeout")

        # Screenshot for debug
        page.screenshot(path="/tmp/debug.png")

        # Optional: dismiss popup
        try:
            page.locator("button:has-text('Accept')").first.click(timeout=3000)
            logging.info("Accepted cookie modal")
        except:
            pass

        try:
            page.wait_for_selector(".audiostream-card", timeout=30000)
        except Exception as e:
            logging.error("No .audiostream-card found, trying fallback")
            html = page.content()
            browser.close()
            with open("/tmp/fallback_dump.html", "w", encoding="utf-8") as f:
                f.write(html)
            raise Exception("Timed out waiting for results. Check selector or site structure.")

        cards = page.query_selector_all(".audiostream-card")
        results = [c.inner_text().strip() for c in cards if c.inner_text().strip()]

        browser.close()
        return {"results": results}