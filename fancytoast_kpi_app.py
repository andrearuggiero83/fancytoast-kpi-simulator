import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Fancytoast KPI Simulator", page_icon="📊", layout="wide")
st.title("Fancytoast KPI Simulator")
st.caption("Simula le performance economiche modificando i parametri di input")

st.header(":wrench: Parametri di Input")

col1, col2, col3 = st.columns(3)

with col1:
    revpash = st.number_input("RevPASH (€)", min_value=0.0, value=5.00, step=0.25, format="%0.2f")
    receipt = st.number_input("Scontrino medio (€)", min_value=0.0, value=25.00, step=1.0, format="%0.2f")
    food_cost_pct = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27)

with col2:
    hours = st.number_input("Ore operative brunch", min_value=1, max_value=12, value=6)
    seats = st.number_input("Posti a sedere", min_value=1, value=70)
    labor_cost_pct = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32)

with col3:
    opex_pct = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20)

st.markdown("---")
st.subheader(":alarm_clock: Calcolo Totale Giornaliero dalle Fasce Orarie")

fasce = pd.DataFrame({
    "Fasce Orarie": ["Mattino", "Brunch", "Snack", "Aperitivo"],
    "Ore": ["8,00 -10,00", "10,00-16,00", "16,00-18,00", "18,00-21,00"],
    "% Coperti": [0.4, 0.6, 0.4, 0.5],
    "ATV": [10, receipt, 10, 12.5]
})

coperti_brunch = int(revpash * seats * hours / receipt)
fasce["Coperti"] = (coperti_brunch * fasce["% Coperti"]).round(0).astype(int)
fasce["Ricavi"] = (fasce["Coperti"] * fasce["ATV"]).round(2)

st.dataframe(fasce, use_container_width=True)

total_coperti = fasce["Coperti"].sum()
total_ricavi = fasce["Ricavi"].sum()
total_ricavi_annuo = total_ricavi * 365
revpasm = total_ricavi / (seats * hours)

ebitda = total_ricavi * (1 - (food_cost_pct + labor_cost_pct + opex_pct) / 100)
ebitda_pct = ebitda / total_ricavi if total_ricavi > 0 else 0

st.markdown("---")
st.subheader(":bar_chart: KPI Calcolati")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric("Coperti Giornalieri Brunch", f"{coperti_brunch}")
    st.metric("Coperti Totali Giornalieri", f"{total_coperti}")
    st.metric("Coperti Annui", f"{int(total_coperti * 365):,}")

with kpi2:
    st.metric("Ricavi Giornalieri Brunch (€)", f"{coperti_brunch * receipt:,.0f}")
    st.metric("Ricavi Giornalieri Totali (€)", f"{total_ricavi:,.0f}")
    st.metric("Ricavi Annui Totali (€)", f"{total_ricavi_annuo:,.0f}")

with kpi3:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:,.2f} €/mq")

with kpi4:
    st.metric("EBITDA (€)", f"{ebitda:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct * 100:.1f}%")
