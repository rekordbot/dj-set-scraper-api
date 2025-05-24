from playwright.sync_api import sync_playwright
import time

def scrape_trackid_mixes(artist: str):
    search_url = f"https://trackid.net/audiostreams?keywords={artist}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to: {search_url}")
        page.goto(search_url, timeout=60000)

        try:
            page.wait_for_selector(".audiostream-card", timeout=10000)
        except:
            browser.close()
            raise Exception("Could not find any cards: Page.wait_for_selector timed out.")

        cards = page.locator(".audiostream-card")
        count = cards.count()
        results = []

        for i in range(count):
            card = cards.nth(i)
            title = card.locator(".audiostream-title").inner_text()
            link = card.locator("a").get_attribute("href")
            full_link = f"https://trackid.net{link}"
            results.append({
                "title": title,
                "url": full_link
            })

        browser.close()
        return results