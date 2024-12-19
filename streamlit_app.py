import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Données simulées
dates = pd.date_range("2024-01-01", periods=10)
values = np.random.randint(100, 200, size=10)
chart_data = pd.DataFrame({"Date": dates, "Value": values})

# Graphique interactif
fig = px.line(chart_data, x="Date", y="Value", title="Graphique interactif")
selected_point = st.plotly_chart(fig, use_container_width=True)

# Zone pour afficher des informations (simulée ici, car Streamlit ne gère pas nativement la sélection des points)
clicked_date = st.text_input("Entrez une date après avoir observé le graphique (au format YYYY-MM-DD) :")

# Affichage des informations associées
if clicked_date:
    value = chart_data.loc[chart_data["Date"].dt.strftime("%Y-%m-%d") == clicked_date, "Value"].iloc[0]
    st.write(f"Pour la date {clicked_date}, la valeur est : {value}.")
