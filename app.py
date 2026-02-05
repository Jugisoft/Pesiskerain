import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Live v2.2", layout="wide")

st.markdown("""
    <style>
    .stButton > button { padding: 2px 2px !important; font-size: 11px !important; }
    .stRadio > div { gap: 5px !important; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up_pelaaja', 'v_up_laatu']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. YLÄPALKKI ---
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1.2, 2, 2, 1, 1.2])
    pvm = c1.date_input("Pvm", datetime.now())
    koti_n = c2.text_input("Koti", "Kouvola")
    vieras_n = c3.text_input("Vieras", "Hyvinkää")
    jakso = c4.selectbox("Jakso", ["1", "2", "S", "K"])
    vuorot = [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]]
    vuoro = c5.selectbox("Vuoro", vuorot)

st.divider()

# --- 2. PÄÄNÄKYMÄ ---
col_lyojat, col_toiminta, col_up = st.columns([1.2, 3, 2.5])

# SARAKE 1: Lyöjät
with col_lyojat:
    st.caption("Lyöjä")
    k_col, v_col = st.columns(2)
    with k_col:
        for i in range(1, 13):
            if st.button(f"K{i}", key=f"lk{i}", use_container_width=True):
                st.session_state.v_lyoja = f"K{i}"
    with v_col:
        for i in range(1, 13):
            if st.button(f"V{i}", key=f"lv{i}", use_container_width=True):
                st.session_state.v_lyoja = f"V{i}"

# SARAKE 2: Tilanne ja Suunnat
with col_toiminta:
    t_lista = ["0 til", "1 til", "0-2 til", "0-3 til", "1-2 til", "1-3 til", "2-3 til", "Ajo"]
    tilanne = st.radio("Tilanne", t_lista, horizontal=True)
    palot = st.radio("Palot", ["0", "1", "2"], horizontal=True)

    st.divider()
    
    st.write(f"Suunta: **{st.session_state.v_suunta}**")
    s_c1, s_c2, s_c3 = st.columns(3)
    with s_c1:
        for s in ["3 jatke", "3 taakse", "3 luukku", "3 sauma"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c2:
        for s in ["keskitakanen", "keskisauma", "keskipieni"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c3:
        for s in ["2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s

# SARAKE 3: Tulos ja ULKOPELI (UP)
with col_up:
    st.write(f"L: **{st.session_state.v_lyoja}** | S: **{st.session_state.v_suunta}**")
    
    # Lyöntityyppi & Tulos
    c_t1, c_t2 = st.columns(2)
    with c_t1:
        st.caption("Lyönti")
        st.session_state.v_tyyppi = st.selectbox("Tyyppi", ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"], label_visibility="collapsed")
    with c_t2:
        st.caption("Tulos")
        st.session_state.v_tulos = st.selectbox("Tulos", ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"], label_visibility="collapsed")

    st.divider()

    # --- ULKOPELAAJAN SUORITUS ---
    st.caption("Suorittava ulkopelaaja")
    # Selvitetään kumpi joukkue on ulkona (vastakkainen kuin lyöjä)
    up_label = "Vieras UP" if "K" in st.session_state.v_lyoja else "Koti UP"
    st.write(f"**{up_label}** (valittu: {st.session_state.v_up_pelaaja})")
    
    up_n1, up_n2, up_n3, up_n4 = st.columns(4)
    for i in range(1, 13):
        col = [up_n1, up_n2, up_n3, up_n4][(i-1) % 4]
        if col.button(f"#{i}", key=f"up{i}", use_container_width=True):
            st.session_state.v_up_pelaaja = str(i)

    # Suorituksen laatu: Palo vai Nakitus
    st.session_state.v_up_laatu = st.radio("Suorituksen laatu", ["Puhdas suoritus (Palo)", "Nakitus (Räpylästä/Virhe)"], horizontal=True)

    c_ex1, c_ex2 = st.columns(2)
    merkattu = c_ex1.checkbox("MERKKI")
    takapalo = c_ex1.checkbox("TAKAPALO")
    up_kuvio = c_ex2.selectbox("UP-Kuvio", ["", "MIKE", "PERTSA", "PYP"], index=0)

    if st.button("💾 TALLENNA", type="primary", use_container_width=True):
        onnistuminen = "Onnistunut" if st.session_state.v_tulos in ["juoksu", "vaihto", "eteni", "kentällemeno"] else "Epäonnistunut"
        uusi = {
            "Pvm": pvm, "Jakso": jakso, "Vuoro": vuoro, "Tilanne": tilanne, "Lyöjä": st.session_state.v_lyoja,
            "Palot ennen": palot, "Lyönti": st.session_state.v_tyyppi, "Merkattu": "M" if merkattu else "",
            "Suunta": st.session_state.v_suunta, "Tulos": st.session_state.v_tulos,
            "Onnistuminen": onnistuminen, "UP-Pelaaja": st.session_state.v_up_pelaaja, 
            "UP-Laatu": st.session_state.v_up_laatu, "UP-KUVIO": up_kuvio, "Takapalo": "K" if takapalo else ""
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        # Nollataan valinnat
        for k in ['v_suunta', 'v_up_pelaaja']: st.session_state[k] = "-"
        st.rerun()

st.dataframe(st.session_state.data.head(3), use_container_width=True)
