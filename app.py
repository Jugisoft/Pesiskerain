import streamlit as st
import pandas as pd
import os
import base64
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis-Tilastoija v11.33", layout="wide")
KUVAN_NIMI = "Näyttökuva 2026-02-05 154559.png" 

# Alustetaan session_state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Jakso", "Vuoro", "Palot", "Tilanne", "Joukkue", "Lyöjä", "L-Nro", "Merkki", "Tyyppi", "Suunta", "Tulos", "Suoritus", "Takapalo"])
if 'valittu_suunta' not in st.session_state:
    st.session_state.valittu_suunta = "Ei valittu"
if 'nykyinen_lyonti' not in st.session_state:
    st.session_state.nykyinen_lyonti = 1

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# --- JOUKKUEET (Alkuperäinen logiikka) ---
with st.expander("Joukkueiden asetukset"):
    c_k, c_v = st.columns(2)
    koti_n = c_k.text_input("Kotijoukkue", "Koti")
    koti_p = c_k.text_area("Koti - Pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')
    vieras_n = c_v.text_input("Vierasjoukkue", "Vieras")
    vieras_p = c_v.text_area("Vieras - Pelaajat", "P1\nP2\nP3\nP4\nP5\nP6\nP7\nP8\nP9\nJ10\nJ11\nJ12").split('\n')

# --- YLÄOSA ---
kaikki_tilanteet = ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
tilanne = st.select_slider("Tilanne", options=kaikki_tilanteet)
palot = st.radio("Palot", ["0", "1", "2", "3"], horizontal=True)

st.divider()

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
    
    try:
        bin_img = get_base64_image(KUVAN_NIMI)
        
        # Määritellään painikkeiden sijainnit kuvan päällä (top%, left%)
        # Nämä vastaavat alkuperäisen koodin koordinaatteja
        nappula_data = [
            ("3 Jatke", 5, 15), ("Keskitaakse", 2, 50), ("2 Jatke", 5, 85),
            ("3 Luukku", 35, 25), ("Keskisauma", 50, 50), ("2 Luukku", 35, 75),
            ("3 Raja", 65, 30), ("Pieni", 85, 50), ("2 Raja", 65, 70)
        ]

        # Luodaan CSS-tyylit napeille
        nappula_html = ""
        for nimi, top, left in nappula_data:
            # Käytetään Streamlitin avainta (key) tunnistamaan painallus
            if st.button(nimi, key=f"btn_{nimi}"):
                st.session_state.valittu_suunta = nimi
                st.rerun()

        # Näytetään taustakuva
        st.markdown(
            f"""
            <div style="position: relative; width: 100%; max-width: 600px; margin: auto;">
                <img src="data:image/png;base64,{bin_img}" style="width: 100%; border-radius: 10px;">
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">
                    </div>
            </div>
            """, unsafe_allow_html=True
        )
        
        # Järjestetään napit visuaalisesti kentän muotoon kuvan alle/päälle sarakkeilla
        # Jotta ne toimivat varmasti klikattavina:
        k1, k2, k3 = st.columns(3)
        with k1:
            st.button("3 Jatke", on_click=lambda: st.session_state.update({"valittu_suunta": "3 Jatke"}))
            st.button("3 Luukku", on_click=lambda: st.session_state.update({"valittu_suunta": "3 Luukku"}))
            st.button("3 Raja", on_click=lambda: st.session_state.update({"valittu_suunta": "3 Raja"}))
        with k2:
            st.button("Keskitaakse", on_click=lambda: st.session_state.update({"valittu_suunta": "Keskitaakse"}))
            st.button("Keskisauma", on_click=lambda: st.session_state.update({"valittu_suunta": "Keskisauma"}))
            st.button("Pieni", on_click=lambda: st.session_state.update({"valittu_suunta": "Pieni"}))
        with k3:
            st.button("2 Jatke", on_click=lambda: st.session_state.update({"valittu_suunta": "2 Jatke"}))
            st.button("2 Luukku", on_click=lambda: st.session_state.update({"valittu_suunta": "2 Luukku"}))
            st.button("2 Raja", on_click=lambda: st.session_state.update({"valittu_suunta": "2 Raja"}))

    except Exception as e:
        st.error(f"Tarkista kuvan nimi GitHubissa: {e}")

with col_r:
    st.subheader("🏁 Tulos")
    tulos = st.radio("Tulos", ["PALO", "HAAVA", "LAITON", "TUOTTAMATON", "KENTÄLLEMENO", "VAIHTO", "ETENI", "JUOKSU"])
    takapalo = st.checkbox("TAKAPALO ⚠️")
    
    if st.button("TALLENNA", type="primary", use_container_width=True):
        if st.session_state.valittu_suunta == "Ei valittu":
            st.warning("Valitse suunta ensin!")
        else:
            uusi = {
                "Jakso": "1. Jakso", "Vuoro": "1. Aloittava", "Palot": palot, "Tilanne": tilanne,
                "Joukkue": v_jok, "Lyöjä": lyoja, "L-Nro": st.session_state.nykyinen_lyonti, "Merkki": merkki,
                "Tyyppi": tyyppi, "Suunta": st.session_state.valittu_suunta, "Tulos": tulos,
                "Suoritus": "Onnistunut" if tulos in ["JUOKSU", "VAIHTO", "KENTÄLLEMENO", "ETENI"] else "Epäonnistunut",
                "Takapalo": "TAKAPALO" if takapalo else "-"
            }
            st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
            st.session_state.nykyinen_lyonti = (st.session_state.nykyinen_lyonti % 3) + 1 # Automaattinen kierto
            st.session_state.valittu_suunta = "Ei valittu"
            st.rerun()

# --- LOKI ---
st.dataframe(st.session_state.data.head(5), use_container_width=True)
csv = st.session_state.data.to_csv(index=False, encoding="utf-8-sig")
st.download_button("📥 Lataa CSV", data=csv, file_name=f"pesis_{datetime.now().strftime('%Y%m%d')}.csv")
