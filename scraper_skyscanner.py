# scraper_skyscanner.py

import os
from currency_converter import convert_currency
from region_mapper import get_region
from scraper_core import fetch_url
import aiohttp
import json

async def fetch_skyscanner(origin, destination, departure_date, return_date=None, cabin_class="economy", rates={}):
    """Scrape Skyscanner flight price via async method."""

    trip_type = "oneway" if return_date is None else "roundtrip"
    url = f"https://www.skyscanner.net/g/autosuggest-flights/{origin}/{destination}/{departure_date}"

    params = {
        "market": "TH",
        "locale": "en-GB",
        "currency": "THB",
        "tripType": trip_type,
        "adults": 1,
        "cabinClass": cabin_class,
    }
    if return_date:
        params["returnDate"] = return_date

    async with aiohttp.ClientSession() as session:
        response_text = await fetch_url(session, url, params=params)

        if not response_text:
            return []

        try:
            data = json.loads(response_text)
        except Exception as e:
            print(f"[Skyscanner] JSON Parse Error: {e}")
            return []

        # ดึงเฉพาะราคาที่ถูกที่สุด
        flights = []
        for deal in data.get('deals', []):
            price = deal.get('price', None)
            airline = deal.get('carrier', None)
            booking_link = deal.get('deeplink', None)

            if price and booking_link:
                flights.append({
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "price": price,
                    "price_thb": convert_currency(price, "THB", rates),
                    "cabin_class": cabin_class,
                    "airline": airline,
                    "source": "skyscanner",
                    "booking_url": booking_link,
                    "booking_source": "Skyscanner",
                    "origin_region": get_region(origin),
                    "destination_region": get_region(destination),
                })

        return flights
