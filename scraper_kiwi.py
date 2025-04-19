# scraper_kiwi.py

import requests
import os
from currency_converter import convert_currency
from region_mapper import get_region

def fetch_kiwi(origin, destination, departure_date, return_date=None, cabin_class="M", rates={}):
    """Scrape Kiwi.com flight price."""
    url = "https://api.tequila.kiwi.com/v2/search"

    # Convert cabin class
    cabin_map = {
        "economy": "M",
        "premium_economy": "W",
        "business": "C",
        "first": "F"
    }
    cabin = cabin_map.get(cabin_class.lower(), "M")

    headers = {
        "apikey": os.getenv('KIWI_API_KEY'),  # ต้องขอ key ที่ Tequila API
    }

    params = {
        "fly_from": origin,
        "fly_to": destination,
        "date_from": departure_date,
        "date_to": departure_date,
        "return_from": return_date if return_date else "",
        "return_to": return_date if return_date else "",
        "curr": "THB",
        "selected_cabins": cabin,
        "one_for_city": 1,
        "limit": 5
    }

    try:
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json()

            flights = []
            for deal in data.get('data', []):
                price = deal.get('price')
                booking_link = deal.get('deep_link')
                airline = deal.get('airlines', [None])[0]

                if price and booking_link:
                    flights.append({
                        "origin": origin,
                        "destination": destination,
                        "departure_date": departure_date,
                        "return_date": return_date,
                        "price": int(price),
                        "price_thb": convert_currency(int(price), "THB", rates),
                        "cabin_class": cabin_class,
                        "airline": airline,
                        "source": "kiwi",
                        "booking_url": booking_link,
                        "booking_source": "Kiwi",
                        "origin_region": get_region(origin),
                        "destination_region": get_region(destination),
                    })

            return flights
        else:
            print(f"[Kiwi] Error {res.status_code}: {res.text}")
            return []

    except Exception as e:
        print(f"[Kiwi] Exception: {e}")
        return []
