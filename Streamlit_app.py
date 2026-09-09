import streamlit as st, yfinance as yf, pandas as pd, numpy as np

st.set_page_config(page_title="RAVAN 2.0 SCREENER", layout="wide")
st.markdown("<h1 style='text-align:center;color:#ff3300;'>👺 RAVAN 2.0 SCREENER - 9:45 BUY</h1>", unsafe_allow_html=True)

# --- CONFIG ---
def get_signals(df):
    df['EMA21'] = df['Close'].ewm(span=21).mean()
    df['EMA50'] = df['Close'].ewm(span=50).mean()
    df['RSI'] = 100 - (100 / (1 + df['Close'].diff().clip(lower=0).rolling(14).mean() / df['Close'].diff().clip(upper=0).abs().rolling(14).mean()))
    # SuperTrend logic simplified
    df['Signal'] = np.where((df['Close'] > df['EMA21']) & (df['EMA21'] > df['EMA50']) & (df['RSI']>55), "BUY", "SELL")
    return df

# --- SCREENER ---
st.sidebar.header("⚙️ Scanner Setting")
scan_btn = st.sidebar.button("🔍 SCAN NIFTY 50", type="primary")

if scan_btn:
    symbols = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SUNDRMFAST.NS","SBIN.NS","BHARTIARTL.NS"]
    results = []
    progress = st.progress(0)
    for i, sym in enumerate(symbols):
        try:
            data = yf.download(sym, period="5d", interval="15m", progress=False)
            data = get_signals(data)
            last = data.iloc[-1]
            if last['Signal']=="BUY":
                results.append({
                    "Symbol": sym.replace(".NS",""),
                    "Price": round(float(last['Close']),2),
                    "ENTRY": round(float(last['Close']),2),
                    "SL": round(float(last['Close']*0.98),2),
                    "TARGET": round(float(last['Close']*1.03),2),
                    "RSI": round(float(last['RSI']),1),
                    "Signal": "🔥 BUY"
                })
        except: pass
        progress.progress((i+1)/len(symbols))
    
    df_res = pd.DataFrame(results)
    if not df_res.empty:
        st.dataframe(df_res, use_container_width=True)
        # Ravan Card Design
        for r in results:
            st.markdown(f"""
            <div style='border:2px solid #00ff00;padding:15px;border-radius:15px;margin:10px;background:#0a0a0a;'>
                <h3 style='color:white;'>{r['Symbol']} - {r['Signal']}</h3>
                <p style='color:#aaa;'>ENTRY: <b style='color:white;'>Rs{r['ENTRY']}</b> | SL: <span style='color:red;'>Rs{r['SL']}</span> | TARGET: <span style='color:#00ff00;'>Rs{r['TARGET']} +3%</span></p>
                <p style='color:gold;'>RSI: {r['RSI']} | EMA21 > EMA50 CONFIRMED</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Abhi koi BUY signal nahi hai - 9:45 ke baad scan karo")

# --- CHART ---
st.markdown("---")
tv = "https://s.tradingview.com/widgetembed/?symbol=NSE%3ASUNDRMFAST&interval=15"
st.html(f'<iframe src="{tv}" height="600" width="100%"></iframe>')
