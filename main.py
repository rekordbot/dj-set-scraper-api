from fastapi import FastAPI
from scrape_trackid import scrape_trackid_mixes
import logging

app = FastAPI()

@app.get("/trackid")
def trackid(artist: str):
    print(f"Received request for artist: {artist}")
    try:
        return scrape_trackid_mixes(artist)
    except Exception as e:
        logging.exception("Scraper failed")
        return {"error": str(e)}