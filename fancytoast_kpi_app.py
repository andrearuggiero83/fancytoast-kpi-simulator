import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fancytoast KPI Simulator – CTR & KPI", layout="wide")

st.title("📊 Fancytoast KPI Simulator – CTR & KPI")
st.caption("Simula l’efficienza operativa del tuo punto vendita Fancytoast")

# ------------------ ISTRUZIONI ------------------
with st.expander("ℹ️ Come funziona il simulatore"):
    st.markdown("""
    Questo strumento ti permette di simulare l’andamento economico di un punto vendita **Fancytoast**, configurando:

    - 🪑 **Posti a sedere**
    - ⏰ **Fasce orarie operative**
    - 🔁 **CTR (Cover Turnover Rate)** per fascia → quante volte ogni posto viene utilizzato
    - 📊 **Incidenza % coperti per fascia**
    - 💶 **ATV (Average Ticket Value)** per fascia → scontrino medio stimato

    ---
    🔢 Il sistema calcola:
    - 👥 Coperti giornalieri totali e per fascia
    - 💰 Ricavi giornalieri e annui
    - 📈 RevPASH per fascia e medio (€/posto/ora)
    - 📏 RevPASM: € per metro quadro di somministrazione al giorno
    - 📉 EBITDA assoluto e in %

    Puoi personalizzare ogni voce e osservare in tempo reale l’impatto sulle performance.
    """)

with st.expander("📘 Legenda KPI"):
    st.markdown("""
    - **Coperti Giornalieri Totali** → somma dei coperti generati in tutte le fasce orarie
    - **Coperti Annui** → coperti giornalieri × 365
    - **Ricavi Giornalieri / Annui** → somma dei ricavi stimati per fascia
    - **Scontrino Medio Generale (€)** → media ponderata degli ATV in base ai coperti
    - **RevPASH per fascia (€)** → Ricavi fascia / (Posti × Ore fascia)
    - **RevPASH Medio (€)** → Ricavi totali / (Posti × Ore apertura)
    - **RevPASM (€ / mq / giorno)** → Ricavi totali / Metri quadri somministrazione
    - **EBITDA (€)** → Ricavi annui – Costi Food – Costi Labor – OPEX
    - **EBITDA %** → Margine operativo lordo in % sui ricavi

    Tutti i calcoli si aggiornano automaticamente quando modifichi i parametri nella colonna sinistra.
    """)

# ------------------ INPUT ------------------
st.sidebar.header("🔧 Parametri di base")
posti = st.sidebar.number_input("Posti a sedere", min_value=10, max_value=200, value=70)
food_cost = st.sidebar.slider("Food Cost (%)", 0, 100, 27)
labor_cost = st.sidebar.slider("Labor Cost (%)", 0, 100, 32)
opex = st.sidebar.slider("OPEX (%)", 0, 100, 20)
mq = st.sidebar.number_input("Metri quadri somministrazione", min_value=10, value=100)

# ------------------ Fasce orarie e CTR ------------------
st.subheader("⏰ Definizione Fasce Orarie")

fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
default_orari = [(8, 12), (10, 16), (16, 18), (18, 21)]
default_atv = [10.0, 25.0, 10.0, 12.5]
default_ctr = [0.5, 1.2, 0.3, 0.6]
default_pesi = [20, 60, 10, 10]

inputs = []
for i, fascia in enumerate(fasce):
    with st.expander(f"{fascia}"):
        col1, col2, col3 = st.columns(3)
        inizio = col1.number_input(f"Inizio {fascia}", min_value=0, max_value=23, value=default_orari[i][0], key=f"i_{i}")
        fine = col2.number_input(f"Fine {fascia}", min_value=1, max_value=24, value=default_orari[i][1], key=f"f_{i}")
        durata = fine - inizio if fine > inizio else 0
        atv = col3.number_input(f"ATV {fascia} (€)", min_value=0.0, value=default_atv[i], step=0.5, key=f"atv_{i}")
        ctr = st.slider(f"CTR (Cover Turnover) {fascia}", min_value=0.0, max_value=3.0, value=default_ctr[i], step=0.1, key=f"ctr_{i}")
        peso = st.slider(f"% Coperti {fascia}", 0, 100, default_pesi[i], key=f"peso_{i}")
        inputs.append({
            "fascia": fascia,
            "inizio": inizio,
            "fine": fine,
            "durata": durata,
            "atv": atv,
            "ctr": ctr,
            "peso_pct": peso
        })

# ------------------ Calcoli ------------------
df = pd.DataFrame(inputs)
df["coperti_fascia_lordi"] = posti * df["ctr"]
coperti_totali = df["coperti_fascia_lordi"].sum()

peso_somma = df["peso_pct"].sum()
df["peso_norm"] = df["peso_pct"] / peso_somma if peso_somma > 0 else 0
df["coperti"] = coperti_totali * df["peso_norm"]
df["ricavi"] = df["coperti"] * df["atv"]
df["revpash_fascia"] = df["ricavi"] / (posti * df["durata"]).replace(0, 1)

ricavi_giornalieri = df["ricavi"].sum()
ricavi_annui = ricavi_giornalieri * 365
coperti_annui = df["coperti"].sum() * 365
scontrino_medio_generale = ricavi_giornalieri / df["coperti"].sum() if df["coperti"].sum() > 0 else 0
revpash_medio = ricavi_giornalieri / (posti * df["durata"].sum())
revpasm = ricavi_giornalieri / mq

ebitda_val = ricavi_annui * (1 - (food_cost + labor_cost + opex)/100)
ebitda_pct = (ebitda_val / ricavi_annui) * 100 if ricavi_annui > 0 else 0

# ------------------ Output ------------------
st.subheader("📋 Tabella Fasce Orarie con CTR & RevPASH")
st.dataframe(df[["fascia", "durata", "ctr", "peso_pct", "coperti", "atv", "ricavi", "revpash_fascia"]]
             .rename(columns={
                 "fascia": "Fascia",
                 "durata": "Durata (h)",
                 "ctr": "CTR",
                 "peso_pct": "% Coperti",
                 "coperti": "Coperti",
                 "atv": "ATV (€)",
                 "ricavi": "Ricavi (€)",
                 "revpash_fascia": "RevPASH Fascia (€)"
             }).style.format({
                 "Coperti": "{:.0f}",
                 "Ricavi (€)": "€{:.0f}",
                 "ATV (€)": "€{:.2f}",
                 "% Coperti": "{:.0f}%",
                 "CTR": "{:.1f}",
                 "RevPASH Fascia (€)": "€{:.2f}"
             }), use_container_width=True)

st.subheader("📈 KPI Calcolati")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coperti Totali Giornalieri", f"{coperti_totali:.0f}")
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
    st.metric("Ricavi Giornalieri (€)", f"{ricavi_giornalieri:,.0f}")
with col2:
    st.metric("Ricavi Annui (€)", f"{ricavi_annui:,.0f}")
    st.metric("Scontrino Medio (€)", f"{scontrino_medio_generale:.2f}")
    st.metric("RevPASH Medio (€)", f"{revpash_medio:.2f}")
with col3:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f}")
    st.metric("EBITDA (€)", f"{ebitda_val:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")