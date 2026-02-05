import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis Live-Syöttö", layout="wide")

# Alustetaan session_state datalle ja valinnoille
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'temp_suunta' not in st.session_state:
    st.session_state.temp_suunta = ""

# Listat Excelistä (Syöttölomake & Listat)
jaksot = ["1", "2", "S", "K"]
tilanteet = ["0 tilanne", "1 tilanne", "0-2 tilanne", "0-3 tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
lyonnit = ["Pieni", "Pomppu", "Pussari", "Varsi", "Merkattu kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"]
suunnat = ["1 raja", "3 luukku", "3 sauma", "3 jatke", "3 taakse", "keskitakanen", "keskisauma", "keskipieni", "2 taakse", "2 sauma", "2 luukku", "2 raja"]
tulokset = ["palo", "haava", "eteni", "tuottamaton", "onnistunut kentällemeno", "laiton", "vaihto", "takapalo", "takaeteneminen", "juoksu"]

st.title("⚡ Pesis Live-Syöttö")

# --- RIVI 1: PELIN PERUSTIEDOT ---
with st.expander("Ottelun perustiedot (Aseta kerran)", expanded=False):
    c1, c2, c3, c4 = st.columns(4)
    vastustaja = c1.text_input("Vastustaja", "Hyvinkään Tahko")
    sarja = c2.text_input("Sarja", "MSU")
    up_kuvio = c3.selectbox("UP-KUVIO", ["MIKE", "PERTSA", "PYP"])
    pvm = c4.date_input("Päivämäärä", datetime.now())

# --- RIVI 2: TILANNE (NAPIT) ---
st.subheader("1. Tilanne")
c_j, c_v, c_t, c_p = st.columns([1, 1, 4, 2])
jakso = c_j.radio("Jakso", jaksot, horizontal=True)
vuoro = c_v.text_input("Vuoro", "1L")
tilanne = c_t.select_slider("Pelitilanne", options=tilanteet)
palot = c_p.radio("Palot ennen", ["0", "1", "2"], horizontal=True)

st.divider()

# --- RIVI 3: LYÖJÄ JA LYÖNNIN LAATU ---
col_lyoja, col_laatu = st.columns([1, 2])

with col_lyoja:
    st.subheader("2. Lyöjä")
    lyoja_nimi = st.text_input("Lyöjän nimi", "Patrik Wahlsten")
    lyonti_nro = st.radio("Lyönti nro", [1, 2, 3], horizontal=True)
    merkattu = st.toggle("MERKKI PÄÄLLÄ")
    
with col_laatu:
    st.subheader("3. Lyönnin tyyppi")
    # Tehdään tyypeistä isoja nappeja
    l_tyyppi = st.radio("Valitse tyyppi", lyonnit, horizontal=True)
    
    st.subheader("4. Suunta")
    # Suunnat sarakkeittain (3-puoli, Keskus, 2-puoli)
    s1, s2, s3 = st.columns(3)
    with s1:
        if st.button("3 Jatke", use_container_width=True): st.session_state.temp_suunta = "3 jatke"
        if st.button("3 Luukku", use_container_width=True): st.session_state.temp_suunta = "3 luukku"
        if st.button("3 Sauma", use_container_width=True): st.session_state.temp_suunta = "3 sauma"
        if st.button("3 Taakse", use_container_width=True): st.session_state.temp_suunta = "3 taakse"
    with s2:
        if st.button("Keskitaakse", use_container_width=True): st.session_state.temp_suunta = "keskitakanen"
        if st.button("Keskisauma", use_container_width=True): st.session_state.temp_suunta = "keskisauma"
        if st.button("Keskipieni", use_container_width=True): st.session_state.temp_suunta = "keskipieni"
    with s3:
        if st.button("2 Jatke", use_container_width=True): st.session_state.temp_suunta = "2 jatke"
        if st.button("2 Luukku", use_container_width=True): st.session_state.temp_suunta = "2 luukku"
        if st.button("2 Sauma", use_container_width=True): st.session_state.temp_suunta = "2 sauma"
        if st.button("1 Raja", use_container_width=True): st.session_state.temp_suunta = "1 raja"
    
    st.info(f"Valittu suunta: **{st.session_state.temp_suunta}**")

st.divider()

# --- RIVI 4: TULOS JA TALLENNUS ---
st.subheader("5. Tulos")
c_tulos, c_lisa = st.columns([2, 1])

with c_tulos:
    l_tulos = st.radio("Lyönnin tulos", tulokset, horizontal=True)
    onnistuminen = "Onnistunut" if l_tulos in ["juoksu", "vaihto", "eteni", "onnistunut kentällemeno"] else "Epäonnistunut"

with c_lisa:
    etenija = st.text_input("Etenijä", "")
    up_suorittaja = st.text_input("UP-suorittaja", "")

if st.button("💾 TALLENNA TAPAHTUMA", type="primary", use_container_width=True):
    uusi_rivi = {
        "Päivämäärä": pvm, "Vastustaja": vastustaja, "Jakso": jakso, "Vuoropari": vuoro,
        "Tilanne": tilanne, "Lyöjä": lyoja_nimi, "Lyönti nro": lyonti_nro, "Etenijä": etenija,
        "Palot ennen lyöntiä": palot, "Lyönnin tyyppi": l_tyyppi, "Merkattu": "Merkattu" if merkattu else "",
        "Lyönnin sijainti": st.session_state.temp_suunta, "Lyönnin tulos": l_tulos, "Onnistuminen": onnistuminen,
        "Suorittava ulkopelaaja": up_suorittaja, "Sarja": sarja, "UP-KUVIO": up_kuvio
    }
    st.session_state.data = pd.concat([pd.DataFrame([uusi_rivi]), st.session_state.data], ignore_index=True)
    st.session_state.temp_suunta = "" # Nollaus
    st.success("Tallennettu!")

# --- DATAN TARKASTELU ---
st.dataframe(st.session_state.data.head(5), use_container_width=True)
