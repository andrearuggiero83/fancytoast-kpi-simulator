import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")

st.title("📊 Fancytoast KPI Simulator")
st.write("Simula le performance economiche modificando i parametri di input")

st.header("🛠️ Parametri di Input")

col1, col2, col3 = st.columns(3)
with col1:
    revpash = st.number_input("RevPASH (€)", value=5.00, step=0.5)
    scontrino_medio = st.number_input("Scontrino medio (€)", value=25.0, step=1.0)
    food_cost = st.number_input("Food Cost (%)", value=27, step=1)
with col2:
    ore_brunch = st.number_input("Ore operative brunch", value=6, step=1)
    posti_sedere = st.number_input("Posti a sedere", value=70, step=1)
    labor_cost = st.number_input("Labor Cost (%)", value=32, step=1)
with col3:
    opex = st.number_input("OPEX (%)", value=20, step=1)

st.divider()
st.subheader("⏰ Calcolo Totale Giornaliero dalle Fasce Orarie")

fasce = pd.DataFrame({
    "Fasce Orarie": ["Mattino", "Brunch", "Snack", "Aperitivo"],
    "Ore": ["8,00 -10,00", "10,00-16,00", "16,00-18,00", "18,00-21,00"],
    "% Coperti": [0.4, 0.6, 0.4, 0.5],
    "ATV": [10, 25, 10, 12.5],
})

fasce_edit = st.data_editor(fasce, num_rows="fixed", use_container_width=True)

fasce_edit["Coperti"] = (fasce_edit["% Coperti"] * posti_sedere).round()
fasce_edit["Ricavi"] = (fasce_edit["Coperti"] * fasce_edit["ATV"]).round()

coperti_brunch = int(fasce_edit.loc[fasce_edit["Fasce Orarie"] == "Brunch", "Coperti"].values[0])
ricavi_brunch = int(fasce_edit.loc[fasce_edit["Fasce Orarie"] == "Brunch", "Ricavi"].values[0])
coperti_tot = int(fasce_edit["Coperti"].sum())
ricavi_tot = int(fasce_edit["Ricavi"].sum())
coperti_annui = int(coperti_tot * 365)
ricavi_annui = int(ricavi_tot * 365)

revpasm = ricavi_tot / 60  # 60 mq fissi
ebitda_val = ricavi_annui * (1 - (food_cost + labor_cost + opex) / 100)
ebitda_pct = (ebitda_val / ricavi_annui) * 100

st.divider()
st.subheader("📈 KPI Calcolati")
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Coperti Giornalieri Brunch", coperti_brunch)
    st.metric("Coperti Totali Giornalieri", coperti_tot)
    st.metric("Ricavi Giornalieri Brunch (€)", f"{ricavi_brunch:,}".replace(",", "."))
with col_b:
    st.metric("Ricavi Giornalieri Totali (€)", f"{ricavi_tot:,}".replace(",", "."))
    st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,}".replace(",", "."))
    st.metric("Coperti Annui", f"{coperti_annui:,}".replace(",", "."))
with col_c:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
    st.metric("EBITDA (€)", f"{ebitda_val:,.0f}".replace(",", "."))
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")