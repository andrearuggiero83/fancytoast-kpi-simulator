import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")

st.title("📊 Fancytoast KPI Simulator")
st.caption("Versione con RevPASH per fascia e calcolo ponderato")

# ------------------ Input base ------------------
st.sidebar.header("🔧 Parametri di base")
posti = st.sidebar.number_input("Posti a sedere", min_value=10, max_value=200, value=70)
ore_totali = st.sidebar.number_input("Ore di apertura giornaliera", min_value=1, max_value=24, value=13)
food_cost = st.sidebar.slider("Food Cost (%)", 0, 100, 27)
labor_cost = st.sidebar.slider("Labor Cost (%)", 0, 100, 32)
opex = st.sidebar.slider("OPEX (%)", 0, 100, 20)
mq = st.sidebar.number_input("Metri quadri somministrazione", min_value=10, value=100)

# ------------------ Fasce orarie ------------------
st.subheader("⏰ Definizione Fasce Orarie")

fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
default_orari = [(8, 12), (10, 16), (16, 18), (18, 21)]
default_atv = [10.0, 25.0, 10.0, 12.5]
default_pesi = [20, 60, 10, 10]

inputs = []
for i, fascia in enumerate(fasce):
    with st.expander(f"{fascia}"):
        col1, col2 = st.columns(2)
        inizio = col1.number_input(f"Orario inizio {fascia}", min_value=0, max_value=23, value=default_orari[i][0], key=f"i_{i}")
        fine = col2.number_input(f"Orario fine {fascia}", min_value=1, max_value=24, value=default_orari[i][1], key=f"f_{i}")
        durata = fine - inizio if fine > inizio else 0
        atv = st.number_input(f"ATV {fascia} (€)", min_value=0.0, value=default_atv[i], step=0.5, key=f"atv_{i}")
        peso = st.slider(f"Incidenza % coperti {fascia}", 0, 100, default_pesi[i], key=f"peso_{i}")
        inputs.append({
            "fascia": fascia,
            "inizio": inizio,
            "fine": fine,
            "durata": durata,
            "atv": atv,
            "peso_pct": peso
        })

# ------------------ Calcoli ------------------
df = pd.DataFrame(inputs)
df["peso_norm"] = df["peso_pct"] / df["peso_pct"].sum()  # normalizzato su 100%
coperti_totali = posti * 1.5  # una rotazione e mezza giornaliera fissa
df["coperti"] = coperti_totali * df["peso_norm"]
df["ricavi"] = df["coperti"] * df["atv"]
df["revpash_fascia"] = df["ricavi"] / (posti * df["durata"]).replace(0, 1)

ricavi_giornalieri = df["ricavi"].sum()
ricavi_annui = ricavi_giornalieri * 365
coperti_annui = df["coperti"].sum() * 365
scontrino_medio_generale = ricavi_giornalieri / df["coperti"].sum() if df["coperti"].sum() > 0 else 0
revpash_medio = ricavi_giornalieri / (posti * ore_totali)
revpasm = ricavi_giornalieri / mq

ebitda_val = ricavi_annui * (1 - (food_cost + labor_cost + opex)/100)
ebitda_pct = (ebitda_val / ricavi_annui) * 100 if ricavi_annui > 0 else 0

# ------------------ Output ------------------
st.subheader("📋 Tabella Fasce Orarie con RevPASH")
st.dataframe(df[["fascia", "inizio", "fine", "durata", "atv", "peso_pct", "coperti", "ricavi", "revpash_fascia"]]
             .rename(columns={
                 "fascia": "Fascia",
                 "inizio": "Ora Inizio",
                 "fine": "Ora Fine",
                 "durata": "Durata (h)",
                 "atv": "ATV (€)",
                 "peso_pct": "% Incidenza",
                 "coperti": "Coperti",
                 "ricavi": "Ricavi (€)",
                 "revpash_fascia": "RevPASH Fascia (€)"
             }).style.format({
                 "Coperti": "{:.0f}",
                 "Ricavi (€)": "€{:.0f}",
                 "ATV (€)": "€{:.2f}",
                 "% Incidenza": "{:.0f}%",
                 "RevPASH Fascia (€)": "€{:.2f}"
             }), use_container_width=True)

st.subheader("📈 KPI Calcolati")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Ricavi Giornalieri (€)", f"{ricavi_giornalieri:,.0f}")
    st.metric("Ricavi Annui (€)", f"{ricavi_annui:,.0f}")
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
with col2:
    st.metric("Scontrino Medio Generale (€)", f"{scontrino_medio_generale:.2f}")
    st.metric("RevPASH Medio (€)", f"{revpash_medio:.2f}")
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f}")
with col3:
    st.metric("EBITDA (€)", f"{ebitda_val:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")