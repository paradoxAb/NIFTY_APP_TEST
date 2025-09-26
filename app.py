import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 🌙 Page Setup
st.set_page_config(page_title="Nifty Stocks Dashboard", page_icon="📊", layout="wide")

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
selected_symbol = st.sidebar.selectbox("📌 Select Symbol", symbols)

chart_type = st.sidebar.radio("📊 Chart Type", ["Line Chart", "Area Chart", "Candlestick", "Volume", "Combined"])

# 🎯 Title
st.markdown(
    "<h1 style='text-align: center; color: cyan;'>📈 Nifty Stocks Interactive Dashboard</h1>",
    unsafe_allow_html=True
)
st.markdown(
    f"<h3 style='text-align: center; color: orange;'>Category: {selected_category} | Symbol: {selected_symbol}</h3>",
    unsafe_allow_html=True
)

# 🎨 Filtered Data
stock_data = df[df['Symbol'] == selected_symbol].sort_values("Date")

# 📊 Plotly Charts
fig = go.Figure()

if chart_type == "Line Chart":
    fig.add_trace(go.Scatter(
        x=stock_data["Date"], y=stock_data["Close"],
        mode="lines", name="Close Price",
        line=dict(color="cyan")
    ))

elif chart_type == "Area Chart":
    fig.add_trace(go.Scatter(
        x=stock_data["Date"], y=stock_data["Close"],
        mode="lines", name="Close Price",
        fill="tozeroy", line=dict(color="orange")
    ))

elif chart_type == "Candlestick":
    fig.add_trace(go.Candlestick(
        x=stock_data["Date"],
        open=stock_data["Open"], high=stock_data["High"],
        low=stock_data["Low"], close=stock_data["Close"],
        name="Candlestick"
    ))

elif chart_type == "Volume":
    colors = ["green" if c >= o else "red" for c, o in zip(stock_data["Close"], stock_data["Open"])]
    fig.add_trace(go.Bar(
        x=stock_data["Date"], y=stock_data["Volume"],
        marker_color=colors, name="Volume"
    ))

elif chart_type == "Combined":
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=stock_data["Date"],
        open=stock_data["Open"], high=stock_data["High"],
        low=stock_data["Low"], close=stock_data["Close"],
        name="Candlestick"
    ))
    # Volume as bar below
    fig.add_trace(go.Bar(
        x=stock_data["Date"], y=stock_data["Volume"],
        marker_color="lightblue", name="Volume", opacity=0.4,
        yaxis="y2"
    ))

    # Dual axis for volume
    fig.update_layout(
        yaxis2=dict(
            overlaying="y",
            side="right",
            showgrid=False,
            position=1.0
        )
    )

# 🖌️ Dark Theme Layout
fig.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="Price",
    plot_bgcolor="black",
    paper_bgcolor="black",
    font=dict(color="white"),
    legend=dict(bgcolor="rgba(0,0,0,0.5)")
)

st.plotly_chart(fig, use_container_width=True)

# 📑 Show Data Table
if st.checkbox("📋 Show Raw Data Table"):
    st.dataframe(stock_data)
