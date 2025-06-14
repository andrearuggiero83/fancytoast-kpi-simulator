
import streamlit as st

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")
st.image("https://raw.githubusercontent.com/andrearuggiero83/fancytoast-kpi-simulator/main/logo_fancytoast.png", width=250)

st.title("📊 Fancytoast KPI Simulator")
st.markdown("Simula le performance economiche modificando i parametri di input")

st.header("🔧 Parametri di Input")
col1, col2, col3 = st.columns(3)

with col1:
    revpash = st.number_input("RevPASH (€)", value=5.0)
    scontrino_medio = st.number_input("Scontrino medio (€)", value=25.0)
    food_cost_pct = st.number_input("Food Cost (%)", value=27) / 100

with col2:
    ore_brunch = st.number_input("Ore operative brunch", value=6)
    posti_sedere = st.number_input("Posti a sedere", value=70)
    labor_cost_pct = st.number_input("Labor Cost (%)", value=32) / 100

with col3:
    opex_pct = st.number_input("OPEX (%)", value=20) / 100

st.divider()
st.subheader("🎯 Calcolo Totale Giornaliero dalle fasce orarie")

fasce = [
    {"fascia": "Mattino", "ore": 2, "peso": 0.40, "atv": 10},
    {"fascia": "Brunch", "ore": 6, "peso": 0.60, "atv": scontrino_medio},
    {"fascia": "Snack", "ore": 2, "peso": 0.40, "atv": 10},
    {"fascia": "Aperitivo", "ore": 3, "peso": 0.50, "atv": 12.5},
]

coperti_giornalieri = 0
ricavi_giornalieri = 0

for f in fasce:
    coperti_fascia = round(posti_sedere * f["peso"])
    ricavi_fascia = coperti_fascia * f["atv"]
    coperti_giornalieri += coperti_fascia
    ricavi_giornalieri += ricavi_fascia

ricavi_annui = ricavi_giornalieri * 365
coperti_annui = coperti_giornalieri * 365
mq_somministrazione = posti_sedere * 1.4
revpasm = ricavi_giornalieri / mq_somministrazione
ebitda = ricavi_annui * (1 - food_cost_pct - labor_cost_pct - opex_pct)
ebitda_pct = ebitda / ricavi_annui

st.divider()
st.header("📈 KPI Calcolati")

col1, col2 = st.columns(2)

with col1:
    st.metric("Coperti Giornalieri Brunch", f"{posti_sedere * ore_brunch * revpash / scontrino_medio:.0f}")
    st.metric("Coperti Totali Giornalieri", f"{coperti_giornalieri}")
    st.metric("Ricavi Giornalieri Brunch (€)", f"€ {posti_sedere * ore_brunch * revpash:,.0f}")
    st.metric("Ricavi Giornalieri Totali (€)", f"€ {ricavi_giornalieri:,.0f}")
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")

with col2:
    st.metric("Ricavi Annui Totali (€)", f"€ {ricavi_annui:,.0f}")
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
    st.metric("EBITDA (€)", f"€ {ebitda:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct*100:.1f}%")
