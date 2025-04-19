# main.py

import asyncio
from search_engine import fetch_all, filter_and_alert
import os
import timefrom multi_city_engine import generate_multi_city_routes, fetch_multi_city, validate_multi_city_deal
from expansion_engine import expand_search_if_good

ORIGINS = os.getenv('ORIGINS').split(',')
DESTINATIONS = os.getenv('DESTINATIONS').split(',')
DATES = os.getenv('DEPARTURE_DATES').split(',')
INTERVAL_MINUTES = int(os.getenv('SEARCH_INTERVAL_MINUTES', 5))

def run_search_cycle():
    for origin in ORIGINS:
        for destination in DESTINATIONS:
            if origin == destination:
                continue
            for departure_date in DATES:
                print(f"Searching {origin} → {destination} {departure_date}")
                flights = asyncio.run(fetch_all(origin, destination, departure_date))
                filter_and_alert(flights)

                # ถ้าเจอ deal ดี → ลอง Multi-City ขยาย
                # ใน filter_and_alert หรือตรงที่ detect Deal
                await expand_search_if_good(origin, destination, departure_date)
                multi_routes = generate_multi_city_routes(origin, destination)
                for route in multi_routes:
                    multi_city_flights = asyncio.run(fetch_multi_city(route, departure_date))
                    is_good, total_price = validate_multi_city_deal(multi_city_flights, "economy", PRICE_THRESHOLD_ECONOMY)
                    if is_good:
                        print(f"[Multi-City Deal Found!] Total Price: {total_price} THB")
                        filter_and_alert(multi_city_flights)

if __name__ == "__main__":
    while True:
        run_search_cycle()
        print(f"Sleeping for {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)





