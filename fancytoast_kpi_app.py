import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", page_icon="📈", layout="wide")

st.title("\U0001F4C8 Fancytoast KPI Simulator")
st.write("Simula le performance economiche modificando i parametri di input")

st.markdown("---")
st.header("🛠️ Parametri di Input")

col1, col2, col3 = st.columns(3)
with col1:
    revpash = st.number_input("RevPASH (€)", min_value=0.0, value=5.0, step=0.5)
    scontrino_medio = st.number_input("Scontrino medio (€)", min_value=0.0, value=25.0, step=1.0)
    food_cost_pct = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27, step=1)
with col2:
    ore_brunch = st.number_input("Ore operative brunch", min_value=1, max_value=24, value=6)
    posti_a_sedere = st.number_input("Posti a sedere", min_value=1, value=70)
    labor_cost_pct = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32, step=1)
with col3:
    opex_pct = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20, step=1)
    mq_somministrazione = st.number_input("Metri quadri somministrazione", min_value=1, value=100)
    ore_totali = st.number_input("Ore di apertura giornaliera", min_value=1, max_value=24, value=13)

st.markdown("---")
st.header("⏰ Calcolo Totale Giornaliero dalle Fasce Orarie")

fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
ore_fasce = [
    st.text_input("Mattino", "8:00-10:00"),
    "10:00-16:00",  # brunch fisso
    st.text_input("Snack", "16:00-18:00"),
    st.text_input("Aperitivo", "18:00-21:00")
]

durata_fasce = [2, ore_brunch, 2, 3]  # ore stimate per ogni fascia

totore = sum(durata_fasce)
quota_oraria = [d / totore for d in durata_fasce]

coperti_totali_giornalieri = posti_a_sedere * ore_totali * revpash / scontrino_medio
coperti_fasce = [coperti_totali_giornalieri * q for q in quota_oraria]

coperti_pct_values = []
coperti_cols = st.columns(4)
for i, fascia in enumerate(fasce):
    with coperti_cols[i]:
        pct = st.number_input(f"% Coperti {fascia}", min_value=0, max_value=100, value=[40, 60, 40, 50][i], step=5)
        coperti_pct_values.append(pct / 100)

atv_values = []
atv_cols = st.columns(4)
for i, fascia in enumerate(fasce):
    with atv_cols[i]:
        val = st.number_input(f"ATV {fascia} (€)", min_value=0.0, value=[10.0, 25.0, 10.0, 12.5][i], step=0.5)
        atv_values.append(val)

coperti_effettivi = [coperti_fasce[i] * coperti_pct_values[i] for i in range(4)]
ricavi_fasce = [coperti_effettivi[i] * atv_values[i] for i in range(4)]

ricavi_giornalieri_totali = sum(ricavi_fasce)
ricavi_annui = ricavi_giornalieri_totali * 365
coperti_annui = sum(coperti_effettivi) * 365
revpasm = ricavi_giornalieri_totali / mq_somministrazione

costo_materie_prime = ricavi_annui * (food_cost_pct / 100)
costo_personale = ricavi_annui * (labor_cost_pct / 100)
costi_opex = ricavi_annui * (opex_pct / 100)

ebitda = ricavi_annui - costo_materie_prime - costo_personale - costi_opex
ebitda_pct = (ebitda / ricavi_annui) * 100 if ricavi_annui > 0 else 0

# Tabella riassuntiva
df_fasce = pd.DataFrame({
    "Fasce Orarie": fasce,
    "Ore": ore_fasce,
    "Durata (h)": durata_fasce,
    "% Coperti": [int(v * 100) for v in coperti_pct_values],
    "ATV (€)": atv_values,
    "Coperti": coperti_effettivi,
    "Ricavi": ricavi_fasce
})

st.dataframe(df_fasce.style.format({"% Coperti": "{:.0f}%", "ATV (€)": "{:.2f}", "Coperti": "{:.0f}", "Ricavi": "{:.0f}"}))

st.markdown("---")
st.header("📉 KPI Calcolati")

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric("Coperti Totali Giornalieri", f"{sum(coperti_effettivi):.0f}")
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
with kpi2:
    st.metric("Ricavi Giornalieri Totali (€)", f"{ricavi_giornalieri_totali:,.0f}")
    st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,.0f}")
with kpi3:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
    st.metric("EBITDA (€)", f"{ebitda:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")
