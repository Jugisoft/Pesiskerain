import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")
KUVAN_NIMI = "image_de6e7c.png" # Varmista että tämä on oikein

# Alustetaan muisti
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = "Ei valittu"
if 'nykyinen_lyonti' not in st.session_state:
    st.session_state.nykyinen_lyonti = 1

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- JOUKKUEIDEN ASETUKSET ---
with st.expander("Joukkueiden asetukset", expanded=False):
    c_k, c_v = st.columns(2)
    koti_n = c_k.text_input("Kotijoukkue", "Koti")
    koti_p = c_k.text_area("Koti - Pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')
    vieras_n = c_v.text_input("Vierasjoukkue", "Vieras")
    vieras_p = c_v.text_area("Vieras - Pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')

# --- YLÄOSA (Tilanteet) ---
tilanteet = ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
tilanne = st.select_slider("Pelitilanne", options=tilanteet)
palot = st.radio("Palot", ["0", "1", "2", "3"], horizontal=True)

st.divider()

# --- PÄÄNÄKYMÄ ---
col_l, col_c, col_r = st.columns([1, 2, 1])

with col_l:
    st.subheader("🏃 Lyöjä")
    v_jok = st.radio("Joukkue", [koti_n, vieras_n], horizontal=True)
    nimet = koti_p if v_jok == koti_n else vieras_p
    lyoja = st.selectbox("Pelaaja", nimet)
    st.session_state.nykyinen_lyonti = st.radio("Lyönti", [1, 2, 3], index=st.session_state.nykyinen_lyonti-1, horizontal=True)
    merkki = st.radio("Merkki", ["Vapaa", "Merkattu"], horizontal=True)
    tyyppi = st.selectbox("Tyyppi", ["Kova", "Kumura", "Pomppu", "Pieni", "Pussari", "Varsi"])

with col_c:
    st.subheader(f"🏟️ Suunta: {st.session_state.valittu_suunta}")
    
    # Graafinen kenttä napeilla
    try:
        bin_img = get_base64_image(KUVAN_NIMI)
        
        # Määritellään suunnat ja niiden sijainnit (%) kuvan päällä
        # Nämä koordinaatit vastaavat pesis_kerain.py:n asettelua
        suunnat = [
            ("3 Jatke", 10, 20), ("Keskitaakse", 50, 10), ("2 Jatke", 90, 20),
            ("3 Luukku", 25, 35), ("Keskisauma", 50, 45), ("2 Luukku", 75, 35),
            ("3 Raja", 30, 70), ("Pieni", 50, 85), ("2 Raja", 70, 70)
        ]

        # Luodaan HTML-rakenne kuvalle
        html_code = f"""
        <div style="position: relative; width: 100%; max-width: 500px; margin: auto;">
            <img src="data:image/png;base64,{bin_img}" style="width: 100%; opacity: 0.9; border-radius: 15px;">
        """
        
        # Lisätään jokainen suunta näkymään (Streamlitin rajoitusten vuoksi käytetään tässä perusnappeja kuvan alla
        # TAI hienompaa ratkaisua jos haluat kokeilla myöhemmin. Tässä selkeä jako:)
        st.markdown(html_code + "</div>", unsafe_allow_html=True)
        
        # Luodaan napit kolmeen riviin jotka muistuttavat kenttää
        r1, r2, r3 = st.columns(3)
        with r1:
            if st.button("3 Jatke"): st.session_state.valittu_suunta = "3 Jatke"
            if st.button("3 Luukku"): st.session_state.valittu_suunta = "3 Luukku"
            if st.button("3 Raja"): st.session_state.valittu_suunta = "3 Raja"
        with r2:
            if st.button("Keskitaakse"): st.session_state.valittu_suunta = "Keskitaakse"
            if st.button("Keskisauma"): st.session_state.valittu_suunta = "Keskisauma"
            if st.button("Pieni"): st.session_state.valittu_suunta = "Pieni"
        with r3:
            if st.button("2 Jatke"): st.session_state.valittu_suunta = "2 Jatke"
            if st.button("2 Luukku"): st.session_state.valittu_suunta = "2 Luukku"
            if st.button("2 Raja"): st.session_state.valittu_suunta = "2 Raja"

    except Exception as e:
        st.error(f"Virhe kuvan latauksessa: {e}")

with col_r:
    st.subheader("🏁 Tulos")
    tulos_lista = ["PALO", "HAAVA", "LAITON", "TUOTTAMATON", "KENTÄLLEMENO", "VAIHTO", "ETENI", "JUOKSU"]
    tulos = st.radio("Lopputulos", tulos_lista)
    takapalo = st.checkbox("TAKAPALO ⚠️")
    
    if st.button("TALLENNA", type="primary", use_container_width=True):
        if st.session_state.valittu_suunta == "Ei valittu":
            st.error("Valitse suunta kentältä!")
        else:
            uusi = {
                "Jakso": "1. Jakso", "Vuoro": "1. Aloittava", "Palot": palot, "Tilanne": tilanne,
                "Joukkue": v_jok, "Lyöjä": lyoja, "L-Nro": st.session_state.nykyinen_lyonti, "Merkki": merkki,
                "Tyyppi": tyyppi, "Suunta": st.session_state.valittu_suunta, "Tulos": tulos,
                "Suoritus": "Onnistunut" if tulos in ["JUOKSU", "VAIHTO", "KENTÄLLEMENO", "ETENI"] else "Epäonnistunut",
                "Takapalo": "TAKAPALO" if takapalo else "-"
            }
            st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
            st.session_state.nykyinen_lyonti = (st.session_state.nykyinen_lyonti % 3) + 1
            st.session_state.valittu_suunta = "Ei valittu"
            st.rerun()

# --- LOKI ---
st.divider()
st.dataframe(st.session_state.data.head(10), use_container_width=True)
csv = st.session_state.data.to_csv(index=False, encoding="utf-8-sig")
st.download_button("📥 Lataa CSV", data=csv, file_name=f"pesis_{datetime.now().strftime('%Y%m%d')}.csv")
