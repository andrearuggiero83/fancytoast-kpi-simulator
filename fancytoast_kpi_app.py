
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")

# Logo
col1, col2 = st.columns([1, 10])
with col1:
    st.image("https://fancytoast.it/wp-content/uploads/2023/11/Fancytoast_Logo_2023.png", width=80)
with col2:
    st.title("Fancytoast KPI Simulator")
    st.caption("Simula le performance economiche modificando i parametri di input")

st.markdown("## 🛠️ Parametri di Input")

col1, col2, col3 = st.columns(3)
with col1:
    revpash = st.number_input("RevPASH (€)", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    scontrino_medio = st.number_input("Scontrino medio (€)", min_value=5.0, max_value=50.0, value=25.0, step=0.5)
    food_cost = st.number_input("Food Cost (%)", min_value=0, max_value=100, value=27, step=1)
with col2:
    ore_brunch = st.number_input("Ore operative brunch", min_value=1, max_value=12, value=6)
    posti_a_sedere = st.number_input("Posti a sedere", min_value=10, max_value=200, value=70)
    labor_cost = st.number_input("Labor Cost (%)", min_value=0, max_value=100, value=32, step=1)
with col3:
    opex = st.number_input("OPEX (%)", min_value=0, max_value=100, value=20, step=1)
    mq_somministrazione = st.number_input("Metri quadri somministrazione", min_value=10, max_value=500, value=100, step=5)

# Fasce orarie
st.markdown("## ⏰ Calcolo Totale Giornaliero dalle Fasce Orarie")
fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
ore = ["8,00 -10,00", "10,00-16,00", "16,00-18,00", "18,00-21,00"]

perc_coperti = []
atv = []

cols = st.columns(4)
for i in range(len(fasce)):
    with cols[0]:
        st.markdown(f"**{fasce[i]}**")
    with cols[1]:
        st.markdown(f"{ore[i]}")
    with cols[2]:
        perc = st.number_input(f"% Coperti {fasce[i]}", min_value=0.0, max_value=1.0, value=[0.4, 0.6, 0.4, 0.5][i], step=0.1, key=f"perc_{i}")
        perc_coperti.append(perc)
    with cols[3]:
        atv_input = st.number_input(f"ATV {fasce[i]} (€)", min_value=0.0, max_value=50.0, value=[10.0, 25.0, 10.0, 12.5][i], step=0.5, key=f"atv_{i}")
        atv.append(atv_input)

# Calcoli
coperti_brunch = posti_a_sedere * ore_brunch * revpash / scontrino_medio
table_turnover = coperti_brunch / posti_a_sedere
coperti_per_fascia = [round(coperti_brunch * p) for p in perc_coperti]
ricavi_per_fascia = [c * a for c, a in zip(coperti_per_fascia, atv)]

coperti_totali = sum(coperti_per_fascia)
ricavi_totali = sum(ricavi_per_fascia)
ricavi_annui = ricavi_totali * 305
coperti_annui = coperti_totali * 305
revpasm = ricavi_totali / mq_somministrazione
ebitda = ricavi_totali * (1 - (food_cost + labor_cost + opex)/100)
ebitda_percent = ebitda / ricavi_totali * 100 if ricavi_totali else 0

# Tabella
df = pd.DataFrame({
    "Fasce Orarie": fasce,
    "Ore": ore,
    "% Coperti": perc_coperti,
    "ATV (€)": atv,
    "Coperti": coperti_per_fascia,
    "Ricavi (€)": ricavi_per_fascia
})

st.dataframe(df, use_container_width=True)

st.markdown("## 📈 KPI Calcolati")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coperti Giornalieri Brunch", round(coperti_brunch))
    st.metric("Ricavi Giornalieri Brunch (€)", f"{coperti_brunch * scontrino_medio:,.0f}")
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
with col2:
    st.metric("Coperti Totali Giornalieri", int(coperti_totali))
    st.metric("Ricavi Giornalieri Totali (€)", f"{ricavi_totali:,.0f}")
    st.metric("EBITDA (€)", f"{ebitda:,.0f}")
with col3:
    st.metric("Coperti Annui", int(coperti_annui))
    st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,.0f}")
    st.metric("EBITDA %", f"{ebitda_percent:.1f}%")
