import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Pro Syöttö", layout="wide")

# Tiivistetään nappeja CSS:llä, jotta ne vievät vähemmän tilaa
st.markdown("""
    <style>
    div.stButton > button {
        padding: 2px 5px !important;
        font-size: 14px !important;
        height: auto !important;
    }
    [data-testid="column"] {
        padding: 0px 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'v_lyoja' not in st.session_state: st.session_state.v_lyoja = ""
if 'v_suunta' not in st.session_state: st.session_state.v_suunta = ""

# --- 1. YLÄPALKKI (Muuttumattomat tiedot) ---
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1.5, 1, 1])
    pvm = c1.date_input("Pvm", datetime.now())
    koti_n = c2.text_input("Koti", "Kouvola")
    vieras_n = c3.text_input("Vieras", "Hyvinkää")
    jakso = c4.selectbox("Jakso", ["1", "2", "S", "K"])
    vuoro = c5.text_input("Vuoro", "1L")

st.divider()

# --- 2. PÄÄNÄKYMÄ (Lyöjät ja toiminta) ---
# Jaetaan sivu: Lyöjät (vasen), Pelitapahtuma (keski), Tulos (oikea)
col_lyojat, col_peli, col_tulos = st.columns([1.5, 3, 1.5])

with col_lyojat:
    st.caption("Valitse lyöjä")
    k_col, v_col = st.columns(2)
    with k_col:
        st.write(f"**{koti_n[:4]}**")
        for i in range(1, 13):
            if st.button(f"{i}", key=f"k{i}", use_container_width=True):
                st.session_state.v_lyoja = f"{koti_n}: {i}"
    with v_col:
        st.write(f"**{vieras_n[:4]}**")
        for i in range(1, 13):
            if st.button(f"{i}", key=f"v{i}", use_container_width=True):
                st.session_state.v_lyoja = f"{vieras_n}: {i}"

with col_peli:
    # Tilanteet ja Palot
    st.write(f"Lyöjä: **{st.session_state.v_lyoja}**")
    
    t1, t2 = st.columns([2, 1])
    with t1:
        tilanne = st.radio("Tilanne", ["0 tilanne", "1 tilanne", "0-2 tilanne", "0-3 tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"], horizontal=True)
    with t2:
        palot = st.radio("Palot", ["0", "1", "2"], horizontal=True)

    st.divider()

    # Suunnat (Excelin mukaan)
    st.write("Valitse Suunta:")
    s_c1, s_c2, s_c3 = st.columns(3)
    suunnat_3 = ["3 jatke", "3 taakse", "3 luukku", "3 sauma"]
    suunnat_k = ["keskitakanen", "keskisauma", "keskipieni"]
    suunnat_2 = ["2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]

    with s_c1:
        for s in suunnat_3:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c2:
        for s in suunnat_k:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c3:
        for s in suunnat_2:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    
    st.info(f"Suunta: {st.session_state.v_suunta}")

with col_tulos:
    st.write("Tulos & Tyyppi")
    l_tyyppi = st.selectbox("Lyönti", ["Pieni", "Pomppu", "Pussari", "Varsi", "Merkattu kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"])
    merkattu = st.toggle("Merkattu")
    
    l_tulos = st.selectbox("Lopputulos", ["palo", "haava", "eteni", "tuottamaton", "onnistunut kentällemeno", "laiton", "vaihto", "takapalo", "takaeteneminen", "juoksu"])
    
    takapalo_btn = st.checkbox("⚠️ TAKAPALO", value=(l_tulos == "takapalo"))
    
    up_kuvio = st.selectbox("UP-Kuvio", ["MIKE", "PERTSA", "PYP"])
    
    if st.button("💾 TALLENNA", type="primary", use_container_width=True):
        onnistuminen = "Onnistunut" if l_tulos in ["juoksu", "vaihto", "eteni", "onnistunut kentällemeno"] else "Epäonnistunut"
        uusi = {
            "Päivämäärä": pvm, "Jakso": jakso, "Vuoropari": vuoro, "Tilanne": tilanne,
            "Lyöjä": st.session_state.v_lyoja, "Palot ennen": palot,
            "Lyönnin tyyppi": l_tyyppi, "Merkattu": "Merkattu" if merkattu else "",
            "Lyönnin sijainti": st.session_state.v_suunta, "Lyönnin tulos": l_tulos,
            "Onnistuminen": onnistuminen, "UP-KUVIO": up_kuvio, "Takapalo": "Kyllä" if takapalo_btn else "Ei"
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        st.session_state.v_suunta = "" # Nollaus
        st.rerun()

# Loki alhaalla
st.dataframe(st.session_state.data.head(5), use_container_width=True)
