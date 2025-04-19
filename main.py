# main.py

import asyncio
from search_engine import fetch_all, filter_and_alert
from multi_city_engine import generate_multi_city_routes, generate_dynamic_routes, fetch_multi_city, validate_multi_city_deal
from expansion_engine import expand_search_if_good
import os
import time

# Load .env Config
ORIGINS = os.getenv('ORIGINS').split(',')
DESTINATIONS = os.getenv('DESTINATIONS').split(',')
DATES = os.getenv('DEPARTURE_DATES').split(',')
INTERVAL_MINUTES = int(os.getenv('SEARCH_INTERVAL_MINUTES', 5))
PRICE_THRESHOLD_ECONOMY = int(os.getenv('PRICE_THRESHOLD_ECONOMY', 15000))

async def run_search_cycle():
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            if origin == destination:
                continue
            for departure_date in DATES:
                print(f"Searching {origin} → {destination} on {departure_date}")

                # Search Direct Flights
                flights = await fetch_all(origin, destination, departure_date)
                filter_and_alert(flights)

                # Expand Neighbor Airports
                await expand_search_if_good(origin, destination, departure_date)

                # Generate and Search Dynamic Multi-City Routes
                dynamic_routes = generate_dynamic_routes()
                for route in dynamic_routes:
                    multi_city_flights = await fetch_multi_city(route, departure_date)
                    is_good, total_price = validate_multi_city_deal(multi_city_flights, "economy", PRICE_THRESHOLD_ECONOMY)
                    if is_good:
                        print(f"[Dynamic Multi-City Deal Found!] Total Price: {total_price} THB (Route: {route})")
                        filter_and_alert(multi_city_flights)

                # Generate and Search Specific Multi-City Routes
                multi_routes = generate_multi_city_routes(origin, destination)
                for route in multi_routes:
                    multi_city_flights = await fetch_multi_city(route, departure_date)
                    is_good, total_price = validate_multi_city_deal(multi_city_flights, "economy", PRICE_THRESHOLD_ECONOMY)
                    if is_good:
                        print(f"[Fixed Multi-City Deal Found!] Total Price: {total_price} THB (Route: {route})")
                        filter_and_alert(multi_city_flights)

if __name__ == "__main__":
    while True:
        asyncio.run(run_search_cycle())
        print(f"Sleeping for {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)
