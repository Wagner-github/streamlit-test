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
entreprise2 = st.selectbox("choisissez l'entreprise :", df["nom"].unique(), index=6)
button2 = st.button("Entrer")  

#attribution du ticker de l'entreprise choisie
ticker2 = df[df["nom"] == entreprise]["ticker"].values[0]

if button2: # Vue des infos de bases
    if ticker2:
        # Récupération des données historiques via yfinance
    stock2 = yf.Ticker(ticker2)
    history_data2 = stock2.history(period="max")  # Récupérer toutes les données disponibles

    if not history_data2.empty:
        # Extraction des dates disponibles
        available_dates = history_data2.index.strftime("%Y-%m-%d").tolist()

        # Sélection de la date
        selected_date = st.selectbox("Choisissez une date :", available_dates)

        # Affichage des informations pour la date choisie
        if st.button("Afficher les données"):
            selected_data = history_data2.loc[selected_date]
            st.write(f"Données pour {selected_date} :")
            st.dataframe(selected_data)
    else:
        st.error("Aucune donnée historique disponible pour cette entreprise.")
