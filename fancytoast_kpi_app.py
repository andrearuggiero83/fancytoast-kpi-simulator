import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", page_icon="📊", layout="wide")

st.markdown("![Logo](https://raw.githubusercontent.com/andrearuggiero83/fancytoast-kpi-simulator/main/assets/logo_fancytoast.png)", unsafe_allow_html=True)
st.title("📊 Fancytoast KPI Simulator")
st.markdown("Simula le performance economiche modificando i parametri di input")

# ------------------- INPUT SECTION -------------------
st.header("🛠️ Parametri di Input")
col1, col2, col3 = st.columns(3)

with col1:
    revpash = st.number_input("RevPASH (€)", min_value=0.0, value=5.00, step=0.1)
    scontrino_medio = st.number_input("Scontrino medio (€)", min_value=1.0, value=25.0, step=0.5)
    food_cost_pct = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27, step=1)

with col2:
    ore_brunch = st.number_input("Ore operative brunch", min_value=1, max_value=12, value=6, step=1)
    posti = st.number_input("Posti a sedere", min_value=10, max_value=200, value=70, step=1)
    labor_cost_pct = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32, step=1)

with col3:
    opex_pct = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20, step=1)
    metri_quadri = st.number_input("Metri quadri di somministrazione", min_value=10, max_value=500, value=112, step=1)

# ------------------- ORARI E % COPERTI -------------------
st.subheader("⏰ Calcolo Totale Giornaliero dalle Fasce Orarie")
fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
orari_default = ["8:00-10:00", "10:00-16:00", "16:00-18:00", "18:00-21:00"]
orari = []

col_orari = st.columns(4)
for i, fascia in enumerate(fasce):
    if fascia == "Brunch":
        orari.append(orari_default[i])
        col_orari[i].text_input(f"{fascia}", value=orari_default[i], disabled=True)
    else:
        orari.append(col_orari[i].text_input(f"{fascia}", value=orari_default[i]))

col_pct = st.columns(4)
coperti_pct = [col_pct[i].number_input(f"% Coperti {fasce[i]}", min_value=0, max_value=100, value=val, step=1) for i, val in enumerate([40, 60, 40, 50])]

col_atv = st.columns(4)
atv_values = [col_atv[i].number_input(f"ATV {fasce[i]} (€)", min_value=0.0, value=val, step=0.5) for i, val in enumerate([10, 25, 10, 12.5])]

# ------------------- CALCOLI -------------------
coperti_totali = [round((pct / 100) * posti) for pct in coperti_pct]
ricavi = [round(coperti * atv, 2) for coperti, atv in zip(coperti_totali, atv_values)]

df = pd.DataFrame({
    "Fasce Orarie": fasce,
    "Ore": orari,
    "% Coperti": [f"{v}%" for v in coperti_pct],
    "ATV (€)": atv_values,
    "Coperti": coperti_totali,
    "Ricavi (€)": ricavi
})

coperti_brunch = coperti_totali[1]
ricavi_brunch = ricavi[1]
coperti_tot = sum(coperti_totali)
ricavi_tot = sum(ricavi)
coperti_annui = coperti_tot * 365
ricavi_annui = ricavi_tot * 365

revpasm = ricavi_tot / metri_quadri if metri_quadri > 0 else 0

ebitda = ricavi_annui * (1 - (food_cost_pct + labor_cost_pct + opex_pct) / 100)
ebitda_pct = (ebitda / ricavi_annui) * 100 if ricavi_annui > 0 else 0

# ------------------- OUTPUT -------------------
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("📈 KPI Calcolati")
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Coperti Giornalieri Brunch", coperti_brunch)
    st.metric("Coperti Totali Giornalieri", coperti_tot)
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
with kpi2:
    st.metric("Ricavi Giornalieri Brunch (€)", f"{ricavi_brunch:,.0f}")
    st.metric("Ricavi Giornalieri Totali (€)", f"{ricavi_tot:,.0f}")
    st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,.0f}")
with kpi3:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:,.2f} €/mq")
    st.metric("EBITDA (€)", f"{ebitda:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")