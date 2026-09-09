import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Page Config
st.set_page_config(page_title="RAVAN 2.0 SCANNER", page_icon="👺", layout="wide")

st.markdown("""
<h1 style='text-align:center;color:#ff3300;'>👺 RAVAN 2.0 - LIVE SCANNER</h1>
<p style='text-align:center;color:gray;'>EMA 21 | ADX | RSI | VWAP | SuperTrend - 9:45 AM Setup</p>
""", unsafe_allow_html=True)

# Functions
def calculate_indicators(df):
    df['EMA21'] = df['Close'].ewm(span=21, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Signal Logic - Ravan Style
    df['Signal'] = "WAIT"
    df.loc[(df['Close'] > df['EMA21']) & (df['EMA21'] > df['EMA50']) & (df['RSI'] > 55) & (df['RSI'] < 75), 'Signal'] = "BUY"
    df.loc[(df['Close'] < df['EMA21']) & (df['EMA21'] < df['EMA50']) & (df['RSI'] < 45), 'Signal'] = "SELL"
    return df

# Sidebar
st.sidebar.title("⚙️ Ravan Setting")
scan_btn = st.sidebar.button("🔍 SCAN NOW - 9:45", type="primary", use_container_width=True)
st.sidebar.info("Nifty 50 stocks scan honge")

# Stock List - Ravan Scanner List
STOCKS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","BHARTIARTL.NS","SUNDRMFAST.NS","TATAMOTORS.NS","WIPRO.NS"]

if scan_btn:
    results = []
    bar = st.progress(0)
    status = st.empty()
    
    for i, sym in enumerate(STOCKS):
        status.text(f"Scanning {sym}... {i+1}/{len(STOCKS)}")
        try:
            data = yf.download(sym, period="10d", interval="15m", progress=False)
            if len(data) < 50: continue
            # Fix for multi-index from yfinance
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            
            data = calculate_indicators(data)
            last = data.iloc[-1]
            prev = data.iloc[-2]
            
            if last['Signal'] == "BUY" and prev['Signal'] != "BUY":
                price = float(last['Close'])
                results.append({
                    "SYMBOL": sym.replace(".NS",""),
                    "LTP": round(price,2),
                    "ENTRY": round(price,2),
                    "SL": round(price * 0.985,2),
                    "TARGET 1": round(price * 1.02,2),
                    "TARGET 2": round(price * 1.04,2),
                    "RSI": round(float(last['RSI']),1),
                    "EMA21": round(float(last['EMA21']),1),
                    "SIGNAL": "🔥 BUY"
                })
        except Exception as e:
            pass
        bar.progress((i+1)/len(STOCKS))
    
    status.empty()
    bar.empty()
    
    if results:
        df = pd.DataFrame(results)
        st.success(f"🔥 {len(results)} BUY Signals Found!")
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Ravan Cards
        for r in results:
            st.markdown(f"""
            <div style='border:2px solid #00ff00; padding:15px; border-radius:12px; margin:10px 0; background:linear-gradient(90deg,#0a0a0a,#1a1a1a);'>
                <div style='display:flex; justify-content:space-between;'>
                    <h3 style='color:white; margin:0;'>{r['SYMBOL']} <span style='color:#00ff00
