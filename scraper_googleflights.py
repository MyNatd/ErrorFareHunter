# scraper_googleflights.py

from playwright.sync_api import sync_playwright
from currency_converter import convert_currency
from region_mapper import get_region

def fetch_googleflights(origin, destination, departure_date, return_date=None, cabin_class="economy", rates={}):
    """Scrape Google Flights live price."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        base_url = f"https://www.google.com/travel/flights?q=flights%20from%20{origin}%20to%20{destination}%20on%20{departure_date}"
        if return_date:
            base_url += f"%20returning%20{return_date}"

        page.goto(base_url)
        page.wait_for_timeout(5000)  # รอโหลดข้อมูล

        prices = page.locator('div[role="listitem"] span[aria-label*="THB"]').all_text_contents()
        airlines = page.locator('div[role="listitem"] div[class*="gws-flights__ellipsize"]').all_text_contents()

        flights = []
        for i in range(min(len(prices), len(airlines))):
            try:
                price = int(prices[i].replace("THB", "").replace(",", "").strip())
                airline = airlines[i]
                flights.append({
                    "origin": origin,
                    "destination": destination,
                    "departure_date": departure_date,
                    "return_date": return_date,
                    "price": price,
                    "price_thb": convert_currency(price, "THB", rates),
                    "cabin_class": cabin_class,
                    "airline": airline,
                    "source": "googleflights",
                    "booking_url": base_url,
                    "booking_source": "Google Flights",
                    "origin_region": get_region(origin),
                    "destination_region": get_region(destination),
                })
            except Exception as e:
                print(f"[Google Flights] Parsing Error: {e}")

        browser.close()
        return flights
