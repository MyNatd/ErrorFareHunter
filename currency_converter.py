# currency_converter.py

import requests
import os

EXCHANGE_RATE_API = os.getenv('EXCHANGE_RATE_API')

def get_exchange_rates(base="THB"):
    """Fetch latest exchange rates."""
    url = f"{EXCHANGE_RATE_API}{base}"
    try:
        response = requests.get(url)
        data = response.json()
        if 'rates' in data:
            return data['rates']
        else:
            raise Exception("Invalid currency data format.")
    except Exception as e:
        print(f"Currency Fetch Error: {e}")
        return {}

def convert_currency(amount, from_currency, rates):
    """Convert amount from from_currency to base THB using rates dict."""
    if from_currency == "THB":
        return amount
    if from_currency not in rates:
        print(f"Warning: {from_currency} not found in rates.")
        return None
    return amount / rates[from_currency]
