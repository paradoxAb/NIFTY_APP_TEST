import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Title of the app
st.title("📈 Nifty Stocks Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Nifty_Stocks.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# Sidebar - Select Category
st.sidebar.header("Filter Options")
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("Select Category", categories)

# Filter by category
filtered_df = df[df['Category'] == selected_category]

# Show available symbols
symbols = filtered_df['Symbol'].unique()
selected_symbol = st.sidebar.selectbox("Select Symbol", symbols)

# Filter by symbol
stock_data = df[df['Symbol'] == selected_symbol]

# Plot line chart
st.subheader(f"Closing Price Trend for {selected_symbol}")
fig, ax = plt.subplots(figsize=(10, 5))
sb.lineplot(x='Date', y='Close', data=stock_data, ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Show raw data (optional)
if st.checkbox("Show Raw Data"):
    st.write(stock_data)
