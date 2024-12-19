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
  #ticker = st.text_input("Enter a stock ticker (e.g. TTE.PA)", "TTE.PA")
entreprise2 = st.selectbox("choisissez l'entreprise :", df["nom"].unique(), index=6)
button2 = st.button("Entrer")  

#attribution du ticker de l'entreprise choisie
ticker2 = df[df["nom"] == entreprise2]["ticker"].values[0]


if button2:
    # Attribution du ticker
    ticker2 = df[df["nom"] == entreprise2]["ticker"].values[0]

    # Récupération des données historiques via yfinance
    stock2 = yf.Ticker(ticker2)
    history_data2 = stock2.history(period="max")  # Récupérer toutes les données disponibles

    if not history_data2.empty:
        # Extraction des années, mois et jours disponibles
        history_data2.index = pd.to_datetime(history_data2.index)  # S'assurer que l'index est de type datetime
        available_years = history_data2.index.year.unique().tolist()
        selected_year = st.selectbox("Choisissez une année :", available_years)

        # Filtrer les données pour l'année choisie
        year_filtered_data = history_data2[history_data2.index.year == selected_year]
        available_months = year_filtered_data.index.month.unique().tolist()
        selected_month = st.selectbox("Choisissez un mois :", available_months)

        # Filtrer les données pour le mois choisi
        month_filtered_data = year_filtered_data[year_filtered_data.index.month == selected_month]
        available_days = month_filtered_data.index.day.unique().tolist()
        
        # Utiliser un widget de type 'selectbox' avec un choix par défaut
        selected_day = st.selectbox("Choisissez un jour :", available_days, index=0)

        # Combiner les sélections pour obtenir la date finale
        if st.button("Afficher les données"):
            selected_date = pd.Timestamp(year=selected_year, month=selected_month, day=selected_day)
            if selected_date in history_data2.index:
                selected_data = history_data2.loc[selected_date]
                st.write(f"Données pour {selected_date.strftime('%Y-%m-%d')} :")
                st.dataframe(selected_data)
            else:
                st.error("Aucune donnée disponible pour cette date.")
    else:
        st.error("Aucune donnée historique disponible pour cette entreprise.")
