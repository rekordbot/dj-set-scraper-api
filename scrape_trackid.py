from playwright.sync_api import sync_playwright

def scrape_trackid_mixes(artist_name: str):
    print(f"Starting scrape for artist: {artist_name}")
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        search_url = f"https://trackid.net/search?q={artist_name.replace(' ', '+')}"
        print(f"Navigating to: {search_url}")
        page.goto(search_url)

        try:
            page.wait_for_selector(".audiostream-card", timeout=10000)
        except Exception as e:
            print("Could not find any cards:", e)
            return []

        cards = page.query_selector_all(".audiostream-card")[:10]
        print(f"Found {len(cards)} mix cards")

        for card in cards:
            title = card.query_selector(".title").inner_text().strip()
            link = card.query_selector("a").get_attribute("href")
            url = f"https://trackid.net{link}"
            date_el = card.query_selector(".date")
            date_text = date_el.inner_text().strip() if date_el else None

            page.goto(url)
            try:
                page.wait_for_selector("ul.tracklist", timeout=5000)
                track_els = page.query_selector_all("ul.tracklist li")
                tracks = [t.inner_text().strip() for t in track_els]
            except:
                tracks = []

            print(f"Scraped mix: {title} – {date_text}")

            results.append({
                "title": title,
                "url": url,
                "date": date_text,
                "tracklist": tracks
            })

        browser.close()

    return results