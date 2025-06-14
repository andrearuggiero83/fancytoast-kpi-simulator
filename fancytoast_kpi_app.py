
import streamlit as st

st.set_page_config(page_title="Fancytoast KPI Simulator", layout="wide")

# Logo e Titolo
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("https://raw.githubusercontent.com/andrearuggiero83/fancytoast-kpi-simulator/main/LOGO_Fancytoast.png", width=100)
with col_title:
    st.title("📊 Fancytoast KPI Simulator")
    st.caption("Simula le performance economiche modificando i parametri di input")

# Input base
st.header("🛠️ Parametri di Input")
col1, col2, col3 = st.columns(3)
with col1:
    revpash = st.number_input("RevPASH (€)", value=5.0, min_value=0.0, step=0.1)
    scontrino_medio = st.number_input("Scontrino medio (€)", value=25.0, min_value=0.0, step=1.0)
    food_cost = st.number_input("Food Cost (%)", value=27, min_value=0, max_value=100)
with col2:
    ore_brunch = st.number_input("Ore operative brunch", value=6, min_value=1)
    posti = st.number_input("Posti a sedere", value=70, min_value=10)
    labor_cost = st.number_input("Labor Cost (%)", value=32, min_value=0, max_value=100)
with col3:
    opex = st.number_input("OPEX (%)", value=20, min_value=0, max_value=100)
    mq_somministrazione = st.number_input("Metri quadri somministrazione", value=100, min_value=1)

# Calcolo coperti giornalieri brunch
coperti_brunch = revpash * ore_brunch * posti
ricavi_brunch = coperti_brunch * scontrino_medio

st.header("⏰ Calcolo Totale Giornaliero dalle Fasce Orarie")
fasce = ["Mattino", "Brunch", "Snack", "Aperitivo"]
ore_fasce_default = ["8:00-10:00", "10:00-16:00", "16:00-18:00", "18:00-21:00"]

col_matt, col_brunch, col_snack, col_ape = st.columns(4)
with col_matt:
    orario_mattino = st.text_input("Mattino", ore_fasce_default[0])
    perc_mattino = st.number_input("% Coperti Mattino", min_value=0, max_value=100, value=40)
with col_brunch:
    st.text_input("Brunch", ore_fasce_default[1], disabled=True)
    perc_brunch = st.number_input("% Coperti Brunch", min_value=0, max_value=100, value=60)
with col_snack:
    orario_snack = st.text_input("Snack", ore_fasce_default[2])
    perc_snack = st.number_input("% Coperti Snack", min_value=0, max_value=100, value=40)
with col_ape:
    orario_ape = st.text_input("Aperitivo", ore_fasce_default[3])
    perc_ape = st.number_input("% Coperti Aperitivo", min_value=0, max_value=100, value=50)

col_atv = st.columns(4)
atv_values = [col_atv[i].number_input(f"ATV {fasce[i]} (€)", min_value=0.0, value=float(val), step=0.5)
              for i, val in enumerate([10.0, 25.0, 10.0, 12.5])]

percentuali = [perc_mattino, perc_brunch, perc_snack, perc_ape]
coperti_totali = []
ricavi_totali = []

for i in range(4):
    coperti = coperti_brunch * (percentuali[i] / 100)
    ricavi = coperti * atv_values[i]
    coperti_totali.append(coperti)
    ricavi_totali.append(ricavi)

coperti_giornalieri_totali = sum(coperti_totali)
ricavi_giornalieri_totali = sum(ricavi_totali)
ricavi_annui = ricavi_giornalieri_totali * 365
coperti_annui = coperti_giornalieri_totali * 365

revpasm = ricavi_giornalieri_totali / mq_somministrazione

ebitda_val = ricavi_annui * (1 - (food_cost + labor_cost + opex) / 100)
ebitda_pct = (ebitda_val / ricavi_annui) * 100 if ricavi_annui > 0 else 0

# KPI Output
st.header("📈 KPI Calcolati")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Coperti Giornalieri Brunch", f"{coperti_brunch:.0f}")
    st.metric("Coperti Totali Giornalieri", f"{coperti_giornalieri_totali:.0f}")
    st.metric("Ricavi Giornalieri Brunch (€)", f"{ricavi_brunch:,.0f}")
with col2:
    st.metric("Ricavi Giornalieri Totali (€)", f"{ricavi_giornalieri_totali:,.0f}")
    st.metric("Ricavi Annui Totali (€)", f"{ricavi_annui:,.0f}")
    st.metric("Coperti Annui", f"{coperti_annui:,.0f}")
with col3:
    st.metric("RevPASM (€ / mq / giorno)", f"{revpasm:.2f} €/mq")
    st.metric("EBITDA (€)", f"{ebitda_val:,.0f}")
    st.metric("EBITDA %", f"{ebitda_pct:.1f}%")
