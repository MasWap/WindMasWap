import requests
from fastapi import FastAPI, HTTPException

import scraper

app = FastAPI()


@app.get("/{spot}")
async def get_wind_data(spot: str):
    try:
        # Check if the spot exists in the URLS_SPOT dictionary
        if spot not in scraper.URLS_SPOT:
            raise HTTPException(status_code=404, detail="Spot not found.")
        # Retrieve spot data if it exists
        if data := scraper.parse_data_from_last_reading(spot):
            return data
        else:
            raise HTTPException(status_code=404, detail="No data found for the spot.")
    except requests.exceptions.RequestException as e:
        # In case of an HTTP request error (for example, unable to connect to the site)
        raise HTTPException(
            status_code=500, detail="Failed to fetch data from the source."
        ) from e