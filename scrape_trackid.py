from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist):
    search_url = f"https://trackid.net/audiostreams?keywords={artist}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        # Wait for a visible link to a mix set
        page.wait_for_selector("a.audiostreams__title", timeout=15000)
        cards = page.query_selector_all("a.audiostreams__title")

        results = []
        for card in cards:
            title = card.inner_text().strip()
            link = card.get_attribute("href")
            full_url = f"https://trackid.net{link}"
            results.append({"title": title, "url": full_url})

        browser.close()
        return results