
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Calculator", layout="wide")

st.image("LOGO_Fancytoast.png", width=200)
st.title("📊 Fancytoast KPI Calculator")

st.markdown("Modifica i parametri di input qui sotto per simulare le performance del tuo punto vendita.")

st.sidebar.header("Parametri di Input")

# --- Input Sidebar ---
revpash = st.sidebar.number_input("RevPASH (€ per posto per ora)", min_value=0.0, value=5.0, step=0.1)
ore_brunch = st.sidebar.number_input("Ore operative brunch", min_value=1, max_value=12, value=6)
posti_sedere = st.sidebar.number_input("Posti a sedere totali", min_value=1, value=70)
atv = st.sidebar.number_input("Scontrino medio (€)", min_value=1.0, value=25.0)
food_cost = st.sidebar.slider("Food Cost (%)", 0, 100, 27)
labor_cost = st.sidebar.slider("Labor Cost (%)", 0, 100, 32)
opex = st.sidebar.slider("OPEX (%)", 0, 100, 20)

# --- Calcoli KPI ---
coperti_giornalieri_brunch = revpash * ore_brunch * posti_sedere / atv
ricavi_giornalieri_brunch = coperti_giornalieri_brunch * atv
ricavi_giornalieri_totali = ricavi_giornalieri_brunch  # si può moltiplicare per moltiplicatore in future versioni
ricavi_annuali = ricavi_giornalieri_totali * 365

costi_totali = (food_cost + labor_cost + opex) / 100 * ricavi_annuali
ebitda = ricavi_annuali - costi_totali
ebitda_pct = ebitda / ricavi_annuali * 100

# --- Output Table ---
kpi_data = {
    "KPI": [
        "Coperti Giornalieri Brunch",
        "Ricavi Giornalieri Brunch (€)",
        "Ricavi Giornalieri Totali (€)",
        "Ricavi Annui Totali (€)",
        "Food Cost (%)",
        "Labor Cost (%)",
        "OPEX (%)",
        "EBITDA (€)",
        "EBITDA (%)"
    ],
    "Valore": [
        round(coperti_giornalieri_brunch, 2),
        round(ricavi_giornalieri_brunch, 2),
        round(ricavi_giornalieri_totali, 2),
        round(ricavi_annuali, 2),
        f"{food_cost}%",
        f"{labor_cost}%",
        f"{opex}%",
        round(ebitda, 2),
        f"{round(ebitda_pct, 1)}%"
    ]
}

st.subheader("📈 Risultati KPI Calcolati")
st.table(pd.DataFrame(kpi_data))
