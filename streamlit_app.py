import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="RAVAN 2.0", page_icon="👺", layout="wide")
st.markdown("<h1 style='text-align:center;color:#ff3300;'>👺 RAVAN 2.0 - LIVE SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>EMA 21 | RSI | SuperTrend - 9:45 AM Setup</p>", unsafe_allow_html=True)

def get_data(symbol):
    df = yf.download(symbol, period="10d", interval="15m", progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    if len(df) < 50:
        return None
    df['EMA21'] = df['Close'].ewm(span=21).mean()
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    df['Signal'] = "WAIT"
    df.loc[(df['Close'] > df['EMA21']) & (df['EMA21'] > df['EMA50']) & (df['RSI'] > 55), 'Signal'] = "BUY"
    return df

st.sidebar.title("Ravan Scanner")
scan = st.sidebar.button("SCAN NOW", type="primary", use_container_width=True)

STOCKS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","SUNDRMFAST.NS","TATAMOTORS.NS"]

if scan:
    results = []
    bar = st.progress(0)
    for i, sym in enumerate(STOCKS):
        try:
            data = get_data(sym)
            if data is None: continue
            last = data.iloc[-1]
            if last['Signal'] == "BUY":
                price = float(last['Close'])
                results.append({
                    "SYMBOL": sym.replace(".NS",""),
                    "LTP": round(price,2),
                    "ENTRY": round(price,2),
                    "SL": round(price*0.985,2),
                    "T1": round(price*1.02,2),
                    "T2": round(price*1.04,2),
                    "RSI": round(float(last['RSI']),1),
                    "SIGNAL": "BUY"
                })
        except:
            pass
        bar.progress((i+1)/len(STOCKS))
    bar.empty()
    
    if results:
        df = pd.DataFrame(results)
        st.success(f"{len(results)} BUY Signals Found!")
        st.dataframe(df, use_container_width=True, hide_index=True)
        for r in results:
            st.markdown(f"<div style='border:2px solid #00ff00;padding:12px;border-radius:10px;margin:8px 0;background:#111;'><b style='color:white;'>{r['SYMBOL']} - {r['SIGNAL']}</b> | LTP Rs {r['LTP']}<br>ENTRY Rs {r['ENTRY']} | SL Rs {r['SL']} | T1 Rs {r['T1']} | T2 Rs {r['T2']}<br>RSI {r['RSI']}</div>", unsafe_allow_html=True)
    else:
        st.warning("No BUY signal now - Scan after 9:45 AM")
else:
    st.info("Left se SCAN NOW dabao")
    st.components.v1.iframe("https://s.tradingview.com/widgetembed/?symbol=NSE%3ASUNDRMFAST&interval=15", height=500)
