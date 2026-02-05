import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")

# Alustetaan session_state, jotta valinnat pysyvät muistissa
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])

# --- YLÄPALKKI ---
st.title("⚾ Pesis-Tilastoija Web v11.33")

with st.container():
    c1, c2, c3, c4 = st.columns([1, 1, 2, 1])
    with c1:
        koti = st.text_input("Kotijoukkue", "Koti")
    with c2:
        vieras = st.text_input("Vierasjoukkue", "Vieras")
    with c3:
        # Alkuperäiset tilanteet
        kaikki_tilanteet = ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
        tilanne = st.select_slider("Tilanne", options=kaikki_tilanteet)
    with c4:
        palot = st.selectbox("Palot", ["0", "1", "2", "3"])

st.divider()

# --- SYÖTTÖALUE ---
col_pelaaja, col_lyonti, col_tulos = st.columns([1, 1.5, 1])

with col_pelaaja:
    st.subheader("🏃 Pelaaja")
    joukkue = st.radio("Lyövä joukkue", [koti, vieras])
    lyoja_nro = st.number_input("Pelaaja nro", 1, 12, 1)
    # Lyöntinumeron rullaus 1-3
    lyonti_nro = st.radio("Lyönti", [1, 2, 3], horizontal=True)

with col_lyonti:
    st.subheader("🏟️ Lyönnin laatu")
    m1, m2 = st.columns(2)
    merkki = m1.radio("Merkki", ["Vapaa", "Merkattu"])
    # Alkuperäiset tyypit
    tyyppi = m2.selectbox("Tyyppi", ["Kova", "Kumura", "Pomppu", "Pieni", "Pussari", "Varsi"])
    
    # Alkuperäiset suunnat
    suunnat = ["3 Jatke", "Keskitaakse", "2 Jatke", "3 Luukku", "Keskisauma", "2 Luukku", "3 Raja", "Pieni", "2 Raja"]
    suunta = st.select_slider("Suunta", options=suunnat)
    
    takapalo = st.checkbox("⚠️ TAKAPALO")

with col_tulos:
    st.subheader("🏁 Tulos")
    # Alkuperäinen tuloslista ja värit logiikasta
    t_lista = ["PALO", "HAAVA", "LAITON", "TUOTTAMATON", "KENTÄLLEMENO", "VAIHTO", "ETENI", "JUOKSU"]
    tulos = st.radio("Valitse tulos", t_lista)
    
    # Automaattinen suoritus-päätelmä
    onnistui = tulos in ["JUOKSU", "VAIHTO", "KENTÄLLEMENO", "ETENI"]
    suoritus = "Onnistunut" if onnistui else "Epäonnistunut"
    st.info(f"Suoritus: {suoritus}")

    if st.button("TALLENNA TAPAHTUMA", type="primary", use_container_width=True):
        uusi_rivi = {
            "Jakso": "1. Jakso", "Vuoro": "1. Aloittava", "Palot": palot, 
            "Tilanne": tilanne, "Joukkue": joukkue, "Lyöjä": f"P{lyoja_nro}", 
            "L-Nro": lyonti_nro, "Merkki": merkki, "Tyyppi": tyyppi, 
            "Suunta": suunta, "Tulos": tulos, "Suoritus": suoritus, 
            "Takapalo": "TAKAPALO" if takapalo else "-"
        }
        
        st.session_state.data = pd.concat([pd.DataFrame([uusi_rivi]), st.session_state.data], ignore_index=True)
        st.success(f"Tallennettu: P{lyoja_nro} -> {tulos}")

# --- LOKI JA LATAUS ---
st.divider()
st.subheader("Ottelun loki")
st.dataframe(st.session_state.data, use_container_width=True)

# CSV Latauspainike
csv = st.session_state.data.to_csv(index=False, encoding="utf-8-sig")
st.download_button(
    label="📥 Lataa otteludata CSV-tiedostona",
    data=csv,
    file_name=f"ottelu_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
)
