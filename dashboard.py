# dashboard.py

import streamlit as st
import pandas as pd
from supabase import create_client
import os
import plotly.express as px
from ai_model import load_flight_data, train_simple_model, predict_future_price

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Mistake Fare Hunter Dashboard", layout="wide")

st.title("✈️ Mistake Fare Hunter V4++ Dashboard")

# Load data
df = load_flight_data()

# Summary Stats
st.subheader("Summary")
st.metric("Total Deals Found", len(df))
st.metric("Average Price (THB)", int(df['min_price'].mean()))

# Price by Cabin Class
st.subheader("Price by Cabin Class")
fig1 = px.box(df, x="cabin_class", y="min_price", color="cabin_class")
st.plotly_chart(fig1)

# Latest Deals Table
st.subheader("Latest Deals")
st.dataframe(df.sort_values("timestamp", ascending=False)[["origin", "destination", "departure_date", "cabin_class", "min_price", "airline"]])

# Future Prediction
st.subheader("Price Prediction")
if not df.empty:
    model = train_simple_model(df)
    import time
    future_time = time.time() + 30*24*60*60  # 30 วันข้างหน้า
    future_price = predict_future_price(model, future_time)
    st.metric("Predicted Price in 30 Days (THB)", int(future_price))
