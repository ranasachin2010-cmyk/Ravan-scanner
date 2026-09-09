import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor
import requests
from io import BytesIO, StringIO

st.set_page_config(page_title="HANUMAN SCANNER 500 FINAL", page_icon="🚩", layout="wide")
st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - FINAL 500 + WIN %</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE 500 | COLOR TABLE | TELEGRAM FILE | WIN %</b></p>", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def get_nifty500_official():
    try:
        url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        df_csv = pd.read_csv(StringIO(r.text))
        col = None
        for c in df_csv.columns:
            if 'SYMBOL' in c.upper():
                col = c
                break
        if col is None: col = df_csv.columns[2]
        symbols = [str(x).strip().upper() for x in df_csv[col].tolist() if str(x).strip()!='']
        symbols = list(dict.fromkeys(symbols))[:500]
        if len(symbols) >= 400: return symbols
    except: pass
    return ["RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","BHARTIARTL","ITC","SBIN","LT","BAJFINANCE","HINDUNILVR","KOTAKBANK","HCLTECH","SUNPHARMA","MARUTI","M&M","AXISBANK","ULTRACEMCO","NTPC","ONGC","TITAN","WIPRO","ADANIENT","POWERGRID","ASIANPAINT","NESTLEIND","TATAMOTORS","BAJAJFINSV","JSWSTEEL","HINDALCO","ADANIPORTS","COALINDIA","CIPLA","GRASIM","DIVISLAB","DRREDDY","EICHERMOT","BRITANNIA","BPCL","SBILIFE","HDFCLIFE","TECHM","INDUSINDBK","APOLLOHOSP","TATASTEEL","BAJAJ-AUTO","HEROMOTOCO","SHRIRAMFIN","ADANIGREEN","VEDL","ZOMATO","SIEMENS","HAL","BEL","TRENT","PIDILITIND","LTIM","DLF","GODREJCP","HAVELLS","ICICIGI","INFOEDGE","INDIGO","360ONE","3MINDIA","AARTIIND","ABFRL","ABBOTINDIA","ADANIENSOL","ATGL","AWL","ABSLAMC","AMBER","ANURAS","APARINDS","APOLLOTYRE","APTUS","ASTRAL","BLS","BSE","BAJAJELEC","BBTC","BIKAJI","BLUEDART","BRIGADE","CCL","CAMPUS","CEATLTD","CERA","CHALET","CLEAN","COCHINSHIP","CRAFTSMAN","CYIENT","DCBBANK","DATAPATTNS","DEEPAKFERT","DELTACORP","DEVYANI","DIXON","EIDPARRY","EPL","FDC","FINEORG","GALAXYSURF","GRSE","GILLETTE","GLAND","GODREJIND","GRANULES","HATHWAY","HATSUN","HFCL","HOMEFIRST","IDBI","IIFL","IRCON","ITI","INDIACEM","IOLCP","JKTYRE","JWL","JUSTDIAL","KPRMILL","KRBL","KSB","KAYNES","LICI","LAXMIMACH","LEMONTREE","MMTC","M&MFIN","MANAPPURAM","MRPL","MFSL","MEDPLUS","MINDACORP","MOIL","NATCOPHARM","NBCC","NESCO","NH","PFIZER","PHOENIXLTD","PRAJIND","RELAXO","RAILTEL","RVNL","RALLIS","RKFORGE","RCF","REDINGTON","SANOFI","SAPPHIRE","SAREGAMA","SKFINDIA","SUNTV","SUZLON","TTKPRESTIG","TATVA","TEJASNET","THERMAX","TIMKEN","MCDOWELL-N","VIPIND","YESBANK","ZENSARTECH"]

NIFTY_500 = get_nifty500_official()
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
        df['RSI'] = 100 - (100 / (1 + gain/loss))
        df = df.dropna()
        last = df.iloc[-1]
        is_buy = (float(last['Close']) > float(last['EMA21'])) and (float(last['EMA21']) > float(last['EMA50'])) and (float(last['RSI']) > 55)
        return {"df": df, "last": last, "is_buy": is_buy, "symbol": symbol}
    except: return None

def backtest_win(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="3mo", interval="1d", progress=False, auto_adjust=False)
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        if len(df) < 60: return None
        df['EMA21'] = df['Close'].ewm(span=21).mean()
        df['EMA50'] = df['Close'].ewm(span=50).mean()
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = -delta.where(delta < 0, 0).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + gain/loss))
        df = df.dropna()
        wins = 0; total = 0
        for i in range(len(df)-35, len(df)-5):
            if i < 0: continue
            if df['Close'].iloc[i] > df['EMA21'].iloc[i] and df['EMA21'].iloc[i] > df['EMA50'].iloc[i] and df['RSI'].iloc[i] > 55:
                total += 1
                entry = float(df['Close'].iloc[i])
                sl = entry * 0.985
                t1 = entry * 1.02
                future = df.iloc[i+1:i+11]
                for _, row in future.iterrows():
                    if float(row['High']) >= t1:
                        wins += 1
                        break
                    if float(row['Low']) <= sl:
                        break
        if total == 0: return None
        return {"symbol": symbol, "total": total, "wins": wins, "win_pct": round(wins/total*100,1)}
    except: return None

def send_telegram_msg(token, chat_id, msg):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except: pass

def send_telegram_file(token, chat_id, file_bytes, filename, caption=""):
    try:
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        files = {'document': (filename, file_bytes)}
        data = {'chat_id': chat_id, 'caption': caption}
        requests.post(url, data=data, files=files, timeout=20)
    except: pass

st.sidebar.title("🚩 Control Panel")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● NSE LIVE 500 LOCKED")
st.sidebar.markdown("---")
st.sidebar.subheader("📲 Telegram Alert")
bot_token = st.sidebar.text_input("Bot Token", type="password")
chat_id = st.sidebar.text_input("Chat ID")
enable_tele = st.sidebar.checkbox("Telegram ON + Full File")
scan = st.sidebar.button("🔍 SCAN 500 NOW", type="primary", use_container_width=True)
calc_win = st.sidebar.button("📊 WIN % BACKTEST", use_container_width=True)

if calc_win:
    st.subheader("📊 WIN % BACKTEST - Last 3 Months (100 Stocks Sample)")
    with st.spinner("Backtest chal raha hai... 100 stocks..."):
        sample = NIFTY_500[:100]
        results = []
        bar = st.progress(0)
        with ThreadPoolExecutor(max_workers=20) as ex:
            for i, r in enumerate(ex.map(backtest_win, sample)):
                if r: results.append(r)
                bar.progress((i+1)/len(sample))
        bar.empty()
        if results:
            df_win = pd.DataFrame(results)
            avg_win = df_win['win_pct'].mean()
            c1,c2,c3 = st.columns(3)
            c1.metric("Avg WIN %", f"{avg_win:.1f}%")
            c2.metric("Total Signals", f"{df_win['total'].sum()}")
            c3.metric("Total Wins", f"{df_win['wins'].sum()}")
            st.dataframe(df_win.sort_values("win_pct", ascending=False).style.format({"win_pct": "{:.1f}%"}).background_gradient(subset=['win_pct'], cmap='Greens'), use_container_width=True, hide_index=True)
            if avg_win >= 65: st.success(f"🔥 RAVAN SE BETTER! Aapka {avg_win:.1f}% vs Ravan ~60-65%")
            elif avg_win >= 55: st.info(f"✅ RAVAN KE BARABAR! Aapka {avg_win:.1f}% - Solid!")
            else: st.warning(f"⚠️ Market down, {avg_win:.1f}% - Bull me 65%+ jayega")

if scan:
    results = []
    bar = st.progress(0); status = st.empty()
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
        if enable_tele and bot_token and chat_id:
            msg = f"🚩 *HANUMAN SCANNER - {len(results)} BUY*\n_NIFTY 500_\n\n"
            for r in results[:20]:
                msg += f"*{r['SYMBOL']}* LTP {r['LTP']:.2f} SL {r['SL']:.2f} T1 {r['T1']:.2f} RSI {r['RSI']}\n"
            if len(results) > 20: msg += f"\n...and {len(results)-20} more. Full Excel attached 👇"
            send_telegram_msg(bot_token, chat_id, msg)
            send_telegram_file(bot_token, chat_id, excel_data, f"Hanuman_500_BUY_{len(results)}.xlsx", f"🚩 FULL {len(results)} BUY List - {pd.Timestamp.now().strftime('%d-%m %H:%M')}")
            st.sidebar.success(f"Telegram pe {len(results)} ka full file gaya! ✅")
    else:
        st.warning("⚠️ Abhi koi BUY nahi - Market sideway hai")
else:
    st.info(f"👈 SCAN NOW dabao - {len(NIFTY_500)} stocks live scan honge")

st.markdown("---")
st.subheader("📈 LIVE Chart")
symbol = st.selectbox("Stock Select:", NIFTY_500[:100], key="chart")
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
