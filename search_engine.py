# search_engine.py

import asyncio
from scraper_skyscanner import fetch_skyscanner
from scraper_googleflights import fetch_googleflights
from scraper_kayak import fetch_kayak
from scraper_kiwi import fetch_kiwi
from database import insert_flight_price, insert_flight_sources, deal_exists
from alert_manager import send_telegram_alert, send_line_alert
from currency_converter import get_exchange_rates
import os
from currency_cache import get_exchange_rates_cached

# Load .env config
PRICE_THRESHOLD_ECONOMY = int(os.getenv('PRICE_THRESHOLD_ECONOMY', 15000))
PRICE_THRESHOLD_PREMIUM_ECO = int(os.getenv('PRICE_THRESHOLD_PREMIUM_ECO', 30000))
PRICE_THRESHOLD_BUSINESS = int(os.getenv('PRICE_THRESHOLD_BUSINESS', 50000))
PRICE_THRESHOLD_FIRST = int(os.getenv('PRICE_THRESHOLD_FIRST', 60000))

CABIN_PRIORITY = os.getenv('CABIN_PRIORITY', "first,business,premium_economy,economy").split(",")

# Mapping Cabin Threshold
CABIN_THRESHOLDS = {
    "first": PRICE_THRESHOLD_FIRST,
    "business": PRICE_THRESHOLD_BUSINESS,
    "premium_economy": PRICE_THRESHOLD_PREMIUM_ECO,
    "economy": PRICE_THRESHOLD_ECONOMY,
}

# ---------------------------
# ✅ ใส่ตรงนี้นะ
def filter_and_alert(flights):
    for cabin in CABIN_PRIORITY:
        filtered_flights = [f for f in flights if f['cabin_class'] == cabin and f['price_thb'] <= CABIN_THRESHOLDS[cabin]]

        for flight in filtered_flights:
            if deal_exists(flight['origin'], flight['destination'], flight['departure_date'], flight['price_thb'], flight['airline']):
                print(f"[Duplicate] {flight['origin']} → {flight['destination']} {flight['departure_date']} {flight['price_thb']} already exists")
                continue

            # Insert Main Flight
            flight_main = {
                "origin": flight['origin'],
                "destination": flight['destination'],
                "origin_region": flight['origin_region'],
                "destination_region": flight['destination_region'],
                "departure_date": flight['departure_date'],
                "cabin_class": flight['cabin_class'],
                "airline": flight['airline'],
                "source": flight['source'],
                "min_price": flight['price_thb'],
                "currency": "THB",
                "booking_url": flight['booking_url'],
                "is_mistake_fare": True,
            }
            flight_id = insert_flight_price(flight_main)

            # Insert OTA Source
            source_entry = {
                "flight_price_id": flight_id,
                "booking_source": flight['booking_source'],
                "booking_url": flight['booking_url'],
                "price": flight['price_thb'],
                "currency": "THB",
                "region": flight['origin_region'],
            }
            insert_flight_sources([source_entry])

            # Alert
            message = f"""✈️ *{flight['origin']} → {flight['destination']}*\n
Cabin: {flight['cabin_class'].capitalize()}
Date: {flight['departure_date']}
Price: {flight['price_thb']:,} THB
Airline: {flight['airline']}
Source: {flight['booking_source']}
"""
            send_telegram_alert(message, urls=[flight['booking_url']])
            send_line_alert(message)
            print(f"[Alert Sent] {flight['origin']} → {flight['destination']} {flight['price_thb']} THB {flight['cabin_class']}")
# ---------------------------

# Parallel Search
async def fetch_all(origin, destination, departure_date, return_date=None):
    rates = get_exchange_rates_cached()

    tasks = [
        asyncio.to_thread(fetch_skyscanner, origin, destination, departure_date, return_date, "economy", rates),
        asyncio.to_thread(fetch_googleflights, origin, destination, departure_date, return_date, "economy", rates),
        asyncio.to_thread(fetch_kayak, origin, destination, departure_date, return_date, "economy", rates),
        asyncio.to_thread(fetch_kiwi, origin, destination, departure_date, return_date, "economy", rates),
    ]

    results = await asyncio.gather(*tasks)
    flights = [flight for result in results for flight in result]  # flatten

    return flights
