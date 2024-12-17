import streamlit as st
import yfinance as yf
import pandas as pd
data = ("/content/drive/MyDrive/Google Sheets/Copie de coedcac40 - libelles.csv")
dg = pd.read_csv(data)
print(dg.head(2))
