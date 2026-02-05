import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")

# Alustetaan session_state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'nykyinen_lyonti' not in st.session_state:
    st.session_state.nykyinen_lyonti = 1

# --- JOUKKUEIDEN NIMET JA KOKOOPANOT ---
with st.expander("Aseta joukkueet ja pelaajat ennen ottelua", expanded=True):
    col_k, col_v = st.columns(2)
    koti_n = col_k.text_input("Kotijoukkue", "Koti")
    koti_pelaajat = col_k.text_area("Kotijoukkueen pelaajat (1 per rivi)", "Pelaaja 1\nPelaaja 2\nPelaaja 3\nPelaaja 4\nPelaaja 5\nPelaaja 6\nPelaaja 7\nPelaaja 8\nPelaaja 9\nJokeri 10\nJokeri 11\nJokeri 12", height=200).split('\n')
    
    vieras_n = col_v.text_input("Vierasjoukkue", "Vieras")
    vieras_pelaajat = col_v.text_area("Vierasjoukkueen pelaajat (1 per rivi)", "Pelaaja 1\nPelaaja 2\nPelaaja 3\nPelaaja 4\nPelaaja 5\nPelaaja 6\nPelaaja 7\nPelaaja 8\nPelaaja 9\nJokeri 10\nJokeri 11\nJokeri 12", height=200).split('\n')

# Varmistetaan että listoissa on 12 nimeä
koti_pelaajat = (koti_pelaajat + [""] * 12)[:12]
vieras_pelaajat = (vieras_pelaajat + [""] * 12)[:12]

# --- TILANNE JA PALOT (PAINONAPIT) ---
st.subheader("Ottelun tilanne")
t_col1, t_col2 = st.columns([3, 1])

with t_col1:
    kaikki_tilanteet = ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
    tilanne = st.radio("Valitse tilanne", kaikki_tilanteet, horizontal=True)

with t_col2:
    palot = st.radio("Palot", ["0", "1", "2", "3"], horizontal=True)

st.divider()

# --- SYÖTTÖALUE ---
col_lyoja, col_laatu, col_tulos = st.columns([1.5, 2, 1.5])

with col_lyoja:
    st.subheader("🏃 Lyöjä")
    valittu_joukkue = st.radio("Vuorossa", [koti_n, vieras_n], horizontal=True)
    nimet = koti_pelaajat if valittu_joukkue == koti_n else vieras_pelaajat
    lyoja_nimi = st.selectbox("Valitse pelaaja", nimet)
    
    st.session_state.nykyinen_lyonti = st.radio("Lyönti nro", [1, 2, 3], index=st.session_state.nykyinen_lyonti-1, horizontal=True)

with col_laatu:
    st.subheader("🏟️ Lyönti")
    m_col, t_col = st.columns(2)
    merkki = m_col.radio("Merkki", ["Vapaa", "Merkattu"], horizontal=True)
    tyyppi = t_col.selectbox("Lyönti-tyyppi", ["Kova", "Kumura", "Pomppu", "Pieni", "Pussari", "Varsi"])
    
    suunnat = ["3 Jatke", "Keskitaakse", "2 Jatke", "3 Luukku", "Keskisauma", "2 Luukku", "3 Raja", "Pieni", "2 Raja"]
    suunta = st.radio("Lyönnin suunta", suunnat, horizontal=True)
    takapalo = st.checkbox("TAKAPALO ⚠️")

with col_tulos:
    st.subheader("🏁 Tulos")
    tulos_lista = ["PALO", "HAAVA", "LAITON", "TUOTTAMATON", "KENTÄLLEMENO", "VAIHTO", "ETENI", "JUOKSU"]
    tulos = st.radio("Valitse lopputulos", tulos_lista)
    
    onnistui = tulos in ["JUOKSU", "VAIHTO", "KENTÄLLEMENO", "ETENI"]
    suoritus = "Onnistunut" if onnistui else "Epäonnistunut"

    if st.button("TALLENNA TAPAHTUMA", type="primary", use_container_width=True):
        uusi_rivi = {
            "Jakso": "1. Jakso", "Vuoro": "1. Aloittava", "Palot": palot, 
            "Tilanne": tilanne, "Joukkue": valittu_joukkue, "Lyöjä": lyoja_nimi, 
            "L-Nro": st.session_state.nykyinen_lyonti, "Merkki": merkki, "Tyyppi": tyyppi, 
            "Suunta": suunta, "Tulos": tulos, "Suoritus": suoritus, 
            "Takapalo": "TAKAPALO" if takapalo else "-"
        }
        
        st.session_state.data = pd.concat([pd.DataFrame([uusi_rivi]), st.session_state.data], ignore_index=True)
        # Automaattinen lyöntinumeron vaihto (1->2->3->1)
        st.session_state.nykyinen_lyonti = (st.session_state.nykyinen_lyonti % 3) + 1
        st.rerun()

# --- LOKI JA LATAUS ---
st.divider()
st.subheader("Viimeisimmät tapahtumat")
st.dataframe(st.session_state.data.head(10), use_container_width=True)

# Latausnappi
csv = st.session_state.data.to_csv(index=False, encoding="utf-8-sig")
st.download_button(label="📥 Lataa CSV", data=csv, file_name=f"pesis_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
