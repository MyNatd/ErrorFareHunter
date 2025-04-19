# database.py

from supabase import create_client
import os

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_flight_price(flight_data):
    """Insert a new flight into flight_prices table."""
    response = supabase.table('flight_prices').insert(flight_data).execute()
    if response.status_code == 201:
        return response.data[0]['id']  # return new flight id
    else:
        raise Exception(f"Insert flight_prices failed: {response}")

def insert_flight_sources(sources_data):
    """Insert multiple sources into flight_price_sources table."""
    response = supabase.table('flight_price_sources').insert(sources_data).execute()
    if response.status_code != 201:
        raise Exception(f"Insert flight_price_sources failed: {response}")

def query_recent_deals(limit=10):
    """Query latest flight deals (for debug/monitoring)."""
    response = supabase.table('flight_prices').select("*").order('timestamp', desc=True).limit(limit).execute()
    return response.data
