import streamlit as st
import yfinance as yf
import pandas as pd
from io import StringIO

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
with st.sidebar:
    st.title("Analise financière")
    #ticker = st.text_input("Enter a stock ticker (e.g. TTE.PA)", "TTE.PA")
    ticker = st.selectbox("choisissez l'entreprise :", df["nom"].unique(), index=35)
    period = st.selectbox("Enter a time frame", ("1D", "5D", "1M", "6M", "YTD", "1Y", "5Y"), index=2)
    button = st.button("Entrer")
code_PA = (
"AC.PA", "AI.PA", "AIR.PA", "MT.PA", "CS.PA", "BNP.PA", "EN.PA", "CA.PA", "DG.PA",
"DSY.PA", "EDR.PA", "ENGI.PA", "RI.PA", "EF.PA", "RMS.PA", "OR.PA", "RI.PA",
"PUB.PA", "RNO.PA", "SAF.PA", "SGO.PA", "GLE.PA", "MC.PA", "ML.PA", "ORA.PA",
"PUB.PA", "SAN.PA", "SU.PA", "GLE.PA", "VIE.PA", "VIV.PA"
)
#)
