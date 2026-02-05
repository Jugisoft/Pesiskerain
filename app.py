import streamlit as st
import pandas as pd
from datetime import datetime

# --- ÄÄRIMMÄINEN TIIVISTYS (CSS) ---
st.set_page_config(page_title="Pesis Live v3.1", layout="wide")

st.markdown("""
    <style>
    /* Pakotetaan elementit lähekkäin */
    .block-container { padding: 0.5rem !important; }
    .stButton > button { 
        padding: 0px 2px !important; 
        font-size: 11px !important; 
        height: 24px !important; 
        border-radius: 2px !important;
    }
    /* Pienennetään otsikoiden ja valintojen välejä */
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    div.stRadio > div { gap: 2px !important; padding: 0px !important; }
    div.stRadio label { font-size: 10px !important; }
    hr { margin: 0.2rem 0 !important; }
    .stCaption { font-size: 10px !important; margin-bottom: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. YLÄRIVI ---
c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1.5, 0.6, 0.7])
pvm = c1.date_input("Pvm", datetime.now(), label_visibility="collapsed")
koti_n = c2.text_input("Koti", "Kouvola", label_visibility="collapsed")
vieras_n = c3.text_input("Vieras", "Hyvinkää", label_visibility="collapsed")
jakso = c4.selectbox("J", ["1", "2", "S", "K"], label_visibility="collapsed")
vuoro = c5.selectbox("V", [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]], label_visibility="collapsed")

# --- STATUSrivi (Kertoo mitä on valittu nyt) ---
st.markdown(f"**L:** {st.session_state.v_lyoja} | **T:** {st.session_state.v_tyyppi} | **S:** {st.session_state.v_suunta} | **R:** {st.session_state.v_tulos} | **UP:** {st.session_state.v_up} ({st.session_state.v_up_laatu})")

# --- 2. PÄÄNÄKYMÄ (3 Saraketta: Lyöjät, Peli, UP/Tulos) ---
col_l, col_m, col_r = st.columns([1.5, 3.5, 2.5])

# SARAKE 1: LYÖJÄT (Leveämmät napit nimille)
with col_l:
    st.caption("LYÖJÄ")
    # Tähän voisi ladata nimet Excelistä, nyt placeholderit
    for i in range(1, 13):
        nappi_teksti = f"{i}. Pelaaja" # Tähän tilalle nimet listasta
        if st.button(nappi_teksti, key=f"lk{i}", use_container_width=True):
            st.session_state.v_lyoja = nappi_teksti

# SARAKE 2: PELITAPAHTUMAT (Kaikki kasaan)
with col_m:
    # Tilanteet pienenä gridinä
    st.caption("TILANNE & PALOT")
    t_map = {"0": "0 til", "1": "1 til", "0-2": "0-2", "0-3": "0-3", "1-2": "1-2", "1-3": "1-3", "2-3": "2-3", "Ajo": "Ajo"}
    tc1, tc2 = st.columns([3, 1])
    til_val = tc1.radio("T", list(t_map.keys()), horizontal=True, label_visibility="collapsed")
    palot = tc2.radio("P", ["0", "1", "2"], horizontal=True, label_visibility="collapsed")

    st.divider()
    
    # Lyöntityypit (3x3 grid)
    st.caption("LYÖNTITYYPPI")
    ly_cols = st.columns(3)
    ly_lista = ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(ly_lista):
        if ly_cols[i % 3].button(t, key=f"lt_{t}", use_container_width=True):
            st.session_state.v_tyyppi = t

    st.divider()

    # Suunnat (4x3 grid)
    st.caption("SUUNTA")
    s_cols = st.columns(3)
    suunnat = ["3 jatke", "3 taakse", "3 luukku", "3 sauma", "keskitakanen", "keskisauma", "keskipieni", "2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]
    for i, s in enumerate(suunnat):
        if s_cols[i % 3].button(s, key=f"s_{s}", use_container_width=True):
            st.session_state.v_suunta = s

# SARAKE 3: TULOS JA ULKOPELI
with col_r:
    st.caption("TULOS")
    tr_cols = st.columns(2)
    t_lista = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    for i, t in enumerate(t_lista):
        if tr_cols[i % 2].button(t, key=f"tr_{t}", use_container_width=True):
            st.session_state.v_tulos = t

    st.divider()

    st.caption("SUORITTAVA ULKOPELAAJA")
    up_cols = st.columns(4)
    for i in range(1, 13):
        if up_cols[(i-1) % 4].button(f"#{i}", key=f"up{i}", use_container_width=True):
            st.session_state.v_up = str(i)
    if st.button("OTTAMATON", use_container_width=True):
        st.session_state.v_up = "Ottamaton"

    st.caption("LAATU")
    la1, la2 = st.columns(2)
    if la1.button("PUHDAS", use_container_width=True): st.session_state.v_up_laatu = "Puhdas"
    if la2.button("NAKITUS", use_container_width=True): st.session_state.v_up_laatu = "Nakitus"

    st.divider()
    c_x1, c_x2 = st.columns(2)
    merkattu = c_x1.checkbox("MERKKI")
    takapalo = c_x1.checkbox("TAKAPALO")
    up_kuvio = c_x2.selectbox("Kuvio", ["", "MIKE", "PERTSA", "PYP"], label_visibility="collapsed")

    if st.button("💾 TALLENNA", type="primary", use_container_width=True):
        uusi = {
            "Pvm": pvm, "Jakso": jakso, "Vuoro": vuoro, "Tilanne": t_map[til_val], 
            "Lyöjä": st.session_state.v_lyoja, "Palot": palot, "Lyönti": st.session_state.v_tyyppi, 
            "Merkattu": "M" if merkattu else "", "Suunta": st.session_state.v_suunta, 
            "Tulos": st.session_state.v_tulos, "UP": st.session_state.v_up, 
            "UP-Laatu": st.session_state.v_up_laatu, "Kuvio": up_kuvio, "Takapalo": "K" if takapalo else ""
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        # Nollaus (paitsi lyöjä ja tilanne usein pysyvät)
        for k in ['v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu']: st.session_state[k] = "-"
        st.rerun()

st.dataframe(st.session_state.data.head(1), use_container_width=True)
