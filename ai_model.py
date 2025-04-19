# ai_model.py

from supabase import create_client
import pandas as pd
from sklearn.linear_model import LinearRegression
import os
from sklearn.ensemble import RandomForestRegressor

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_flight_data():
    """Load historical flight prices from Supabase."""
    response = supabase.table('flight_prices').select("*").execute()
    df = pd.DataFrame(response.data)
    return df

def train_simple_model(df):
    """Train basic Linear Regression model to predict future prices."""
    df = df.dropna(subset=["min_price", "timestamp"])

    # เตรียมฟีเจอร์
    df['timestamp_numeric'] = pd.to_datetime(df['timestamp']).astype(int) / 10**9  # เปลี่ยน timestamp เป็นตัวเลข
    X = df[['timestamp_numeric']]
    y = df['min_price']

    model = LinearRegression()
    model.fit(X, y)
    return model

def train_advanced_model(df):
    """Train Random Forest Model."""
    df = df.dropna(subset=["min_price", "timestamp"])
    df['timestamp_numeric'] = pd.to_datetime(df['timestamp']).astype(int) / 10**9
    X = df[['timestamp_numeric']]
    y = df['min_price']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

def predict_future_price(model, future_timestamp):
    """Predict future price given future timestamp (as POSIX seconds)."""
    return model.predict([[future_timestamp]])[0]
