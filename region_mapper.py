# region_mapper.py

REGION_MAPPING = {
    "BKK": "SEA", "DMK": "SEA", "CNX": "SEA", "HKT": "SEA", "KBV": "SEA", "HDY": "SEA",
    "SIN": "SEA", "KUL": "SEA", "PEN": "SEA", "LGK": "SEA", "BKI": "SEA",
    "SGN": "SEA", "HAN": "SEA", "DAD": "SEA",
    "HKG": "North Asia", "TPE": "North Asia", "KHH": "North Asia",
    "NRT": "North Asia", "HND": "North Asia", "ICN": "North Asia",
    "VTE": "SEA", "LPQ": "SEA", "RGN": "SEA", "MDL": "SEA",
    "SYD": "Oceania", "MEL": "Oceania",
    "DEL": "South Asia", "BOM": "South Asia",
}

def get_region(airport_code):
    """Return region name given IATA airport code."""
    return REGION_MAPPING.get(airport_code.upper(), "Unknown")
