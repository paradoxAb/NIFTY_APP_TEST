import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 🌙 Page Setup
st.set_page_config(page_title="Nifty Stocks Dashboard", page_icon="📊", layout="wide")

# 🎨 Dark Theme Styling
plt.style.use("dark_background")
sns.set_style("darkgrid")
sns.set_palette("bright")

# 📂 Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("Nifty_Stocks.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# 🏷️ Sidebar Filters
st.sidebar.markdown("## 🔍 Filters")
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("📂 Select Category", categories)

filtered_df = df[df['Category'] == selected_category]
symbols = filtered_df['Symbol'].unique()
selected_symbols = st.sidebar.multiselect("📌 Select Symbol(s)", symbols, default=[symbols[0]])

chart_type = st.sidebar.radio("📊 Chart Type", ["Line Chart", "Area Chart", "Both"])

# 🎯 Title
st.markdown(
    "<h1 style='text-align: center; color: cyan;'>📈 Nifty Stocks Interactive Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h3 style='text-align: center; color: orange;'>Category: {selected_category} | Symbols: {', '.join(selected_symbols)}</h3>",
    unsafe_allow_html=True
)

# 📊 Plot Chart
fig, ax = plt.subplots(figsize=(12, 6))

for symbol in selected_symbols:
    stock_data = df[df['Symbol'] == symbol]

    if chart_type == "Line Chart":
        sns.lineplot(x="Date", y="Close", data=stock_data, label=symbol, ax=ax)

    elif chart_type == "Area Chart":
        ax.fill_between(stock_data["Date"], stock_data["Close"], alpha=0.4, label=symbol)

    else:  # Both
        sns.lineplot(x="Date", y="Close", data=stock_data, label=symbol, ax=ax)
        ax.fill_between(stock_data["Date"], stock_data["Close"], alpha=0.2)

ax.set_xlabel("Date", fontsize=12, color="white")
ax.set_ylabel("Closing Price", fontsize=12, color="white")
ax.set_title("Stock Price Trend", fontsize=16, fontweight="bold", color="cyan")
plt.xticks(rotation=45, color="white")
plt.yticks(color="white")
plt.legend(title="Symbols", facecolor="black", labelcolor="white")

st.pyplot(fig)

# 📑 Show Data Table
if st.checkbox("📋 Show Raw Data Table"):
    st.dataframe(filtered_df[filtered_df['Symbol'].isin(selected_symbols)])
