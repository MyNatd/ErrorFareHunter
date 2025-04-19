# main.py

import asyncio
from search_engine import fetch_all, filter_and_alert
import os
import time

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

if __name__ == "__main__":
    while True:
        run_search_cycle()
        print(f"Sleeping for {INTERVAL_MINUTES} minutes...\n")
        time.sleep(INTERVAL_MINUTES * 60)
