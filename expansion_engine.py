# expansion_engine.py

from search_engine import fetch_all, filter_and_alert
from neighbors import NEIGHBOR_AIRPORTS
import asyncio

async def expand_search_if_good(origin, destination, departure_date, return_date=None, rates={}):
    """Expand search to neighbor airports if good deal found."""

    neighbors = NEIGHBOR_AIRPORTS.get(origin, [])
    if not neighbors:
        print(f"[Expand] No neighbors configured for {origin}")
        return

    tasks = []
    for neighbor_origin in neighbors:
        print(f"[Expand] Trying from neighbor {neighbor_origin} → {destination}")
        tasks.append(fetch_all(neighbor_origin, destination, departure_date, return_date))

    all_flights_nested = await asyncio.gather(*tasks)
    all_flights = [flight for result in all_flights_nested for flight in result]

    # Filter และ Alert
    filter_and_alert(all_flights)
