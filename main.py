from fastapi import FastAPI
from scrape_trackid import scrape_trackid_mixes

app = FastAPI()

@app.get("/trackid")
def trackid(artist: str):
    return scrape_trackid_mixes(artist)
