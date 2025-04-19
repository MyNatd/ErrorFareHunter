# multi_city_engine.py

from search_engine import fetch_all, filter_and_alert
import asyncio

# กำหนด Multi-City Templates
MULTI_CITY_TEMPLATES = [
    ["BKK", "HKG", "JFK", "HKG", "SIN", "BKK"],
    ["BKK", "TPE", "LAX", "TPE", "BKK"],
    ["SIN", "ICN", "SFO", "ICN", "SIN"],
    ["KUL", "HND", "NYC", "HND", "SIN"],
]

def generate_multi_city_routes(origin, destination):
    """สร้าง Multi-City Routes แบบไดนามิก."""
    routes = []

    for template in MULTI_CITY_TEMPLATES:
        if template[0] == origin and template[-1] == origin:
            routes.append(template)
        elif template[0] == origin and template[-1] != origin:
            routes.append(template)

    # Default simple multi-city
    routes.append([origin, destination, origin])

    return routes

async def fetch_multi_city(routes, departure_date, return_date=None):
    """ดึงข้อมูล multi-city ทั้งเส้นทาง."""
    all_flights = []

    for i in range(len(routes) - 1):
        leg_origin = routes[i]
        leg_dest = routes[i + 1]
        flights = await fetch_all(leg_origin, leg_dest, departure_date, return_date)
        all_flights.extend(flights)

    return all_flights

def validate_multi_city_deal(all_flights, cabin_class, threshold_thb):
    """Validate รวมราคาทุกขา ว่ายังไม่เกิน Threshold."""
    total_price = sum([f['price_thb'] for f in all_flights if f['cabin_class'] == cabin_class])

    if total_price <= threshold_thb:
        return True, total_price
    return False, total_price
