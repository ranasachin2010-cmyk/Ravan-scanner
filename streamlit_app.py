import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="RAVAN 2.0", page_icon="👺", layout="wide")
st.markdown("<h1 style='text-align:center;color:#ff3300;'>👺 RAVAN 2.0 - LIVE SCANNER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>EMA 21 | RSI 55 | EMA50 - 9:45 AM Setup</p>", unsafe_allow_html=True)

def get_data(symbol):
    try:
        df = yf.download(symbol, period="5d", interval="15m", progress=False)
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
        return df.dropna()
    except:
        return None

st.sidebar.title("Ravan Scanner")
scan = st.sidebar.button("🔍 SCAN NOW", type="primary", use_container_width=True)

STOCKS = ["RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS","ICICIBANK.NS","SBIN.NS","SUNDRMFAST.NS","TATAMOTORS.NS","WIPRO.NS","BHARTIARTL.NS"]

if scan:
    results = []
    bar = st.progress(0)
    for i, sym in enumerate(STOCKS):
        data = get_data(sym)
        if data is not None:
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
                    "SIGNAL": "🔥 BUY"
                })
        bar.progress((i+1)/len(STOCKS))
    bar.empty()
    if results:
        st.success(f"🔥 {len(results)} BUY Signals Found!")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Abhi koi fresh BUY signal nahi - 9:45 AM ke baad scan karo")

# --- PERFECT CHART - FIXED SCALE ---
st.markdown("---")
st.subheader("📈 NSE Live Chart - 15 Min")

symbol = st.selectbox("Stock Select Karo:", ["RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","SUNDRMFAST","TATAMOTORS","BHARTIARTL","WIPRO"], key="chart_select")
st.caption(f"Showing: NSE:{symbol} | 100% NSE Data | No Apple Bug")

df_chart = get_data(f"{symbol}.NS")

if df_chart is not None:
    last = df_chart.iloc[-1]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("LTP", f"Rs {float(last['Close']):.2f}")
    c2.metric("EMA21", f"{float(last['EMA21']):.2f}")
    c3.metric("EMA50", f"{float(last['EMA50']):.2f}")
    c4.metric("RSI", f"{float(last['RSI']):.1f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'], name="Close", line=dict(color="#00ff00", width=2)))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA21'], name="EMA21", line=dict(color="orange", width=1.5)))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA50'], name="EMA50", line=dict(color="#ff3300", width=1.5)))
    
    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Time",
        yaxis_title="Price (Rs)",
        hovermode="x unified",
        margin=dict(l=10,r=10,t=10,b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📊 Last 5 Candles"):
        st.dataframe(df_chart[['Close','EMA21','EMA50','RSI','Signal']].tail(5).sort_index(ascending=False), use_container_width=True)
else:
    st.error("Data load nahi hua")

# Requirements ke liye
st.markdown("<p style='text-align:center;color:gray;margin-top:30px;'>RAVAN 2.0 | 100% NSE Data</p>", unsafe_allow_html=True)
