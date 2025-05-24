from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist_name: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_url = f"https://trackid.net/audiostreams?keywords={artist_name}"
        print(f"Navigating to: {search_url}")
        page.goto(search_url, timeout=60000)

        try:
            page.wait_for_selector(".audiostream-card__title", timeout=20000)
        except Exception:
            raise Exception("Timed out waiting for results. Check selector or network.")

        cards = page.query_selector_all(".audiostream-card")
        print(f"Found {len(cards)} cards")

        results = []
        for card in cards:
            title_elem = card.query_selector(".audiostream-card__title")
            date_elem = card.query_selector(".audiostream-card__timestamp")
            link_elem = card.query_selector("a")

            title = title_elem.inner_text().strip() if title_elem else "Unknown Title"
            date = date_elem.inner_text().strip() if date_elem else "Unknown Date"
            link = link_elem.get_attribute("href") if link_elem else None

            results.append({
                "title": title,
                "date": date,
                "url": f"https://trackid.net{link}" if link else None
            })

        browser.close()
        return results