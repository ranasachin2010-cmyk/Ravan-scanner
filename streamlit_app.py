import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import requests
from io import BytesIO, StringIO

st.set_page_config(page_title="HANUMAN SCANNER 500 LIVE", page_icon="🚩", layout="wide")
st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - LIVE NSE 500</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE DATA | NIFTY 500 | AUTO REFRESH 5 MIN</b></p>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def get_nifty500_official():
    try:
        url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        df_csv = pd.read_csv(StringIO(r.text))
        col = None
        for c in df_csv.columns:
            if 'Symbol' in c or 'SYMBOL' in c.upper():
                col = c
                break
        if col is None: col = df_csv.columns[2]
        symbols = [str(x).strip().upper() for x in df_csv[col].tolist() if str(x).strip()!= '']
        symbols = list(dict.fromkeys(symbols))[:500]
        if len(symbols) >= 400: return symbols
    except: pass
    return ["RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","BHARTIARTL","ITC","SBIN","LT","BAJFINANCE","HINDUNILVR","KOTAKBANK","HCLTECH","SUNPHARMA","MARUTI","M&M","AXISBANK","ULTRACEMCO","NTPC","ONGC","TITAN","WIPRO","ADANIENT","POWERGRID","ASIANPAINT","NESTLEIND","TATAMOTORS","BAJAJFINSV","JSWSTEEL","HINDALCO","ADANIPORTS","COALINDIA","CIPLA","GRASIM","DIVISLAB","DRREDDY","EICHERMOT","BRITANNIA","BPCL","SBILIFE","HDFCLIFE","TECHM","INDUSINDBK","APOLLOHOSP","TATASTEEL","BAJAJ-AUTO","HEROMOTOCO","SHRIRAMFIN","ADANIGREEN","VEDL","ZOMATO","SIEMENS","HAL","BEL","TRENT","PIDILITIND","LTIM","DLF","GODREJCP","HAVELLS","ICICIGI","INFOEDGE","INDIGO"]*5

NIFTY_500 = get_nifty500_official()
NIFTY_500 = list(dict.fromkeys(NIFTY_500))[:500]
if len(NIFTY_500) < 500:
    extra = ["360ONE","3MINDIA","AARTIIND","ABFRL","ABBOTINDIA","ADANIENSOL","ATGL","AWL","ABSLAMC","AMBER","ANURAS","APARINDS","APOLLOTYRE","APTUS","ASTRAL","BLS","BSE","BAJAJELEC","BBTC","BIKAJI","BLUEDART","BRIGADE","CCL","CAMPUS","CEATLTD","CERA","CHALET","CLEAN","COCHINSHIP","CRAFTSMAN","CYIENT","DCBBANK","DATAPATTNS","DEEPAKFERT","DELTACORP","DEVYANI","DIXON","EIDPARRY","EPL","FDC","FINEORG","GALAXYSURF","GRSE","GILLETTE","GLAND","GODREJIND","GRANULES","HATHWAY","HATSUN","HFCL","HOMEFIRST","IDBI","IIFL","IRCON","ITI","INDIACEM","IOLCP","JKTYRE","JWL","JUSTDIAL","KPRMILL","KRBL","KSB","KAYNES","LICI","LAXMIMACH","LEMONTREE","MMTC","M&MFIN","MANAPPURAM","MRPL","MFSL","MEDPLUS","MINDACORP","MOIL","NATCOPHARM","NBCC","NESCO","NH","PFIZER","PHOENIXLTD","PRAJIND","RELAXO","RAILTEL","RVNL","RALLIS","RKFORGE","RCF","REDINGTON","SANOFI","SAPPHIRE","SAREGAMA","SKFINDIA","SUNTV","SUZLON","TTKPRESTIG","TATVA","TEJASNET","THERMAX","TIMKEN","MCDOWELL-N","VIPIND","YESBANK","ZENSARTECH"]
    for s in extra:
        if s not in NIFTY_500 and len(NIFTY_500) < 500: NIFTY_500.append(s)

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

def send_telegram_msg(token, chat_id, msg):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=10)
        return True
    except: return False

def send_telegram_file(token, chat_id, file_bytes, filename, caption=""):
    try:
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        files = {'document': (filename, file_bytes)}
        data = {'chat_id': chat_id, 'caption': caption}
        requests.post(url, data=data, files=files, timeout=20)
        return True
    except: return False

st.sidebar.title("🚩 Hanuman Scanner")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● NSE LIVE 500 | Auto 5 Min")
st.sidebar.markdown("---")
st.sidebar.subheader("📲 Telegram Alert")
bot_token = st.sidebar.text_input("Bot Token", type="password")
chat_id = st.sidebar.text_input("Chat ID")
enable_tele = st.sidebar.checkbox("Telegram ON + File")
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
        styled = df.style.format({"LTP": "{:.2f}", "ENTRY": "{:.2f}", "SL": "{:.2f}", "T1": "{:.2f}", "T2": "{:.2f}", "RSI": "{:.1f}"})\
                        .map(lambda x: 'background-color: #ff4d4d; color: white; font-weight: bold', subset=['SL'])\
                        .map(lambda x: 'background-color: #00cc66; color: white; font-weight: bold', subset=['T1','T2'])\
                        .map(lambda v: 'background-color: #90EE90; color: black; font-weight: bold' if v>=60 else 'background-color: yellow; color: black' if v>=55 else '', subset=['RSI'])
        st.dataframe(styled, use_container_width=True, hide_index=True)

        c1, c2 = st.columns(2)
        csv_data = df.to_csv(index=False).encode('utf-8')
        c1.download_button("📥 Download CSV", csv_data, "hanuman_500_buy.csv", "text/csv", use_container_width=True)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='BUY Signals')
        excel_data = output.getvalue()
        c2.download_button("📊 Download Excel", excel_data, "hanuman_500_buy.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)

        # TELEGRAM - MESSAGE + FILE
        if enable_tele and bot_token and chat_id:
            # 1. Pehle summary message
            msg = f"🚩 *HANUMAN SCANNER - {len(results)} BUY*\n_NIFTY 500 SCAN_\n\n"
            for r in results[:20]: # Telegram limit ke liye 20
                msg += f"*{r['SYMBOL']}* LTP {r['LTP']:.2f} SL {r['SL']:.2f} T1 {r['T1']:.2f} RSI {r['RSI']}\n"
            if len(results) > 20:
                msg += f"\n...and {len(results)-20} more. Full file attached 👇"
            send_telegram_msg(bot_token, chat_id, msg)

            # 2. Ab poori file bhejo
            caption = f"🚩 HANUMAN 500 - Full {len(results)} BUY List - {pd.Timestamp.now().strftime('%d-%m-%Y %H:%M')}"
            send_telegram_file(bot_token, chat_id, excel_data, f"Hanuman_500_BUY_{len(results)}.xlsx", caption)
            st.sidebar.success(f"Telegram pe {len(results)} ka full file gaya! ✅")
    else:
        st.warning("⚠️ Abhi koi BUY nahi")
else:
    st.info(f"👈 SCAN NOW dabao - {len(NIFTY_500)} stocks scan")

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
    st.plotly_chart(fig, use_container_width=True)
