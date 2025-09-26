import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🎨 Streamlit Page Config
st.set_page_config(page_title="Nifty Stocks Dashboard", page_icon="📊", layout="wide")

# 🌈 Custom Style
sns.set_style("whitegrid")
sns.set_palette("Set2")

# 📂 Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("../Dataset/Nifty_Stocks.csv12.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# 🏷️ Sidebar - Filters
st.sidebar.header("🔍 Filter Options")

# Category selection
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("📂 Select Category", categories)

# Filter by category
filtered_df = df[df['Category'] == selected_category]

# Symbol selection (multi-select for comparison)
symbols = filtered_df['Symbol'].unique()
selected_symbols = st.sidebar.multiselect("📌 Select Symbol(s)", symbols, default=[symbols[0]])

# Chart type
chart_type = st.sidebar.radio("📊 Chart Type", ["Line Chart", "Area Chart"])

# 🎯 Main Dashboard
st.title("📈 Nifty Stocks Interactive Dashboard")
st.markdown(f"Showing **{chart_type}** for **{', '.join(selected_symbols)}** in category **{selected_category}**")

# 🎨 Plot
fig, ax = plt.subplots(figsize=(12, 6))

for symbol in selected_symbols:
    stock_data = df[df['Symbol'] == symbol]
    if chart_type == "Line Chart":
        sns.lineplot(x="Date", y="Close", data=stock_data, label=symbol, ax=ax)
    else:
        ax.fill_between(stock_data["Date"], stock_data["Close"], alpha=0.3, label=symbol)

ax.set_xlabel("Date")
ax.set_ylabel("Closing Price")
ax.set_title("Stock Price Trend", fontsize=16, fontweight="bold")
plt.xticks(rotation=45)
plt.legend(title="Symbols")
st.pyplot(fig)

# 📋 Show Raw Data Option
if st.checkbox("📑 Show Raw Data Table"):
    st.dataframe(filtered_df[filtered_df['Symbol'].isin(selected_symbols)])
