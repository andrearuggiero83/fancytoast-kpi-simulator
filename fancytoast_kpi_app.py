import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", page_icon="📊", layout="centered")
st.title("📊 Fancytoast KPI Simulator")
st.caption("Simula le performance economiche modificando i parametri di input")

# ------------------------------
# INPUT PARAMETRI GENERALI
# ------------------------------
st.header("🔧 Parametri di Input")
col1, col2, col3 = st.columns(3)

with col1:
    revpash = st.number_input("RevPASH (€)", min_value=0.0, value=5.0, step=0.1)
    atv = st.number_input("Scontrino medio (€)", min_value=0.0, value=25.0, step=0.5)
    food_cost = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27)

with col2:
    brunch_hours = st.number_input("Ore operative brunch", min_value=1, max_value=12, value=6)
    seats = st.number_input("Posti a sedere", min_value=1, value=70)
    labor_cost = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32)

with col3:
    opex = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20)

# ------------------------------
# INPUT FASCE ORARIE
# ------------------------------
st.markdown("---")
st.subheader("⏱️ Calcolo Totale Giornaliero dalle Fasce Orarie")

fascia_labels = ["Mattino", "Brunch", "Snack", "Aperitivo"]
fascia_orari = ["8:00 - 10:00", "10:00 - 16:00", "16:00 - 18:00", "18:00 - 21:00"]
fascia_inputs = []

for i, label in enumerate(fascia_labels):
    st.markdown(f"**{label} ({fascia_orari[i]})**")
    cols = st.columns(2)
    perc = cols[0].number_input(f"% Coperti - {label}", min_value=0.0, max_value=1.0,
                                value=0.25 if label != "Brunch" else 0.5, step=0.05, key=f"perc_{label}")
    fascia_atv = cols[1].number_input(f"ATV (€) - {label}", min_value=1.0, max_value=100.0,
                                      value=atv if label == "Brunch" else 10.0, step=0.5, key=f"atv_{label}")
    fascia_inputs.append({"nome": label, "orario": fascia_orari[i], "perc": perc, "atv": fascia_atv})

# ------------------------------
# CALCOLI BASE
# ------------------------------
coperti_giornalieri_brunch = round(revpash * seats * brunch_hours / atv)
table_turnover = coperti_giornalieri_brunch / seats

fasce_df = pd.DataFrame(fascia_inputs)
fasce_df["Coperti"] = (coperti_giornalieri_brunch * fasce_df["perc"]).round()
fasce_df["Ricavi"] = (fasce_df["Coperti"] * fasce_df["atv"]).round(2)

st.dataframe(fasce_df, use_container_width=True)

coperti_totali = int(fasce_df["Coperti"].sum())
ricavi_totali = float(fasce_df["Ricavi"].sum())
coperti_annui = coperti_totali * 365
ricavi_annui = ricavi_totali * 365
revpasm = ricavi_totali / 60  # €/mq/giorno (60 mq fissi)

ebitda = ricavi_annui * (1 - (food_cost + labor_cost + opex) / 100)
ebitda_pct = ebitda / ricavi_annui if ricavi_annui else 0

# ------------------------------
# KPI CALCOLATI
# ------------------------------
st.markdown("---")
st.header("📈 KPI Calcolati")

col1, col2 = st.columns(2)
with col1:
    st.metric("Coperti Giornalieri Brunch", f"{coperti_giornalieri_brunch}")
    st.metric("Table Sit Turn Over", f"{table_turnover:.2f}")
    st.metric("Coperti Totali Giornalieri", f"{coperti_totali}")
    st.metric("Ricavi Giornalieri Brunch (€)", f"€ {coperti_giornalieri_brunch * atv:,.0f}")
    st.metric("Ricavi Giornalieri Totali (€)", f"€ {ricavi_totali:,.0f}")

with col2:
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
    st.metric("Ricavi Annui Totali (€)", f"€ {ricavi_annui:,.0f}")
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
    st.metric("EBITDA (€)", f"€ {ebitda:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct * 100:.1f}%")