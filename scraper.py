import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.winds-up.com/"
URLS_SPOT = {
    "gruissan": "spot-gruissan-windsurf-kitesurf-23-observations-releves-vent.html",
    "veille_nouvelle": "spot-la-vieille-nouvelle-usine-windsurf-kitesurf-1617-observations-releves-vent.html",
    "pont_levis": "spot-syite-cn-barrou-windsurf-kitesurf-48-observations-releves-vent.html",
    "richelieu": "spot-agde-windsurf-kitesurf-1-observations-releves-vent.html",
}


def scrape_spot_page(spot_name: str) -> BeautifulSoup | None:
    """Scrape the spot page.

    Args:
        spot (str): Name of the spot.

    Returns:
        BeautifulSoup | None: BeautifulSoup object of the spot page or None if the request failed.
    """
    url_target_spot = URLS_SPOT.get(spot_name)
    if url_target_spot is None:
        return None
    response = requests.get(f"{BASE_URL}{url_target_spot}")
    response.raise_for_status()
    return BeautifulSoup(response.content, "html.parser")


def get_data_from_last_reading_spot(spot_name: str) -> list:
    """Get the data from the last reading of the spot.

    Args:
        spot (str): Name of the spot.

    Returns:
        list: List of data from the last reading of the spot.
    """
    spot_data = scrape_spot_page(spot_name)
    if spot_data is None:
        return []
    data_tables = spot_data.find_all("table", class_="tableau")
    rows = [row for table in data_tables for row in table.find_all("tr")[2:]]
    for row in rows:
        cells = row.find_all("td")
        if len(cells) > 2:
            return cells
    return []

def parse_data_from_last_reading(spot_name: str) -> dict | None:
    """Parse the data from the last reading of the spot.

    Returns:
        dict: Dictionary of data from the last reading of the spot.
    """
    if data := get_data_from_last_reading_spot(spot_name):
        hours, direction, avg_knots, _, min_knots, max_knots = [item.text.strip() for item in data]
        date_cleaned = " ".join(hours.split())
        direction_cleaned = direction.split()[0]
        time_only = date_cleaned.split()[-1]

        return {
            "spot": spot_name,
            "date": date_cleaned or None,
            "time": time_only or None,
            "direction": direction_cleaned or None,
            "avg_knots": avg_knots or None,
            "min_knots": min_knots or None,
            "max_knots": max_knots or None,
        }
    else:
        return None