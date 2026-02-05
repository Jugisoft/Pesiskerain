import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")

# VAIHDA TÄHÄN SE NIMI JOKA GITHUBISSA ON
KUVAN_NIMI = "Näyttökuva 2026-02-05 154559.png" 

# Funktio kuvan lukemiseksi (Streamlit tarvitsee tämän paikallisille kuville)
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Alustetaan muisti
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = "Ei valittu"
if 'nykyinen_lyonti' not in st.session_state:
    st.session_state.nykyinen_lyonti = 1

# --- JOUKKUEIDEN NIMET JA KOKOOPANOT ---
with st.expander("Aseta joukkueet ja pelaajat"):
    c_k, c_v = st.columns(2)
    koti_n = c_k.text_input("Kotijoukkue", "Koti")
    koti_p = c_k.text_area("Kotijoukkueen pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')
    vieras_n = c_v.text_input("Vierasjoukkue", "Vieras")
    vieras_p = c_v.text_area("Vierasjoukkueen pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')

# --- YLÄOSA ---
t_col1, t_col2 = st.columns([3, 1])
with t_col1:
    tilanteet = ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
    tilanne = st.radio("Tilanne", tilanteet, horizontal=True)
with t_col2:
    palot = st.radio("Palot", ["0", "1", "2", "3"], horizontal=True)

st.divider()

# --- SYÖTTÖALUE ---
c_lyoja, c_kentta, c_tulos = st.columns([1, 2, 1])

with c_lyoja:
    st.subheader("🏃 Lyöjä")
    v_jok = st.radio("Vuorossa", [koti_n, vieras_n], horizontal=True)
    nimet = koti_p if v_jok == koti_n else vieras_p
    lyoja = st.selectbox("Pelaaja", nimet)
    st.session_state.nykyinen_lyonti = st.radio("Lyönti", [1, 2, 3], index=st.session_state.nykyinen_lyonti-1, horizontal=True)
    merkki = st.radio("Merkki", ["Vapaa", "Merkattu"], horizontal=True)
    tyyppi = st.selectbox("Tyyppi", ["Kova", "Kumura", "Pomppu", "Pieni", "Pussari", "Varsi"])

with c_kentta:
    st.subheader("🏟️ Lyönnin suunta")
    st.write(f"Valittu: **{st.session_state.valittu_suunta}**")
    
    try:
        bin_img = get_base64_image(KUVAN_NIMI)
        st.markdown(f"""
            <div style="position: relative; width: 100%; max-width: 500px; margin: auto;">
                <img src="data:image/png;base64,{bin_img}" style="width: 100%; border-radius: 10px; opacity: 0.8;">
            </div>
        """, unsafe_allow_html=True)
    except:
        st.error(f"Kuvaa '{KUVAN_NIMI}' ei löytynyt reposta.")

    # Napit kentän muotoon
    s1, s2, s3 = st.columns(3)
    if s1.button("3 Jatke", use_container_width=True): st.session_state.valittu_suunta = "3 Jatke"
    if s2.button("Keskitaakse", use_container_width=True): st.session_state.valittu_suunta = "Keskitaakse"
    if s3.button("2 Jatke", use_container_width=True): st.session_state.valittu_suunta = "2 Jatke"
    
    s4, s5, s6 = st.columns(3)
    if s4.button("3 Luukku", use_container_width=True): st.session_state.valittu_suunta = "3 Luukku"
    if s5.button("Keskisauma", use_container_width=True): st.session_state.valittu_suunta = "Keskisauma"
    if s6.button("2 Luukku", use_container_width=True): st.session_state.valittu_suunta = "2 Luukku"
    
    s7, s8, s9 = st.columns(3)
    if s7.button("3 Raja", use_container_width=True): st.session_state.valittu_suunta = "3 Raja"
    if s8.button("Pieni", use_container_width=True): st.session_state.valittu_suunta = "Pieni"
    if s9.button("2 Raja", use_container_width=True): st.session_state.valittu_suunta = "2 Raja"

with c_tulos:
    st.subheader("🏁 Tulos")
    # Alkuperäiset värit ja lista
    tulos = st.radio("Tulos", ["PALO", "HAAVA", "LAITON", "TUOTTAMATON", "KENTÄLLEMENO", "VAIHTO", "ETENI", "JUOKSU"])
    takapalo = st.checkbox("TAKAPALO ⚠️")
    
    if st.button("TALLENNA", type="primary", use_container_width=True):
        uusi = {
            "Jakso": "1. Jakso", "Vuoro": "1. Aloittava", "Palot": palot, "Tilanne": tilanne,
            "Joukkue": v_jok, "Lyöjä": lyoja, "L-Nro": st.session_state.nykyinen_lyonti, "Merkki": merkki,
            "Tyyppi": tyyppi, "Suunta": st.session_state.valittu_suunta, "Tulos": tulos,
            "Suoritus": "Onnistunut" if tulos in ["JUOKSU", "VAIHTO", "KENTÄLLEMENO", "ETENI"] else "Epäonnistunut",
            "Takapalo": "TAKAPALO" if takapalo else "-"
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        # Automaattinen lyöntinumeron vaihto kuten alkuperäisessä
        st.session_state.nykyinen_lyonti = (st.session_state.nykyinen_lyonti % 3) + 1
        st.session_state.valittu_suunta = "Ei valittu"
        st.rerun()

# --- LOKI ---
st.divider()
st.dataframe(st.session_state.data.head(10), use_container_width=True)
csv = st.session_state.data.to_csv(index=False, encoding="utf-8-sig")
st.download_button("📥 Lataa CSV", data=csv, file_name=f"pesis_{datetime.now().strftime('%Y%m%d')}.csv")
