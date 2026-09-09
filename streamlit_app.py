import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="HANUMAN SCANNER 500 LIVE", page_icon="🚩", layout="wide")

# SAB ICON HATANE KA JADU
st.markdown("""
<style>
[data-testid="stElementToolbar"] {display: none !important;}
.stActionButton {display: none !important;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;color:#ff6600;'>🚩 HANUMAN SCANNER - LIVE NSE 500</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:green;'><b>● LIVE NSE DATA | NIFTY 500</b></p>", unsafe_allow_html=True)

# NIFTY 500 - PURA LIST
NIFTY_500 = [
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
"SYNGENE","TATAELXSI","TIINDIA","TRIDENT","UJJIVANSFB","VGUARD","WELCORP","ZYDUSLIFE","AFFLE","ANGELONE",
"ASTERDM","ATUL","BDL","BLUESTARCO","CENTRALBK","COFORGE","DELHIVERY","EIHOTEL","ELGIEQUIP","GICRE",
"GLAXO","GSPL","HBLPOWER","IDBI","IIFL","IRB","JBCHEPHARM","JKCEMENT","KARURVYSYA","KIMS",
"MASTEK","MAZDOCK","MOTILALOFS","NYKAA","OLECTRA","PATANJALI","PNBHOUSING","RADICO","RITES","SOBHA",
"SOLARINDS","STARHEALTH","SUVENPHAR","TANLA","TEAMLEASE","UCOBANK","UNIONBANK","VAIBHAVGBL","WELSPUNLIV","ZYDUSWELL",
"AARTIPHARM","ABSLAMC","AEGISCHEM","AKZOINDIA","ALKYLAMINE","AMBER","ANURAS","APLLTD","ASAHIINDIA","ASTRAL",
"AVANTIFEED","BAJAJELEC","BALMLAWRIE","BAYERCROP","BECTORFOOD","BFUTILITIE","BHARATRAS","BIRLACABLE","BLUEDART","BORORENEW",
"BRIGADE","BSE","CCL","CENTURYPLY","CHALET","CHEMPLASTS","CIGNITEC","CYIENT","DCBBANK","DCMSHRIRAM",
"DEEPAKFERT","DHANUKA","DODLA","DYNAMATECH","EIDPARRY","ELECON","EQUITASBNK","ERIS","ESABINDIA","ETHOS",
"FCL","FIEMIND","FINCABLES","FINEORG","FIVESTAR","FLUOROCHEM","GAEL","GARFIBRES","GESHIP","GHCL",
"GLS","GMMPFAUDLR","GNA","GOCLCORP","GOCOLORS","GODREJAGRO","GPIL","GPPL","GRANULES","GRAPHITE",
"GRAVITA","HARSHA","HCC","HCG","HEIDELBERG","HFCL","HGINFRA","HIKAL","HINDOILEXP","HOMEFIRST",
"HSCL","ICRA","IOLCP","IRCON","ITDC","JAYBARMARU","JBMA","JCHAC","JINDALPOLY","JKLAKSHMI",
"JPPOWER","JSWHL","JTEKTINDIA","JTLIND","KABRAEXTRU","KALPATPOWR","KANSAINER","KESORAMIND","KIRLOSENG","KNRCON",
"KTKBANK","LAKSHMIMACH","LEMONTREE","LGBBROSLTD","LINDEINDIA","LLOYDSME","LUMAXTECH","MAHABANK","MAHLOG","MANINFRA",
"MANGCHEFER","MARKSANS","MAXHEALTH","MAYURUNIQ","MMTC","MOIL","MOLDTECH","MONTECARLO","MOREPENLAB","MTARTECH",
"NATCOPHARM","NDL","NEOGEN","NESCO","NFL","NILKAMAL","NIPPOBATRY","NOCIL","NRBBEARING","NUCLEUS",
"OBEROIRLTY","OMAXE","ONMOBILE","ONWARDTEC","ORIENTCEM","ORIENTELEC","ORIENTHOT","PACL","PALREDTEC","PANAMAPET",
"PARACABLES","PARKHOTELS","PCJEWELLER","PDSL","PENIND","PFOCUS","PGEL","PGHL","PHOENIXLTD","PILANIINVS",
"PITTIENG","PNBGILTS","PNCINFRA","POLYPLEX","PONNIERODE","POWERMECH","PPAP","PRAKASH","PRECOT","PRECWIRE",
"PREMEXPLN","PRICOLLTD","PRINCEPIPE","PRSMJOHNSN","PSB","PSPPROJECT","PTC","PTL","PUNJABCHEM","QUESS",
"QUICKHEAL","RADAAN","RAILTEL","RAIN","RAJESHEXPO","RALLIS","RAMASTEEL","RAMCOIND","RAMCOSYS","RATEGAIN",
"RBLBANK","REDINGTON","RELAXO","RELIGARE","REPCOHOME","RESPONIND","RGL","RHIM","RICOAUTO","RKFORGE",
"ROLEXRINGS","ROSSARI","ROTO","ROUTE","RPGLIFE","RPOWER","RSYSTEMS","RTNINDIA","SADBHAV","SAFARI",
"SALASAR","SANDHAR","SANGHIIND","SANGHVIMOV","SANOFI","SAPPHIRE","SAREGAMA","SBCL","SCHAEFFLER","SCHAND",
"SCHNEIDER","SEAMECLTD","SELAN","SEPC","SEQUENT","SFL","SHALBY","SHANKARA","SHANTIGEAR","SHAREINDIA",
"SHEMAROO","SHILPAMED","SHK","SHOPERSTOP","SHYAMCENT","SHYAMMETL","SIEMENS","SIRCA","SKFINDIA","SKIPPER",
"SMLISUZU","SMLT","SMSLIFE","SMSPHARMA","SNOWMAN","SOLARA","SOMANYCERA","SONATSOFTW","SOTL","SOUTHBANK",
"SPAL","SPANDANA","SPARC","SPECIALITY","SPENCERS","SPIC","SPLPET","SPMLINFRA","SPORTKING","SRF",
"STARCEMENT","STLTECH","STOVEKRAFT","SUBEXLTD","SUBROS","SUDARSCHEM","SUMICHEM","SUNCLAYLTD","SUNDARMFIN","SUNTECK",
"SUPERHOUSE","SUPRAJIT","SURANAT&P","SURYAROSNI","SUTLEJTEX","SYMPHONY","TANLA","TARSONS","TATACOFFEE","TATAMETALI",
"TCIEXP","TCNSBRANDS","TCPLPACK","TECHM","TEJASNET","TEXRAIL","THANGAMAYL","THERMAX","THOMASCOOK","TI",
"TIMETECHNO","TIMKEN","TIPSINDLTD","TMB","TNPETRO","TNPL","TORNTPOWER","TPHQ","TRANSPEK","TRENT",
"TTKPRESTIG","TTML","TV18BRDCST","TVSMOTOR","TVSSCS","TVTODAY","UCAL","UFLEX","UJJIVAN","ULTRACEMCO",
"UNICHEMLAB","UNITECH","UNITEDTEA","UNOMINDA","USHAMART","UTIAMC","VADILALIND","VAKRANGEE","VENKEYS","VHL",
"VIDHIING","VIJAYA","VINATIORGA","VINDHYATEL","VIPIND","VIPULLTD","VISAKAIND","VLSFINANCE","VMART","VOLTAMP",
"VOLTAS","VRLLOG","VSSL","VSTIND","VSTTILLERS","VTL","WABAG","WALCHANNAG","WANBURY","WEBSOLENERG",
"WELENT","WESTLIFE","WHEELS","WHIRLPOOL","WINDMACHIN","WOCKPHARMA","XCHANGING","XLENERGY","XPROINDIA","YESBANK",
"ZANDUREALT","ZEELEARN","ZEEL","ZENSARTECH","ZENTEC","ZODIACLOTH","ZOTA","ZUARI","ZUARIIND","ZYDUSLIFE"
]

NIFTY_500 = list(dict.fromkeys(NIFTY_500))
NIFTY_500 = NIFTY_500[:500]

def get_data(symbol):
    try:
        df = yf.download(f"{symbol}.NS", period="5d", interval="15m", progress=False, auto_adjust=False)
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
        df = df.dropna()
        last = df.iloc[-1]
        is_buy = (float(last['Close']) > float(last['EMA21'])) and (float(last['EMA21']) > float(last['EMA50'])) and (float(last['RSI']) > 55)
        return {"df": df, "last": last, "is_buy": is_buy, "symbol": symbol}
    except:
        return None

st.sidebar.title("🚩 Hanuman Scanner")
st.sidebar.metric("Total Stocks", len(NIFTY_500))
st.sidebar.success("● NSE LIVE 500")
scan = st.sidebar.button("🔍 LIVE SCAN 500 NOW", type="primary", use_container_width=True)

if scan:
    results = []
    bar = st.progress(0)
    status = st.empty()
    def scan_one(sym):
        return get_data(sym)
    with ThreadPoolExecutor(max_workers=30) as ex:
        for i, res in enumerate(ex.map(scan_one, NIFTY_500)):
            if res and res['is_buy']:
                last = res['last']
                price = float(last['Close'])
                results.append({
                    "SYMBOL": res['symbol'],
                    "LTP": round(price,2),
                    "ENTRY": round(price,2),
                    "SL": round(price*0.985,2),
                    "T1": round(price*1.02,2),
                    "T2": round(price*1.04,2),
                    "RSI": round(float(last['RSI']),1),
                    "SIGNAL": "🚩 BUY"
                })
            bar.progress((i+1)/len(NIFTY_500))
            status.text(f"Scanning {i+1}/{len(NIFTY_500)} | BUY: {len(results)}")
    bar.empty()
    status.empty()
    if results:
        st.success(f"🚩 {len(results)} BUY Signals Found in {len(NIFTY_500)} Stocks!")
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Abhi koi BUY nahi")
else:
    st.info(f"👈 SCAN NOW dabao - {len(NIFTY_500)} stocks ka LIVE scan hoga! 2-3 min lagega")

st.markdown("---")
st.subheader("📈 LIVE Chart")
symbol = st.selectbox("Stock Select:", NIFTY_500[:100], key="chart_select")
live = get_data(symbol)
if live:
    df_chart = live['df']
    last = live['last']
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("LTP", f"Rs {float(last['Close']):.2f}")
    c2.metric("EMA21", f"{float(last['EMA21']):.2f}")
    c3.metric("EMA50", f"{float(last['EMA50']):.2f}")
    c4.metric("RSI", f"{float(last['RSI']):.1f}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'], name="Close", line=dict(color="#00ff00", width=2)))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA21'], name="EMA21", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA50'], name="EMA50", line=dict(color="red")))
    fig.update_layout(template="plotly_dark", height=450, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False, 'displaylogo': False})

st.markdown("<p style='text-align:center;color:gray;'>🚩 HANUMAN SCANNER 500 | Jai Shri Ram</p>", unsafe_allow_html=True)
