# currency_cache.py

import time
from currency_converter import get_exchange_rates

CACHED_RATES = None
LAST_FETCH = 0
CACHE_DURATION_SECONDS = 6 * 3600  # 6 ชั่วโมง

def get_exchange_rates_cached(base="THB"):
    """Get cached exchange rates, update if older than 6 hours."""
    global CACHED_RATES, LAST_FETCH
    current_time = time.time()

    # เงื่อนไข: ถ้าเก่าเกิน CACHE_DURATION หรือยังไม่มีข้อมูล
    if current_time - LAST_FETCH > CACHE_DURATION_SECONDS or not CACHED_RATES:
        print("[Currency] Refreshing Exchange Rates...")
        latest_rates = get_exchange_rates(base)
        if latest_rates:
            CACHED_RATES = latest_rates
            LAST_FETCH = current_time
        else:
            print("[Currency] Warning: Failed to fetch exchange rates, using old cache if available.")

    return CACHED_RATES or {}
