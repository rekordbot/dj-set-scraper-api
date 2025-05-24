from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist_name: str):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        search_url = f"https://trackid.net/search?q={artist_name.replace(' ', '+')}"
        page.goto(search_url)
        page.wait_for_selector(".audiostream-card", timeout=10000)

        cards = page.query_selector_all(".audiostream-card")[:10]

        for card in cards:
            title = card.query_selector(".title").inner_text().strip()
            link = card.query_selector("a").get_attribute("href")
            url = f"https://trackid.net{link}"
            date_el = card.query_selector(".date")
            date_text = date_el.inner_text().strip() if date_el else None

            # Visit mix page
            page.goto(url)
            page.wait_for_selector("ul.tracklist", timeout=5000)
            track_els = page.query_selector_all("ul.tracklist li")
            tracks = [t.inner_text().strip() for t in track_els]

            results.append({
                "title": title,
                "url": url,
                "date": date_text,
                "tracklist": tracks
            })

        browser.close()

    return results