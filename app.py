import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Indian Stock Analyzer", page_icon="📈")

st.title("📈 Indian Stock & Financial Metrics Analyzer")
st.write("Built by Naresh | Finance & Data Analytics Portfolio")

# User input for NSE stock ticker
ticker = st.text_input("Enter NSE Stock Ticker (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):", "TCS.NS")
period = st.selectbox("Select Time Period:", ["6mo", "1y", "2y", "5y"], index=1)

if st.button("Analyze Stock"):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        st.error("Invalid ticker or no data found. Make sure to add '.NS' for NSE stocks.")
    else:
        # Display Key Financial Info
        info = stock.info
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price (₹)", f"₹{hist['Close'].iloc[-1]:.2f}")
        col2.metric("P/E Ratio", info.get("trailingPE", "N/A"))
        col3.metric("Market Cap", f"₹{info.get('marketCap', 0) / 1e7:,.0f} Cr")

        # Calculate 50-Day Moving Average
        hist['50_MA'] = hist['Close'].rolling(window=50).mean()

        # Plot Closing Price & 50-Day Moving Average
        st.subheader(f"{ticker} Price Trend & 50-Day Moving Average")
        st.line_chart(hist[['Close', '50_MA']])

        # Show Recent Historical Data Table
        st.subheader("Recent Trading Data")
        st.dataframe(hist[['Open', 'High', 'Low', 'Close', 'Volume']].tail(10))
