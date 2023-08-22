from fastapi import FastAPI
import uvicorn
from bs4 import BeautifulSoup
from tabulate import tabulate
import requests

app = FastAPI()

# URLs disponibles
urls = {
    "Gruissan": "https://www.winds-up.com/spot-gruissan-windsurf-kitesurf-23-observations-releves-vent.html",
    "VieilleNouvelle": "https://www.winds-up.com/spot-la-vieille-nouvelle-usine-windsurf-kitesurf-1617-observations-releves-vent.html",
    "PontLevis": "https://www.winds-up.com/spot-syite-cn-barrou-windsurf-kitesurf-48-observations-releves-vent.html",
    "Richelieu": "https://www.winds-up.com/spot-agde-windsurf-kitesurf-1-observations-releves-vent.html",
}

@app.get("/{spot}")
async def get_wind_data(spot: str):
    if spot not in urls:
        return {"error": "Spot invalide"}

    url = urls[spot]
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, "html.parser")

    div = soup.find("div", class_="titre")
    if div:
        span = div.find("span")
        if span:
            text = span.find_next_sibling(text=True)

    table = soup.find("table", class_="tableau")
    all_tr = table.find_all("tr")
    before_last = all_tr[2]
    all_data = before_last.find_all("td")
    hour = all_data[0]
    orien = all_data[1]
    moy = all_data[2]
    min = all_data[4]
    max = all_data[5]

    orientation_cleaned = orien.text.split()[0]
    date_cleaned = " ".join(hour.text.split())
    time_only = date_cleaned.split()[-1]

    return {
        "Heure": time_only,
        "Orientation": orientation_cleaned,
        "Moyenne": f"{moy.text} kts",
        "Minimum": f"{min.text} kts",
        "Maximum": f"{max.text} kts"
    }

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
