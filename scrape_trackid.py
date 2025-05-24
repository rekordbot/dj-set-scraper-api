import requests
from bs4 import BeautifulSoup

BASE_URL = "https://trackid.net"

def scrape_trackid_mixes(artist_name: str):
    search_url = f"{BASE_URL}/search?q={artist_name.replace(' ', '+')}"
    
    # Bypass SSL cert verification
    res = requests.get(search_url, verify=False)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for card in soup.select(".audiostream-card")[:10]:  # limit to 10 results
        title = card.select_one(".title").get_text(strip=True)
        url = BASE_URL + card.select_one("a")["href"]
        date = card.select_one(".date")
        date_text = date.get_text(strip=True) if date else None

        # Also bypass SSL verification for each mix page
        mix_page = requests.get(url, verify=False)
        mix_soup = BeautifulSoup(mix_page.text, "html.parser")
        tracks = [li.get_text(strip=True) for li in mix_soup.select("ul.tracklist li")]

        results.append({
            "title": title,
            "url": url,
            "date": date_text,
            "tracklist": tracks
        })

    return results