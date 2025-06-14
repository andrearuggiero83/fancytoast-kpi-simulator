import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")

# Logo
logo = Image.open("LOGO_Fancytoast.png")
st.image(logo, width=300)

st.title("📊 Fancytoast KPI Simulator")
st.markdown("Simula le performance economiche modificando i parametri di input")

# -------------------- INPUT -------------------- #
st.header("🛠️ Parametri di Input")
col1, col2, col3 = st.columns(3)

with col1:
    revpash = st.number_input("RevPASH (€)", min_value=1.0, value=5.0, step=0.1)
    avg_ticket = st.number_input("Scontrino medio (€)", min_value=5.0, value=25.0, step=0.5)
    food_cost = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27)

with col2:
    brunch_hours = st.number_input("Ore operative brunch", min_value=1, max_value=12, value=6)
    seats = st.number_input("Posti a sedere", min_value=1, max_value=200, value=70)
    labor_cost = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32)

with col3:
    opex = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20)

# -------------------- FASCE ORARIE -------------------- #
st.header("🕒 Calcolo Totale Giornaliero dalle Fasce Orarie")
fasce_orarie = ["Mattino", "Brunch", "Snack", "Aperitivo"]
ore = ["8,00 -10,00", "10,00-16,00", "16,00-18,00", "18,00-21,00"]

percentuali = []
atv_values = []

col1, col2 = st.columns(2)
with col1:
    percentuali = [st.number_input(f"% Coperti {f}", min_value=0.0, max_value=1.0, value=val, step=0.1)
                   for f, val in zip(fasce_orarie, [0.4, 0.6, 0.4, 0.5])]
with col2:
    atv_values = [st.number_input(f"ATV {f} (€)", min_value=0.0, value=val, step=0.5)
                  for f, val in zip(fasce_orarie, [10, 25, 10, 12.5])]

coperti_brunch = int(seats * brunch_hours * (revpash / avg_ticket))
coperti_fasce = [int(p * coperti_brunch) for p in percentuali]
ricavi_fasce = [round(c * a, 2) for c, a in zip(coperti_fasce, atv_values)]

fasce_df = pd.DataFrame({
    "Fasce Orarie": fasce_orarie,
    "Ore": ore,
    "% Coperti": percentuali,
    "ATV (€)": atv_values,
    "Coperti": coperti_fasce,
    "Ricavi (€)": ricavi_fasce
})

st.dataframe(fasce_df, use_container_width=True)

# -------------------- KPI CALCOLATI -------------------- #
ricavi_totali_giornalieri = sum(ricavi_fasce)
coperti_giornalieri_totali = sum(coperti_fasce)
ricavi_annui = ricavi_totali_giornalieri * 365
coperti_annui = coperti_giornalieri_totali * 365
revpasm = ricavi_totali_giornalieri / 60  # mq fissi

# Margini
ebitda = ricavi_annui * (1 - food_cost/100 - labor_cost/100 - opex/100)
ebitda_perc = ebitda / ricavi_annui * 100

st.header("📈 KPI Calcolati")
st.metric("Coperti Giornalieri Brunch", coperti_brunch)
st.metric("Coperti Totali Giornalieri", coperti_giornalieri_totali)
st.metric("Ricavi Giornalieri Brunch (€)", round(coperti_brunch * avg_ticket, 2))
st.metric("Ricavi Giornalieri Totali (€)", round(ricavi_totali_giornalieri, 2))
st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,.0f}".replace(",", "."))
st.metric("Coperti Annui", f"{coperti_annui:,.0f}".replace(",", "."))
st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
st.metric("EBITDA (€)", f"{ebitda:,.0f}".replace(",", "."))
st.metric("EBITDA %", f"{ebitda_perc:.1f}%")
