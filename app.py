import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")

# Alustetaan session_state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = "Ei valittu"

# --- GRAAFINEN KENTTÄVALITSIN ---
def piirra_kentta_valitsin():
    # Kuvan URL (tämä on lähettämäsi kuva tai vastaava)
    kentta_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Pesapallokentta.svg/800px-Pesapallokentta.svg.png" 
    
    st.subheader("🏟️ Valitse lyönnin suunta")
    st.write(f"Nykyinen valinta: **{st.session_state.valittu_suunta}**")

    # CSS-tyylit napeille kentän päällä
    st.markdown(f"""
    <style>
        .kentta-container {{
            position: relative;
            width: 100%;
            max-width: 500px;
            margin: auto;
        }}
        .kentta-img {{
            width: 100%;
            display: block;
            border-radius: 10px;
            opacity: 0.6;
        }}
        .suunta-nappi {{
            position: absolute;
            transform: translate(-50%, -50%);
            background-color: #2c3e50;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 10px;
            cursor: pointer;
            border: 2px solid white;
        }}
        .suunta-nappi:hover {{ background-color: #f1c40f; color: black; }}
    </style>
    <div class="kentta-container">
        <img src="{kentta_url}" class="kentta-img">
    </div>
    """, unsafe_allow_index=True)

    # Koska Streamlitin omat napit eivät mene helposti HTML-kerroksen päälle "vapaasti",
    # käytämme tässä yksinkertaistettua kolmirivistä nappiasettelua, joka jäljittelee kuvaa:
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("3 Jatke"): st.session_state.valittu_suunta = "3 Jatke"
        if st.button("3 Luukku"): st.session_state.valittu_suunta = "3 Luukku"
        if st.button("3 Raja"): st.session_state.valittu_suunta = "3 Raja"
    with c2:
        if st.button("Keskitaakse"): st.session_state.valittu_suunta = "Keskitaakse"
        if st.button("Keskisauma"): st.session_state.valittu_suunta = "Keskisauma"
        if st.button("Pieni"): st.session_state.valittu_suunta = "Pieni"
    with c3:
        if st.button("2 Jatke"): st.session_state.valittu_suunta = "2 Jatke"
        if st.button("2 Luukku"): st.session_state.valittu_suunta = "2 Luukku"
        if st.button("2 Raja"): st.session_state.valittu_suunta = "2 Raja"

# --- PÄÄKÄYTTÖLIITTYMÄ ---
# (Käytetään aiemmin sovittua rakennetta pelaajalistojen ja muiden osalta)
with st.expander("Joukkueiden asetukset"):
    # ... (Pelaajien nimien syöttö kuten aiemmin)
    pass

# Jaetaan ruutu osiin
col_l, col_c, col_r = st.columns([1, 2, 1])

with col_l:
    st.subheader("🏃 Lyöjä")
    # Pelaajavalinnat
    pass

with col_c:
    piirra_kentta_valitsin()

with col_r:
    st.subheader("🏁 Tulos")
    # Tulosnapit väreineen
    if st.button("TALLENNA", type="primary", use_container_width=True):
        # Tallennuslogiikka
        st.rerun()
