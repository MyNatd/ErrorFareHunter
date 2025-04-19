# scraper_kayak.py

import requests
import os
from currency_converter import convert_currency
from region_mapper import get_region

def fetch_kayak(origin, destination, departure_date, return_date=None, cabin_class="economy", rates={}):
    """Scrape Kayak flight price."""
    base_url = "https://www.kayak.com/s/horizon/flights/api/search"

    params = {
        "origin": origin,
        "destination": destination,
        "depart_date": departure_date,
        "cabin": cabin_class,
        "travelers": "1",
        "currency": "THB",
        "market": "TH",
    }
    if return_date:
        params["return_date"] = return_date

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        res = requests.get(base_url, headers=headers, params=params)
        if res.status_code == 200:
            data = res.json()

            flights = []
            for deal in data.get('offers', []):
                price = deal.get('price', {}).get('amount')
                airline = deal.get('airline_display_name')
                booking_link = deal.get('deeplink_url')

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
                        "source": "kayak",
                        "booking_url": booking_link,
                        "booking_source": "Kayak",
                        "origin_region": get_region(origin),
                        "destination_region": get_region(destination),
                    })

            return flights
        else:
            print(f"[Kayak] Error {res.status_code}: {res.text}")
            return []

    except Exception as e:
        print(f"[Kayak] Exception: {e}")
        return []
