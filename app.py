import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija Pro", layout="wide")

# Alustetaan session_state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

# Ladataan listat Excelistä (tässä koodissa kiinteänä Excel-tiedoston pohjalta)
valinnat = {
    "Jakso": ["1", "2", "S", "K"],
    "Tilanne": ["0 tilanne", "1 tilanne", "0-2 tilanne", "0-3 tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"],
    "Lyönti_nro": [1, 2, 3],
    "Lyönnin_tyyppi": ["Pieni", "Pomppu", "Pussari", "Varsi", "Merkattu kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"],
    "Merkattu": ["", "Merkattu"],
    "Suunta": ["1 raja", "3 luukku", "3 sauma", "3 jatke", "3 taakse", "keskitakanen", "keskisauma", "keskipieni", "2 taakse", "2 sauma", "2 luukku", "2 raja", "keskisauma"],
    "Tulos": ["palo", "haava", "eteni", "tuottamaton", "onnistunut kentällemeno", "laiton", "vaihto", "takapalo", "takaeteneminen", "juoksu"],
    "Onnistuminen": ["Onnistunut", "Epäonnistunut"]
}

st.title("⚾ Pesäpallon Syöttölomake")

# --- 1. PERUSTIEDOT (Yläpalkki) ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    pvm = c1.date_input("Päivämäärä", datetime.now())
    vastustaja = c2.text_input("Vastustaja", "Hyvinkään Tahko")
    sarja = c3.text_input("Sarja", "MSU")
    up_kuvio = c4.text_input("UP-KUVIO", "MIKE")

st.divider()

# --- 2. TILANNE JA LYÖJÄ ---
col1, col2, col3 = st.columns([1, 1.5, 1.5])

with col1:
    st.subheader("Peli")
    jakso = st.radio("Jakso", valinnat["Jakso"], horizontal=True)
    vuoropari = st.text_input("Vuoropari (esim. 2L tai 4A)", "1L")
    tilanne = st.selectbox("Tilanne", valinnat["Tilanne"])
    palot = st.radio("Palot ennen", ["0", "1", "2"], horizontal=True)

with col2:
    st.subheader("Lyöjä & Etenijät")
    lyoja = st.text_input("Lyöjä", "Patrik Wahlsten")
    lyonti_nro = st.radio("Lyönti nro", valinnat["Lyönti_nro"], horizontal=True)
    etenija = st.text_input("Etenijä", "")
    t_etenija1 = st.text_input("Takaetenijä 1", "")
    t_etenija2 = st.text_input("Takaetenijä 2", "")

with col3:
    st.subheader("Lyönnin laatu")
    l_tyyppi = st.selectbox("Lyönnin tyyppi", valinnat["Lyönnin_tyyppi"])
    merkattu = st.radio("Merkattu", valinnat["Merkattu"], horizontal=True)
    sijainti = st.selectbox("Lyönnin sijainti (Suunta)", valinnat["Suunta"])
    lukkari_toiminto = st.text_input("Lukkarin toiminto", "")

st.divider()

# --- 3. TULOS ---
col_t1, col_t2 = st.columns(2)

with col_t1:
    st.subheader("Lopputulos")
    l_tulos = st.radio("Lyönnin tulos", valinnat["Tulos"], horizontal=True)
    onnistuminen = "Onnistunut" if l_tulos in ["juoksu", "vaihto", "eteni", "onnistunut kentällemeno"] else "Epäonnistunut"
    st.info(f"Päätelty onnistuminen: **{onnistuminen}**")

with col_t2:
    st.subheader("Lisätiedot")
    o_tarkenne = st.text_input("Onnistumisen tarkenne", "")
    toiminto_lyoja = st.text_input("Toiminto lyöjällä", "")
    suorittava_up = st.text_input("Suorittava ulkopelaaja", "")

# --- TALLENNUS ---
if st.button("TALLENNA RIVI EXCELIIN", type="primary", use_container_width=True):
    uusi_rivi = {
        "Päivämäärä": pvm, "Vastustaja": vastustaja, "Jakso": jakso, "Vuoropari": vuoropari,
        "Tilanne": tilanne, "Lyöjä": lyoja, "Lyönti nro": lyonti_nro, "Etenijä": etenija,
        "Palot ennen lyöntiä": palot, "Lyönnin tyyppi": l_tyyppi, "Merkattu": merkattu,
        "Lyönnin sijainti": sijainti, "Lyönnin tulos": l_tulos, "Onnistuminen": onnistuminen,
        "Onnistumisen tarkenne": o_tarkenne, "Toiminto lyöjällä": toiminto_lyoja,
        "Suorittava ulkopelaaja": suorittava_up, "Lukkarin toiminto": lukkari_toiminto,
        "Sarja": sarja, "Takaetenijä 1": t_etenija1, "Takaetenijä 2": t_etenija2, "UP-KUVIO": up_kuvio
    }
    
    st.session_state.data = pd.concat([pd.DataFrame([uusi_rivi]), st.session_state.data], ignore_index=True)
    st.success("Tapahtuma tallennettu listaan!")

# --- NÄKYMÄ ---
st.divider()
st.subheader("Tallennetut rivit")
st.dataframe(st.session_state.data, use_container_width=True)

# Lataus
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Lataa CSV (Excel-yhteensopiva)", data=csv, file_name="pesis_tilastot.csv", mime="text/csv")
