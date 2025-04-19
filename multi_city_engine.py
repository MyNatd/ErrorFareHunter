# multi_city_engine.py

from search_engine import fetch_all, filter_and_alert
import asyncio

# Template แบบ Manual
MULTI_CITY_TEMPLATES = [
    ["BKK", "HKG", "JFK", "HKG", "SIN", "BKK"],
    ["BKK", "TPE", "LAX", "TPE", "BKK"],
    ["SIN", "ICN", "SFO", "ICN", "SIN"],
    ["KUL", "HND", "NYC", "HND", "SIN"],
]

def generate_multi_city_routes(origin, destination):
    """Generate fixed Multi-City Routes."""
    routes = []

    for template in MULTI_CITY_TEMPLATES:
        if template[0] == origin and template[-1] == origin:
            routes.append(template)
        elif template[0] == origin and template[-1] != origin:
            routes.append(template)

    routes.append([origin, destination, origin])  # default
    return routes

# ✅ ใส่ตรงนี้! (ฟังก์ชันของคุณ)
SEA = ["BKK", "SIN", "KUL", "SGN", "DPS"]
NORTH_ASIA = ["HKG", "TPE", "ICN", "NRT"]
EUROPE = ["LHR", "CDG", "FRA", "AMS"]
USA = ["JFK", "LAX", "SFO", "ORD"]

def generate_dynamic_routes():
    """Generate Dynamic Multi-City Routes."""
    routes = []
    for sea in SEA:
        for na in NORTH_ASIA:
            for eu in EUROPE:
                for usa in USA:
                    routes.append([sea, na, eu, usa, sea])
    return routes

async def fetch_multi_city(routes, departure_date, return_date=None):
    """Fetch flight prices for multi-city routes."""
    all_flights = []

    for i in range(len(routes) - 1):
        leg_origin = routes[i]
        leg_dest = routes[i + 1]
        flights = await fetch_all(leg_origin, leg_dest, departure_date, return_date)
        all_flights.extend(flights)

    return all_flights

def validate_multi_city_deal(all_flights, cabin_class, threshold_thb):
    """Check if multi-city deal total is under threshold."""
    total_price = sum([f['price_thb'] for f in all_flights if f['cabin_class'] == cabin_class])

    if total_price <= threshold_thb:
        return True, total_price
    return False, total_price
