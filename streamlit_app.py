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
current_date = datetime.now().date()
entreprise2 = st.selectbox("choisissez l'entreprise :", df["nom"].unique(), index=6)
user_date = st.text_input("Entrez une date (format: YYYY-MM-DD) :", current_date)
button2 = st.button("Entrer")  

if button2:
    # Attribution du ticker
    ticker2 = df[df["nom"] == entreprise2]["ticker"].values[0]

    # Récupération des données historiques via yfinance
    stock2 = yf.Ticker(ticker2)
    history_data2 = stock2.history(period="max")  # Récupérer toutes les données disponibles

    if not history_data2.empty:
        # Afficher les données disponibles dans un format compréhensible
        st.write(f"Données disponibles pour {entreprise2} ({ticker2}):")
        st.write(history_data2.head())  # Affiche les premières lignes pour montrer les données

        # Convertir l'index en format 'YYYY-MM-DD' sans heure et fuseau horaire
        history_data2.index = history_data2.index.date  # Cela garde seulement la date (année-mois-jour
        if not user_date.empty:
            try:
                if user_date in history_data2.index:
                    st.write(f"Données pour {selected_date.strftime('%Y-%m-%d')} :")
                else:
                    st.error("La date saisie n'est pas presente dans les données.")
            except ValueError:
                st.error("Le format de la date est incorrect. Veuillez entrer une date au format YYYY-MM-DD.")


