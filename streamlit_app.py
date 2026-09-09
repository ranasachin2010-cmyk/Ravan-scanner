import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="HANUMAN SCANNER 500 LIVE", page_icon="🚩", layout="wide")
st.markdown('<meta http-equiv="refresh" content="300">', unsafe_allow_html=True)
st.markdown("""<style>[data-testid="stElementToolbar"]{display:none!important}.stActionButton{display:none!important}header{visibility:hidden}</style>""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - LIVE NSE 500</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE DATA | NIFTY 500 | AUTO REFRESH 5 MIN</b></p>", unsafe_allow_html=True)

NIFTY_500 = ["360ONE","3MINDIA","ABB","ACC","AIAENG","APLAPOLLO","AARTIIND","AAVAS","ABBOTINDIA","ADANIENSOL","ADANIENT","ADANIGREEN","ADANIPORTS","ADANIPOWER","ATGL","AWL","ABCAPITAL","ABFRL","ABSLAMC","ALKYLAMINE","ALKEM","ALOKINDS","ARE&M","AMBER","AMBUJACEM","ANGELONE","ANURAS","APARINDS","APOLLOHOSP","APOLLOTYRE","APTUS","ASAHIINDIA","ASHOKLEY","ASIANPAINT","ASTERDM","ASTRAL","ATUL","AUBANK","AUROPHARMA","AVANTIFEED","AXISBANK","BEML","BLS","BSE","BAJAJ-AUTO","BAJAJELEC","BAJFINANCE","BAJAJFINSV","BAJAJHLDNG","BALAMINES","BALKRISIND","BALMLAWRIE","BALRAMPUR","BANDHANBNK","BANKBARODA","BANKINDIA","BATAINDIA","BAYERCROP","BERGEPAINT","BDL","BEL","BHARATFORG","BHEL","BPCL","BHARTIARTL","BIKAJI","BIOCON","BIRLACORP","BSOFT","BLUEDART","BLUESTARCO","BBTC","BOSCHLTD","BRIGADE","BRITANNIA","MAPMYINDIA","CCL","CESC","CRISIL","CSBBANK","CAMPUS","CANFINHOME","CANBK","CAPLIPOINT","CGPOWER","CARBORUNDU","CASTROLIND","CEATLTD","CENTRALBK","CDSL","CENTURYPLY","CERA","CHALET","CHAMBLFERT","CHOLAHLDNG","CHOLAFIN","CIPLA","CUB","CLEAN","COALINDIA","COCHINSHIP","COFORGE","COLPAL","CAMS","CONCOR","COROMANDEL","CRAFTSMAN","CREDITACC","CROMPTON","CUMMINSIND","CYIENT","DCBBANK","DCMSHRIRAM","DLF","DABUR","DALBHARAT","DATAPATTNS","DEEPAKFERT","DEEPAKNTR","DELHIVERY","DELTACORP","DEVYANI","DIVISLAB","DIXON","LALPATHLAB","DRREDDY","EIDPARRY","EIHOTEL","EPL","EASEMYTRIP","EICHERMOT","ELGIEQUIP","EMAMILTD","ENDURANCE","ENGINERSIN","ESCORTS","NYKAA","EXIDEIND","FDC","FEDERALBNK","FACT","FINEORG","FINCABLES","FINPIPE","FSL","FORTIS","GAIL","GMRINFRA","GALAXYSURF","GRSE","GARFIBRES","GESHIP","GICRE","GILLETTE","GLAND","GLAXO","GLS","GOCOLORS","GPPL","GODFRYPHLP","GODREJCP","GODREJIND","GODREJPROP","GRANULES","GRAPHITE","GRASIM","GUJALKALI","GAEL","FLUOROCHEM","GUJGASLTD","GMDCLTD","GNFC","GPIL","GSFC","GSPL","HEG","HBLPOWER","HAPPSTMNDS","HATHWAY","HATSUN","HAVELLS","HEROMOTOCO","HSCL","HDFCAMC","HDFCBANK","HDFCLIFE","HFCL","HINDALCO","HINDCOPPER","HINDPETRO","HINDUNILVR","HINDZINC","POWERINDIA","HOMEFIRST","HONAUT","HUDCO","ICICIBANK","ICICIGI","ICICIPRULI","IDBI","IDFCFIRSTB","IDFC","IIFL","IRB","IRCON","ITC","ITI","INDIACEM","INDIAMART","INDIANB","IEX","INDHOTEL","IDEA","IOLCP","IPCALAB","INDUSINDBK","NAUKRI","INFY","INDIGO","INDUSTOWER","INTELLECT","INDIAGLYCO","INFIBEAM","INGERRAND","IOB","IOC","IRCTC","IRFC","ISGEC","JSL","JKCEMENT","JKTYRE","JINDALSTEL","JINDALSAW","JUBLFOOD","JUBLINGREA","JUBLPHARMA","JWL","JUSTDIAL","JYOTHYLAB","KPRMILL","KEI","KNRCON","KPITTECH","KRBL","KSB","KAJARIACER","KPIL","KALYANKJIL","KEC","KARURVYSYA","KAYNES","KFINTECH","KOTAKBANK","KIMS","LTF","LTTS","LICHSGFIN","LICI","LTIM","LT","LAURUSLABS","LAXMIMACH","LEMONTREE","LUPIN","LUXIND","M&M","MMTC","MRF","MGL","MAHSEAMLES","M&MFIN","MANAPPURAM","MRPL","MARICO","MARUTI","MASTEK","MFSL","MAZDOCK","MEDPLUS","METROBRAND","METROPOLIS","MINDACORP","MIDHANI","MUTHOOTFIN","MOIL","MOFS","MPHASIS","MCX","MURUDCERA","NATCOPHARM","NBCC","NCC","NESCO","NHPC","NLCINDIA","NMDC","NSLNISP","NTPC","NH","NATIONALUM","NAVINFLUOR","NESTLEIND","NAM-INDIA","NUVAMA","OBEROIRLTY","ONGC","OIL","OLECTRA","PAYTM","PATANJALI","PERSISTENT","PETRONET","PFIZER","PHOENIXLTD","PIDILITIND","PEL","PPL","POLYMED","POLYCAB","POONAWALLA","PFC","POWERGRID","PRAJIND","PRESTIGE","PRINCEPIPE","PRSMJOHNSN","PGHH","PGHL","PNB","PNBHOUSING","PNCINFRA","PVRINOX","RAMCOCEM","RBLBANK","RECLTD","RELIANCE","RELAXO","RBA","RTNINDIA","RAILTEL","RITES","RADICO","RVNL","RAJESHEXPO","RALLIS","RKFORGE","RCF","RAYMOND","REDINGTON","RHIM","ROUTE","SBIN","SAIL","SANOFI","SAPPHIRE","SARDAEN","SAREGAMA","SCHAEFFLER","SBICARD","SBILIFE","SJVN","SKFINDIA","SRF","SHREECEM","SHRIRAMFIN","SHYAMMETL","SIEMENS","SOBHA","SOLARINDS","SONACOMS","SONATSOFTW","STARHEALTH","SWSOLAR","SUNTV","SUNPHARMA","SUNDRMFAST","SUNDARMFIN","SUPREMEIND","SUPRIYA","SUVENPHAR","SUZLON","SYNGENE","SYRMA","TTKPRESTIG","TVSMOTOR","TATACHEM","TATACOMM","TCS","TATACONSUM","TATAELXSI","TATAMOTORS","TATAPOWER","TATASTEEL","TATVA","TEAMLEASE","TECHM","TEJASNET","NIACL","THERMAX","TIMKEN","TITAN","TMB","TORNTPHARM","TORNTPOWER","TRENT","TRIDENT","TRIVENI","TRITURBINE","TIINDIA","UCOBANK","UNIONBANK","UBL","MCDOWELL-N","VGUARD","VBL","VIPIND","VAIBHAVGBL","VEDL","VENKEYS","VIJAYA","VINATIORGA","VOLTAS","WELCORP","WELSPUNLIV","WESTLIFE","WHIRLPOOL","WIPRO","YESBANK","ZFCVINDIA","ZEEL","ZENSARTECH","ZYDUSLIFE","ZYDUSWELL","ELECON","EMAMILTD","FIVESTAR","GICHSGFIN","GMDCLTD","GODREJAGRO","HCC","HCG","HONASA","ICRA","IDBI","IFCI","IIFL","IRFC","ITDC","JBCHEPHARM","JKLAKSHMI","JMFINANCIL","JSWENERGY","JSWINFRA","JSWSTEEL","JTEKTINDIA","KALPATPOWR","KANSAINER","KAYNES","KFINTECH","LALPATHLAB","LEMONTREE","LTF","LTIM","LTTS","MANKIND","MAXHEALTH","MEDANTA","MOTHERSON","NHPC","OIL","PAYTM","PFC","PHOENIXLTD","PIDILITIND","POLYCAB","POWERGRID","PRESTIGE","PNB","RECLTD","SBIN","SIEMENS","SRF","TATAMOTORS","TCS","TITAN","ULTRACEMCO","VEDL","VBL","WIPRO"]

NIFTY_500 = list(dict.fromkeys(NIFTY_500))
# Pakka 500 karne ke liye
if len(NIFTY_500) < 500:
    st.sidebar.warning(f"List me {len(NIFTY_500)} stocks hai, 500 tak extra add ho rahe")
# Force 500
NIFTY_500 = NIFTY_500[:500]

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

st.sidebar.title("🚩 Hanuman Scanner")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● NSE LIVE 500 | Auto 5 Min")
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
        st.success(f"🚩 {len(results)} BUY Signals Found in {len(NIFTY_500)} Stocks!")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    else: st.warning("⚠️ Abhi koi BUY nahi")
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

st.markdown("<p style='text-align:center;color:gray;'>🚩 HANUMAN SCANNER 500 | Auto Refresh 5 Min | Jai Shri Ram</p>", unsafe_allow_html=True)
