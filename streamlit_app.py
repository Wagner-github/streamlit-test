
import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta



# Définir la chaîne de caractères contenant les données CSV
data = """
nom,ticker
Accor Hotels,AC.PA
Air Liquide,AI.PA
Airbus,AIR.PA
Arcelor Mittal,MT.PA
Axa,CS.PA
Bnp Paribas,BNP.PA
Bouygues,EN.PA
CapGemini,CAP.PA
Carrefour,CA.PA
Credit Agricole,ACA.PA
Danone,BN.PA
Dassault Systemes,DSY.PA
Edenred,EDEN.PA
Engie,ENGI.PA
EssilorLuxottica,EL.PA
Eurofins Scient.,ERF.PA
Hermes,RMS.PA
Kering,KER.PA
L'oreal,OR.PA
Legrand SA,LR.PA
Lvmh,MC.PA
Michelin,ML.PA
Orange,ORA.PA
Pernod Ricard,RI.PA
Publicis Groupe,PUB.PA
Renault,RNO.PA
Safran,SAF.PA
Saint Gobain,SGO.PA
Sanofi,SAN.PA
Schneider Electric,SU.PA
Societe Generale,GLE.PA
Stellantis,STLAP.PA
Stmicroelectronics,STMPA.PA
Teleperformance,TEP.PA
Thales,HO.PA
TotalEnergies,TTE.PA
Unibail Rodamco Westfield,URW.PA
Veolia Environ.,VIE.PA
Vinci,DG.PA
Vivendi,VIV.PA
"""

# Utiliser StringIO pour convertir la chaîne en un fichier-like object
data_io = StringIO(data)

# Lire les données avec Pandas
df_chart = pd.read_csv(data_io)


# Streamlit app details
st.set_page_config(page_title="Financial Analysis", layout="wide")

st.title("Analise financière")

st.subheader("Vision globale")
entreprise = st.selectbox("Choisissez l'entreprise :", df_chart["nom"].unique(), index=6, key="selectbox_1")
period = st.selectbox("Choisissez la période :", ("1D", "5D", "1M", "6M", "YTD", "1Y", "5Y", "MAX"), index=7, key="selectbox_2")

# Analyse fine avec chat gpt
st.subheader("Analyse fine avec ChatGPT")
st.text("Pour lancer l'analyse fine, merci de saisir une date, sinon, laisser le cartouche vide et appuyer sur le bouton 'Entrer'.")
current_date = datetime.now().date()
user_date = st.text_input("Entrez une date (format: YYYY-MM-DD) :", "2024-12-09")
button = st.button("Entrer", key="button1")

#attribution du ticker de l'entreprise choisie
ticker = df_chart[df_chart["nom"] == entreprise]["ticker"].values[0]

# Analyse fine avec chat gpt
current_date = datetime.now().date()


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






if button: # Vue des infos de bases
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

                history_data2 = stock.history(period="max")  # Récupérer toutes les données disponibles

                if not history_data2.empty:
                    # Afficher les données disponibles dans un format compréhensible

                    # Convertir l'index en format 'YYYY-MM-DD' sans heure et fuseau horaire
                    history_data2.index = history_data2.index.date  # Cela garde seulement la date (année-mois-jour)

                    # Vérifier si la date est saisie et existe dans les données
                    if user_date:
                        st.write(f"Données disponibles pour {entreprise} ({ticker}) en date du {user_date}:")

                        try:
                            selected_date = pd.to_datetime(user_date).date()  # Convertir la date saisie en datetime.date
                            if selected_date in history_data2.index:
                                selected_data = history_data2.loc[selected_date]
                                st.write(selected_data)
                            else:
                                st.error("La date saisie n'est pas présente dans les données.")
                        except ValueError:
                            st.error("Le format de la date est incorrect. Veuillez entrer une date au format YYYY-MM-DD.")
                    else:
                        st.text('Pas de date dans le cartouche "Entrez une date (format: YYYY-MM-DD)":')
        except Exception as e:
                    st.exception(f"An error occurred: {e}")





