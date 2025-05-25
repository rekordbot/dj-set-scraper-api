from playwright.sync_api import sync_playwright

def test_page_content():
    url = "https://trackid.net/audiostreams?keywords=Redfreya"
    print(f"Testing content at: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000)
            html = page.content()
            print(f"Page content loaded, length: {len(html)}")
        except Exception as e:
            print(f"Failed to load page content: {e}")
        finally:
            browser.close()