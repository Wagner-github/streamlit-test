import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta



# Définir la chaîne de caractères contenant les données CSV
data = """
nom,ticker
Credit Agricole,ACA.PA
Teleperformance,TEP.PA
Hermes,RMS.PA
Safran,SAF.PA
Air Liquide,AI.PA
Carrefour,CA.PA
TotalEnergies,TTE.PA
L'oreal,OR.PA
Accor Hotels,AC.PA
Bouygues,EN.PA
Sanofi,SAN.PA
Axa,CS.PA
Danone,BN.PA
Pernod Ricard,RI.PA
Lvmh,MC.PA
Thales,HO.PA
Kering,KER.PA
EssilorLuxottica,EL.PA
Schneider Electric,SU.PA
Veolia Environ.,VIE.PA
Saint Gobain,SGO.PA
CapGemini,CAP.PA
Vinci,DG.PA
Vivendi,VIV.PA
Publicis Groupe,PUB.PA
Societe Generale,GLE.PA
Bnp Paribas,BNP.PA
Renault,RNO.PA
Orange,ORA.PA
Engie,ENGI.PA
Legrand SA,LR.PA
Edenred,EDEN.PA
Unibail Rodamco Westfield,URW.PA
Eurofins Scient.,ERF.PA
Dassault Systemes,DSY.PA
Michelin,ML.PA
Arcelor Mittal,MT.PA
Stmicroelectronics,STMPA.PA
Airbus,AIR.PA
Stellantis,STLAP.PA
"""

# Utiliser StringIO pour convertir la chaîne en un fichier-like object
data_io = StringIO(data)

# Lire les données avec Pandas
df = pd.read_csv(data_io)


# Streamlit app details
st.set_page_config(page_title="Financial Analysis", layout="wide")

st.title("Analise financière")
  #ticker = st.text_input("Enter a stock ticker (e.g. TTE.PA)", "TTE.PA")
entreprise = st.selectbox("choisissez l'entreprise :", df["nom"].unique(), index=6)
period = st.selectbox("Choisissez la periode :", ("1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "MAX"), index=7)
button = st.button("Entrer")  

#attribution du ticker de l'entreprise choisie
ticker = df[df["nom"] == entreprise]["ticker"].values[0]

# Format market cap and enterprise value into something readable
def format_value(value):
    suffixes = ["", "K", "M", "Md"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def safe_format(value, fmt="{:.2f}", fallback="N/A"):
    try:
        return fmt.format(value) if value is not None else fallback
    except (ValueError, TypeError):
        return fallback






if button:
    if ticker:
        try:
            with st.spinner('Please wait...'):
                # Retrieve stock data
                stock = yf.Ticker(ticker)
                info = stock.info

                st.subheader(f"{ticker} - {info.get('longName', 'N/A')}")

                # Plot historical stock price data
                period_map = {
                    "1D": ("1d", "1h"),
                    "5D": ("5d", "1d"),
                    "1M": ("1mo", "1d"),
                    "6M": ("6mo", "1wk"),
                    "YTD": ("ytd", "1mo"),
                    "1Y": ("1y", "1mo"),
                    "5Y": ("5y", "3mo"),
                    "MAX": ("max", "1mo")	
                }
                selected_period, interval = period_map.get(period, ("1mo", "1d"))
                history = stock.history(period=selected_period, interval=interval)

                chart_data = pd.DataFrame(history["Close"])
                st.line_chart(chart_data)

                col1, col2, col3 = st.columns(3)

                # Display stock information as a dataframe
                stock_info = [
                    ("Stock Info", "Value"),
                    ("Country", info.get('country', 'N/A')),
                    ("Sector", info.get('sector', 'N/A')),
                    ("Industry", info.get('industry', 'N/A')),
                    ("Market Cap", format_value(info.get('marketCap'))),
                    ("Enterprise Value", format_value( info.get('enterpriseValue'))),
                    ("Employees", info.get('fullTimeEmployees', 'N/A'))
                ]

                df = pd.DataFrame(stock_info[1:], columns=stock_info[0]).astype(str)
                col1.dataframe(df, width=400, hide_index=True)

                # Display price information as a dataframe
                price_info = [
                    ("Price Info", "Value"),
                    ("Current Price", safe_format(info.get('currentPrice'), fmt="${:.2f}")),
                    ("Previous Close", safe_format(info.get('previousClose'), fmt="${:.2f}")),
                    ("Day High", safe_format(info.get('dayHigh'), fmt="${:.2f}")),
                    ("Day Low", safe_format(info.get('dayLow'), fmt="${:.2f}")),
                    ("52 Week High", safe_format(info.get('fiftyTwoWeekHigh'), fmt="${:.2f}")),
                    ("52 Week Low", safe_format(info.get('fiftyTwoWeekLow'), fmt="${:.2f}"))
                ]

                df = pd.DataFrame(price_info[1:], columns=price_info[0]).astype(str)
                col2.dataframe(df, width=400, hide_index=True)

                # Display business metrics as a dataframe
                biz_metrics = [
                    ("Business Metrics", "Value"),
                    ("EPS (FWD)", safe_format(info.get('forwardEps'))),
                    ("P/E (FWD)", safe_format(info.get('forwardPE'))),
                    ("PEG Ratio", safe_format(info.get('pegRatio'))),
                    ("Div Rate (FWD)", safe_format(info.get('dividendRate'), fmt="${:.2f}")),
                    ("Div Yield (FWD)", safe_format(info.get('dividendYield') * 100, fmt="{:.2f}%") if info.get('dividendYield') else 'N/A'),
                    ("Recommendation", info.get('recommendationKey', 'N/A').capitalize())
                ]

                df = pd.DataFrame(biz_metrics[1:], columns=biz_metrics[0]).astype(str)
                col3.dataframe(df, width=400, hide_index=True)

        except Exception as e:
            st.exception(f"An error occurred: {e}")
