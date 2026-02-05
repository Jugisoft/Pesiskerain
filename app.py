import streamlit as st
import pandas as pd
import base64
from datetime import datetime

st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")
KUVAN_NIMI = "Näyttökuva 2026-02-05 154559.png" 

# Alustukset
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = "Ei valittu"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- CSS: NAPPIEN SIJOITTELU KUVAN PÄÄLLE ---
def piirra_graafinen_kentta():
    try:
        bin_img = get_base64_image(KUVAN_NIMI)
        
        # Määritellään suunnat ja niiden sijainti prosentteina (Y, X)
        # Säädä näitä lukuja, jos napit eivät osu kohdalleen
        nappulat = [
            ("3 Jatke", 15, 10), ("Keskitaakse", 5, 50), ("2 Jatke", 15, 90),
            ("3 Luukku", 40, 25), ("Keskisauma", 45, 50), ("2 Luukku", 40, 75),
            ("3 Raja", 65, 20), ("Pieni", 85, 50), ("2 Raja", 65, 80)
        ]

        # Luodaan HTML-rakenne
        html_sisalto = f"""
        <div style="position: relative; width: 100%; max-width: 500px; margin: auto;">
            <img src="data:image/png;base64,{bin_img}" style="width: 100%; border-radius: 10px;">
        """
        
        for nimi, top, left in nappulat:
            # Luodaan näkymätön klikattava alue tai tyylitelty nappi
            # Huom: Streamlitin st.buttonia ei voi suoraan laittaa HTML:n sisään, 
            # joten käytämme tässä Streamlitin query_params tai nappilistaa alla.
            pass
            
        st.markdown(html_sisalto + "</div>", unsafe_allow_html=True)
        
        # Koska HTML-napit eivät keskustele helposti Pythonin kanssa ilman lisäosia,
        # käytetään "Nappiryppäitä", jotka on aseteltu visuaalisesti kentän muotoon:
        
        st.write(f"### Valittu suunta: :red[{st.session_state.valittu_suunta}]")
        
        # Takakenttä
        c1, c2, c3 = st.columns([1,1,1])
        if c1.button("3 Jatke", use_container_width=True): st.session_state.valittu_suunta = "3 Jatke"
        if c2.button("Keskitaakse", use_container_width=True): st.session_state.valittu_suunta = "Keskitaakse"
        if c3.button("2 Jatke", use_container_width=True): st.session_state.valittu_suunta = "2 Jatke"
        
        # Välikenttä
        c4, c5, c6 = st.columns([1.5, 2, 1.5])
        if c4.button("3 Luukku", use_container_width=True): st.session_state.valittu_suunta = "3 Luukku"
        if c5.button("Keskisauma", use_container_width=True): st.session_state.valittu_suunta = "Keskisauma"
        if c6.button("2 Luukku", use_container_width=True): st.session_state.valittu_suunta = "2 Luukku"
        
        # Etukenttä
        c7, c8, c9 = st.columns([2, 1, 2])
        if c7.button("3 Raja", use_container_width=True): st.session_state.valittu_suunta = "3 Raja"
        if c8.button("Pieni", use_container_width=True): st.session_state.valittu_suunta = "Pieni"
        if c9.button("2 Raja", use_container_width=True): st.session_state.valittu_suunta = "2 Raja"

    except Exception as e:
        st.error(f"Kuvaa ei saatu ladattua: {e}")

# --- PÄÄNÄKYMÄ ---
col_stats, col_action = st.columns([1, 3])

with col_stats:
    st.subheader("Pelaaja & Tulos")
    # Tähän kaikki ne valinnat jotka hävisivät (lyöjä, tulos jne)
    lyoja = st.number_input("Lyöjä", 1, 12)
    tulos = st.selectbox("Tulos", ["PALO", "HAAVA", "VAIHTO", "JUOKSU", "KENTÄLLEMENO"])
    if st.button("TALLENNA", type="primary", use_container_width=True):
        # Tallennuslogiikka tähän
        st.success("Tallennettu!")

with col_action:
    piirra_graafinen_kentta()
