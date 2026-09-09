import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import requests
from io import BytesIO

st.set_page_config(page_title="HANUMAN SCANNER 500 LIVE", page_icon="🚩", layout="wide")
st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)
st.markdown("""<style>[data-testid="stElementToolbar"]{display:none!important}.stActionButton{display:none!important}header{visibility:hidden}</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - LIVE NSE 500</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE DATA | NIFTY 500 | AUTO REFRESH 5 MIN</b></p>", unsafe_allow_html=True)

NIFTY_500 = ["RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","BHARTIARTL","ITC","SBIN","LT","BAJFINANCE","HINDUNILVR","KOTAKBANK","HCLTECH","SUNPHARMA","MARUTI","M&M","AXISBANK","ULTRACEMCO","NTPC","ONGC","TITAN","WIPRO","ADANIENT","POWERGRID","ASIANPAINT","NESTLEIND","TATAMOTORS","BAJAJFINSV","JSWSTEEL","HINDALCO","ADANIPORTS","COALINDIA","CIPLA","GRASIM","DIVISLAB","DRREDDY","EICHERMOT","BRITANNIA","BPCL","SBILIFE","HDFCLIFE","TECHM","INDUSINDBK","APOLLOHOSP","TATASTEEL","BAJAJ-AUTO","HEROMOTOCO","SHRIRAMFIN","ADANIGREEN","VEDL","ZOMATO","SIEMENS","HAL","BEL","TRENT","PIDILITIND","LTIM","DLF","GODREJCP","HAVELLS","ICICIGI","INFOEDGE","INDIGO","AMBUJACEM","BANKBARODA","BERGEPAINT","BOSCHLTD","CANBK","CHOLAFIN","DABUR","GAIL","GODREJPROP","HDFCAMC","HINDPETRO","INDHOTEL","IOC","IRCTC","JINDALSTEL","JSWENERGY","JUBLFOOD","LUPIN","MUTHOOTFIN","NMDC","OBEROIRLTY","PFC","PNB","RECLTD","SAIL","SHREECEM","SRF","TATACONSUM","TATAPOWER","TORNTPHARM","UPL","VOLTAS","ZEEL","ACC","ALKEM","ASHOKLEY","AUROPHARMA","BANDHANBNK","BATAINDIA","BHARATFORG","BIOCON","CGPOWER","COLPAL","CONCOR","CUMMINSIND","FEDERALBNK","GMRINFRA","GUJGASLTD","HINDZINC","IDFCFIRSTB","IGL","INDIAMART","IPCALAB","LAURUSLABS","MARICO","MOTHERSON","MPHASIS","MRF","PAGEIND","PEL","PERSISTENT","PETRONET","PIIND","POLYCAB","PVRINOX","RAMCOCEM","RBLBANK","TATACHEM","TATACOMM","TORNTPOWER","TVSMOTOR","UBL","VBL","ABB","ABCAPITAL","ABFRL","AARTIIND","AIAENG","AJANTPHARM","APLAPOLLO","AUBANK","BALKRISIND","BEML","BHEL","BSOFT","CAMS","CDSL","CESC","COROMANDEL","CRISIL","CROMPTON","DALBHARAT","EXIDEIND","FSL","FORTIS","GNFC","GRINDWELL","HAPPSTMNDS","HUDCO","IDFC","IEX","IRFC","JSL","JSWINFRA","KAJARIACER","KEI","KPITTECH","LALPATHLAB","LTF","LTTS","MCX","METROPOLIS","MGL","NCC","NHPC","OIL","PAYTM","POLYMED","POONAWALLA","PRESTIGE","RATNAMANI","RAYMOND","SBICARD","SJVN","SONACOMS","SUNDRMFAST","SUPREMEIND","SYNGENE","TATAELXSI","TIINDIA","TRIDENT","UJJIVANSFB","VGUARD","WELCORP","ZYDUSLIFE","AFFLE","ANGELONE","ASTERDM","ATUL","BDL","BLUESTARCO","CENTRALBK","COFORGE","DELHIVERY","EIHOTEL","ELGIEQUIP","GICRE","GLAXO","GSPL","HBLPOWER","IDBI","IIFL","IRB","JBCHEPHARM","JKCEMENT","KARURVYSYA","KIMS","MASTEK","MAZDOCK","MOTILALOFS","NYKAA","OLECTRA","PATANJALI","PNBHOUSING","RADICO","RITES","SOBHA","SOLARINDS","STARHEALTH","SUVENPHAR","TANLA","TEAMLEASE","UCOBANK","UNIONBANK","VAIBHAVGBL","WELSPUNLIV","ZYDUSWELL"]

NIFTY_500 = list(dict.fromkeys(NIFTY_500))[:500]

def get_data(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="5d", interval="15m", progress=False, auto_adjust=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        if len(df) < 50: return None
        df['EMA21'] = df['Close'].ewm(span=21).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df = df.dropna()
        last = df.iloc[-1]
        is_buy = (float(last['Close']) > float(last['EMA21'])) and (float(last['EMA21']) > float(last['EMA50'])) and (float(last['RSI']) > 55)
        return {"df": df, "last": last, "is_buy": is_buy, "symbol": symbol}
    except: return None

def send_telegram(token, chat_id, msg):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
        return True
    except: return False

# SIDEBAR
st.sidebar.title("🚩 Hanuman Scanner")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● NSE LIVE 500 | Auto 5 Min")

st.sidebar.markdown("---")
st.sidebar.subheader("📲 Telegram Alert")
bot_token = st.sidebar.text_input("Bot Token", type="password", placeholder="1234:AAH...")
chat_id = st.sidebar.text_input("Chat ID", placeholder="123456789")
enable_tele = st.sidebar.checkbox("Telegram ON")

scan = st.sidebar.button("🔍 LIVE SCAN 500 NOW", type="primary", use_container_width=True)

if scan:
    results = []
    bar = st.progress(0)
    status = st.empty()
    with ThreadPoolExecutor(max_workers=30) as ex:
        for i, res in enumerate(ex.map(get_data, NIFTY_500)):
            if res and res['is_buy']:
                last = res['last']; price = float(last['Close'])
                results.append({"SYMBOL": res['symbol'],"LTP": round(price,2),"ENTRY": round(price,2),"SL": round(price*0.985,2),"T1": round(price*1.02,2),"T2": round(price*1.04,2),"RSI": round(float(last['RSI']),1),"SIGNAL": "🚩 BUY"})
            bar.progress((i+1)/len(NIFTY_500))
            status.text(f"Scanning {i+1}/{len(NIFTY_500)} | BUY: {len(results)}")
    bar.empty(); status.empty()
    
    if results:
        df = pd.DataFrame(results)
        st.success(f"🚩 {len(results)} BUY Signals Found in {len(NIFTY_500)} Stocks!")
        
        # 3. COLOR STYLING
        def color_rsi(val):
            if val >= 70: color = '#00ff00'
            elif val >= 60: color = '#90EE90'
            elif val >= 55: color = '#FFFF00'
            else: color = ''
            return f'background-color: {color}; color: black; font-weight: bold'

        def style_df(df):
            return df.style.applymap(lambda x: 'background-color: #ff4d4d; color: white; font-weight: bold', subset=['SL'])\
                         .applymap(lambda x: 'background-color: #00cc66; color: white; font-weight: bold', subset=['T1','T2'])\
                         .applymap(color_rsi, subset=['RSI'])

        st.dataframe(style_df(df), use_container_width=True, hide_index=True)

        # 1. DOWNLOAD BUTTONS
        col1, col2 = st.columns(2)
        csv = df.to_csv(index=False).encode('utf-8')
        col1.download_button("📥 Download CSV", csv, "hanuman_500_buy.csv", "text/csv", use_container_width=True)
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='BUY Signals')
        excel_data = output.getvalue()
        col2.download_button("📊 Download Excel", excel_data, "hanuman_500_buy.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

        # 2. TELEGRAM ALERT
        if enable_tele and bot_token and chat_id:
            msg = f"🚩 *HANUMAN SCANNER - {len(results)} BUY SIGNALS*\n\n"
            for r in results[:15]: # Top 15 bhejenge telegram pe
                msg += f"*{r['SYMBOL']}* - LTP {r['LTP']} | SL {r['SL']} | T1 {r['T1']} | RSI {r['RSI']}\n"
            if len(results) > 15:
                msg += f"\n...and {len(results)-15} more. Check App!"
            if send_telegram(bot_token, chat_id, msg):
                st.sidebar.success("Telegram Sent! ✅")
            else:
                st.sidebar.error("Telegram Failed!")
        elif enable_tele:
            st.sidebar.warning("Bot Token / Chat ID dalo!")

    else: 
        st.warning("⚠️ Abhi koi BUY nahi")
else:
    st.info(f"👈 SCAN NOW dabao - {len(NIFTY_500)} stocks LIVE scan | Auto Refresh 5 min ON hai")

st.markdown("---")
st.subheader("📈 LIVE Chart")
symbol = st.selectbox("Stock Select:", NIFTY_500[:100], key="chart_select")
live = get_data(symbol)
if live:
    df_chart = live['df']; last = live['last']
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("LTP", f"Rs {float(last['Close']):.2f}"); c2.metric("EMA21", f"{float(last['EMA21']):.2f}")
    c3.metric("EMA50", f"{float(last['EMA50']):.2f}"); c4.metric("RSI", f"{float(last['RSI']):.1f}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'], name="Close", line=dict(color="#00ff00", width=2)))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA21'], name="EMA21", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA50'], name="EMA50", line=dict(color="red")))
    fig.update_layout(template="plotly_dark", height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False})
