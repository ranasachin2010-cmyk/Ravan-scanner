import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from nsepython import nse_eq, nse_get_fno_lot
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import time

st.set_page_config(page_title="HANUMAN SCANNER LIVE NSE", page_icon="🚩", layout="wide")
st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - LIVE NSE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE DATA | REAL-TIME | 100% Ravan Clone</b></p>", unsafe_allow_html=True)

# NIFTY 500 - Unique list
NIFTY_500_RAW = [
"RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","BHARTIARTL","ITC","SBIN","LT","BAJFINANCE",
"HINDUNILVR","KOTAKBANK","HCLTECH","SUNPHARMA","MARUTI","M&M","AXISBANK","ULTRACEMCO","NTPC","ONGC",
"TITAN","WIPRO","ADANIENT","POWERGRID","ASIANPAINT","NESTLEIND","TATAMOTORS","BAJAJFINSV","JSWSTEEL","HINDALCO",
"ADANIPORTS","COALINDIA","CIPLA","GRASIM","DIVISLAB","DRREDDY","EICHERMOT","BRITANNIA","BPCL","SBILIFE",
"HDFCLIFE","TECHM","INDUSINDBK","APOLLOHOSP","TATASTEEL","BAJAJ-AUTO","HEROMOTOCO","SHRIRAMFIN","ADANIGREEN","VEDL",
"ZOMATO","SIEMENS","HAL","BEL","TRENT","PIDILITIND","LTIM","DLF","GODREJCP","HAVELLS",
"ICICIGI","INFOEDGE","INDIGO","AMBUJACEM","BANKBARODA","BERGEPAINT","BOSCHLTD","CANBK","CHOLAFIN","DABUR",
"GAIL","GODREJPROP","HDFCAMC","HINDPETRO","INDHOTEL","IOC","IRCTC","JINDALSTEL","JSWENERGY","JUBLFOOD",
"LUPIN","MUTHOOTFIN","NMDC","OBEROIRLTY","PFC","PNB","RECLTD","SAIL","SHREECEM","SRF",
"TATACONSUM","TATAPOWER","TORNTPHARM","UPL","VOLTAS","ZEEL","ACC","ALKEM","ASHOKLEY","AUROPHARMA",
"BANDHANBNK","BATAINDIA","BHARATFORG","BIOCON","CGPOWER","COLPAL","CONCOR","CUMMINSIND","FEDERALBNK","GMRINFRA",
"GUJGASLTD","HINDZINC","IDFCFIRSTB","IGL","INDIAMART","IPCALAB","LAURUSLABS","MARICO","MOTHERSON","MPHASIS",
"MRF","PAGEIND","PEL","PERSISTENT","PETRONET","PIIND","POLYCAB","PVRINOX","RAMCOCEM","RBLBANK",
"TATACHEM","TATACOMM","TORNTPOWER","TVSMOTOR","UBL","VBL","ABB","ABCAPITAL","ABFRL","AARTIIND",
"AIAENG","AJANTPHARM","APLAPOLLO","AUBANK","BALKRISIND","BEML","BHEL","BSOFT","CAMS","CDSL",
"CESC","COROMANDEL","CRISIL","CROMPTON","DALBHARAT","EXIDEIND","FSL","FORTIS","GNFC","GRINDWELL",
"HAPPSTMNDS","HUDCO","IDFC","IEX","IRFC","JSL","JSWINFRA","KAJARIACER","KEI","KPITTECH",
"LALPATHLAB","LTF","LTTS","MCX","METROPOLIS","MGL","NCC","NHPC","OIL","PAYTM",
"POLYMED","POONAWALLA","PRESTIGE","RATNAMANI","RAYMOND","SBICARD","SJVN","SONACOMS","SUNDRMFAST","SUPREMEIND",
"SYNGENE","TATAELXSI","TIINDIA","TRIDENT","UJJIVANSFB","VGUARD","WELCORP","ZYDUSLIFE","AFFLE","ANGELONE"
]
NIFTY_500 = list(dict.fromkeys(NIFTY_500_RAW)) # duplicate hatao

def get_live_data(symbol):
    try:
        # 15min EMA RSI ke liye yfinance history
        df = yf.download(f"{symbol}.NS", period="5d", interval="15m", progress=False)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        if len(df) < 50:
            return None
        
        # LIVE LTP ke liye NSE
        try:
            nse_data = nse_eq(symbol)
            live_ltp = float(nse_data['priceInfo']['lastPrice'])
            df.iloc[-1, df.columns.get_loc('Close')] = live_ltp # last candle ko live se update
        except:
            live_ltp = float(df['Close'].iloc[-1])

        df['EMA21'] = df['Close'].ewm(span=21).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df = df.dropna()
        
        last = df.iloc[-1]
        is_buy = (last['Close'] > last['EMA21']) and (last['EMA21'] > last['EMA50']) and (last['RSI'] > 55)
        
        return {
            "df": df,
            "ltp": live_ltp,
            "ema21": float(last['EMA21']),
            "ema50": float(last['EMA50']),
            "rsi": float(last['RSI']),
            "is_buy": is_buy,
            "symbol": symbol
        }
    except:
        return None

st.sidebar.title("🚩 Hanuman Live NSE")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● LIVE NSE Connected")
scan = st.sidebar.button("🔍 LIVE SCAN NOW", type="primary", use_container_width=True)

if scan:
    results = []
    bar = st.progress(0)
    status = st.empty()
    
    def scan_one(sym):
        return get_live_data(sym)

    with ThreadPoolExecutor(max_workers=30) as ex:
        for i, res in enumerate(ex.map(scan_one, NIFTY_500)):
            if res and res['is_buy']:
                price = res['ltp']
                results.append({
                    "SYMBOL": res['symbol'],
                    "LTP": round(price,2),
                    "ENTRY": round(price,2),
                    "SL": round(price*0.985,2),
                    "T1": round(price*1.02,2),
                    "T2": round(price*1.04,2),
                    "RSI": round(res['rsi'],1),
                    "EMA21": round(res['ema21'],1),
                    "SIGNAL": "🚩 BUY"
                })
            bar.progress((i+1)/len(NIFTY_500))
            status.text(f"Scanning {i+1}/{len(NIFTY_500)} | LIVE BUY: {len(results)}")
    
    bar.empty()
    status.empty()
    
    if results:
        st.balloons()
        st.success(f"🚩 {len(results)} LIVE BUY Signals Found! - Real NSE Data")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        for r in results[:15]:
            st.markdown(f"<div style='border:2px solid #00ff00;padding:10px;border-radius:10px;margin:5px 0;background:#111;'><b style='color:white;'>{r['SYMBOL']} - LIVE {r['SIGNAL']}</b> <span style='float:right;color:#00ff00;'>Rs {r['LTP']}</span><br>ENTRY {r['ENTRY']} | SL <span style='color:#ff4444;'>{r['SL']}</span> | T1 {r['T1']} | T2 {r['T2']} | RSI {r['RSI']}</div>", unsafe_allow_html=True)
    else:
        st.warning("⚠️ Live scan me abhi koi BUY nahi - Market 9:45 AM ke baad check karo")

else:
    st.info(f"👈 LIVE SCAN NOW dabao - {len(NIFTY_500)} stocks ka LIVE NSE data ayega!")

# Live Chart
st.markdown("---")
st.subheader("📈 LIVE NSE Chart - 15 Min + LIVE Price")
symbol = st.selectbox("Stock Select:", NIFTY_500[:100], key="chart_select")
live = get_live_data(symbol)
if live:
    df_chart = live['df']
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("LIVE LTP", f"Rs {live['ltp']:.2f}", delta=f"{live['ltp']-float(df_chart['Close'].iloc[-2]):.2f}")
    c2.metric("EMA21", f"{live['ema21']:.2f}")
    c3.metric("EMA50", f"{live['ema50']:.2f}")
    c4.metric("RSI", f"{live['rsi']:.1f}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'], name="Close LIVE", line=dict(color="#00ff00", width=2)))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA21'], name="EMA21", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA50'], name="EMA50", line=dict(color="red")))
    fig.update_layout(template="plotly_dark", height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Last Update: {pd.Timestamp.now().strftime('%d-%m-%Y %H:%M:%S')} IST - LIVE NSE")

st.markdown("<p style='text-align:center;color:gray;'>🚩 HANUMAN SCANNER LIVE NSE | 100% Ravan Clone | Jai Shri Ram</p>", unsafe_allow_html=True)
