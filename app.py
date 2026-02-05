import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis Live v2.0", layout="wide")

# Alustetaan muisti
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'valittu_lyoja' not in st.session_state:
    st.session_state.valittu_lyoja = ""
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = ""

# --- TIEDOT EXCELISTÄ ---
tulokset = ["palo", "haava", "eteni", "tuottamaton", "onnistunut kentällemeno", "laiton", "vaihto", "takapalo", "takaeteneminen", "juoksu"]
lyonnit = ["Pieni", "Pomppu", "Pussari", "Varsi", "Merkattu kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"]

# --- 1. KIINTEÄT OTTELUTIEDOT (Yläpalkki) ---
with st.sidebar:
    st.header("Ottelun asetukset")
    pvm = st.date_input("Päivämäärä", datetime.now())
    koti_n = st.text_input("Kotijoukkue", "Kotijoukkue")
    vieras_n = st.text_input("Vierasjoukkue", "Vierailija")
    sarja = st.text_input("Sarja", "MSU")
    up_kuvio = st.selectbox("UP-KUVIO", ["MIKE", "PERTSA", "PYP"])
    
    st.divider()
    jakso = st.selectbox("Jakso", ["1", "2", "S", "K"])
    vuoro = st.text_input("Vuoropari", "1L")

# --- 2. PELAALISTAT (12 painonappia per joukkue) ---
st.subheader("Valitse Lyöjä")
col_koti, col_vieras, col_pelitilanne = st.columns([1, 1, 2])

with col_koti:
    st.write(f"**{koti_n}**")
    for i in range(1, 13):
        if st.button(f"{i}. Pelaaja K", key=f"k{i}", use_container_width=True):
            st.session_state.valittu_lyoja = f"{koti_n}: P{i}"

with col_vieras:
    st.write(f"**{vieras_n}**")
    for i in range(1, 13):
        if st.button(f"{i}. Pelaaja V", key=f"v{i}", use_container_width=True):
            st.session_state.valittu_lyoja = f"{vieras_n}: P{i}"

# --- 3. PELITILANNE JA LYÖNTI (Keskisarake) ---
with col_pelitilanne:
    st.info(f"Valittu lyöjä: **{st.session_state.valittu_lyoja}**")
    
    # Palot painonappeina
    palot = st.radio("Palot", ["0", "1", "2"], horizontal=True)
    
    # Tilanne (Excelin mukainen lista)
    tilanne = st.radio("Tilanne", ["0 tilanne", "1 tilanne", "1-2 tilanne", "Ajolähtö"], horizontal=True)

    st.divider()
    
    # Lyönnin tyyppi ja suunta
    c_tyyppi, c_suunta = st.columns(2)
    with c_tyyppi:
        l_tyyppi = st.selectbox("Lyönnin tyyppi", lyonnit)
        merkattu = st.checkbox("MERKKI PÄÄLLÄ")
    with c_suunta:
        # Suunnat napitettuina
        s1, s2, s3 = st.columns(3)
        if s1.button("3J"): st.session_state.valittu_suunta = "3 jatke"
        if s2.button("KS"): st.session_state.valittu_suunta = "keskisauma"
        if s3.button("2J"): st.session_state.valittu_suunta = "2 jatke"
        st.write(f"Suunta: **{st.session_state.valittu_suunta}**")

    st.divider()
    
    # Tulos (Nappeina nopeuden takia)
    st.subheader("Tulos")
    l_tulos = st.select_slider("Valitse tulos", options=tulokset)
    
    if st.button("💾 TALLENNA TAPAHTUMA", type="primary", use_container_width=True):
        onnistuminen = "Onnistunut" if l_tulos in ["juoksu", "vaihto", "eteni", "onnistunut kentällemeno"] else "Epäonnistunut"
        uusi = {
            "Päivämäärä": pvm, "Jakso": jakso, "Vuoropari": vuoro, "Tilanne": tilanne,
            "Lyöjä": st.session_state.valittu_lyoja, "Palot ennen lyöntiä": palot,
            "Lyönnin tyyppi": l_tyyppi, "Merkattu": "Merkattu" if merkattu else "",
            "Lyönnin sijainti": st.session_state.valittu_suunta, "Lyönnin tulos": l_tulos,
            "Onnistuminen": onnistuminen, "Sarja": sarja, "UP-KUVIO": up_kuvio
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        st.success("Tallennettu!")

# --- LOKI ---
st.dataframe(st.session_state.data.head(5), use_container_width=True)
