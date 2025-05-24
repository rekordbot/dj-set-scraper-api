from playwright.sync_api import sync_playwright
import logging

def scrape_trackid_mixes(artist):
    logging.info(f"Received request for artist: {artist}")
    url = f"https://trackid.net/audiostreams?keywords={artist}"
    logging.info(f"Navigating to: {url}")
    results = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            # Correct selector for result cards
            page.wait_for_selector(".audiostream-card a", timeout=20000)

            cards = page.query_selector_all(".audiostream-card")
            for card in cards:
                title_el = card.query_selector("a")
                title = title_el.inner_text().strip() if title_el else "Unknown title"
                link = title_el.get_attribute("href") if title_el else "#"

                full_link = f"https://trackid.net{link}" if link.startswith("/") else link
                results.append({
                    "title": title,
                    "url": full_link
                })

            browser.close()
            return results

    except Exception as e:
        logging.error("Scraper failed", exc_info=True)
        raise Exception("Timed out waiting for results. Check selector or network.")