import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Live v2.3", layout="wide")

# Erittäin tiukka CSS-tyyli, jotta kaikki mahtuu kerralla ruudulle
st.markdown("""
    <style>
    .stButton > button { padding: 1px 1px !important; font-size: 11px !important; height: 25px !important; }
    .stRadio > div { gap: 2px !important; }
    label { font-size: 12px !important; font-weight: bold; }
    .main .block-container { padding-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up_pelaaja', 'v_up_laatu']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. YLÄPALKKI (Tiivistetty) ---
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1.5, 0.8, 1])
    pvm = c1.date_input("Pvm", datetime.now(), label_visibility="collapsed")
    koti_n = c2.text_input("Koti", "Kotijoukkue", label_visibility="collapsed")
    vieras_n = c3.text_input("Vieras", "Vierailija", label_visibility="collapsed")
    jakso = c4.selectbox("Jakso", ["1", "2", "S", "K"])
    vuorot = [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]]
    vuoro = c5.selectbox("Vuoro", vuorot)

st.divider()

# --- 2. PÄÄNÄKYMÄ ---
col_lyojat, col_keski, col_tulos_up = st.columns([1, 3.5, 2.5])

# SARAKE 1: Lyöjät (Numeronapit)
with col_lyojat:
    st.write("🏃 **Lyöjä**")
    k_col, v_col = st.columns(2)
    with k_col:
        for i in range(1, 13):
            if st.button(f"K{i}", key=f"lk{i}", use_container_width=True): st.session_state.v_lyoja = f"K{i}"
    with v_col:
        for i in range(1, 13):
            if st.button(f"V{i}", key=f"lv{i}", use_container_width=True): st.session_state.v_lyoja = f"V{i}"

# SARAKE 2: Tilanne (tiivis), Suunnat ja Lyöntityyppi
with col_keski:
    # Tilanteet yhdellä rivillä (lyhenteet tilan säästämiseksi)
    t_map = {"0 til": "0 tilanne", "1 til": "1 tilanne", "0-2": "0-2 tilanne", "0-3": "0-3 tilanne", 
             "1-2": "1-2 tilanne", "1-3": "1-3 tilanne", "2-3": "2-3 tilanne", "Ajo": "Ajolähtö"}
    tilanne_lyhyt = st.radio("Tilanne", list(t_map.keys()), horizontal=True)
    tilanne = t_map[tilanne_lyhyt]
    palot = st.radio("Palot", ["0", "1", "2"], horizontal=True)

    st.divider()
    
    # Lyöntityypit painonappeina (3 saraketta)
    st.write(f"Lyöjä: **{st.session_state.v_lyoja}** | Tyyppi: **{st.session_state.v_tyyppi}**")
    lt1, lt2, lt3 = st.columns(3)
    l_tyypit = ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(l_tyypit):
        col = [lt1, lt2, lt3][i % 3]
        if col.button(t, key=f"lt_{t}", use_container_width=True): st.session_state.v_tyyppi = t

    st.divider()
    
    # Suunnat (Excelin mukaan)
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

# SARAKE 3: Tulos ja ULKOPELI
with col_tulos_up:
    # Tulos painonappeina
    st.write(f"Tulos: **{st.session_state.v_tulos}**")
    tr1, tr2 = st.columns(2)
    t_lista = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    for i, t in enumerate(t_lista):
        col = [tr1, tr2][i % 2]
        if col.button(t, key=f"tr_{t}", use_container_width=True): st.session_state.v_tulos = t

    st.divider()

    # Ulkopelaaja (Numerot + Ottamaton)
    st.write(f"UP: **{st.session_state.v_up_pelaaja}**")
    up1, up2, up3, up4 = st.columns(4)
    for i in range(1, 13):
        col = [up1, up2, up3, up4][(i-1) % 4]
        if col.button(f"#{i}", key=f"upn{i}", use_container_width=True): st.session_state.v_up_pelaaja = str(i)
    if st.button("OTTAMATON", type="secondary", use_container_width=True): st.session_state.v_up_pelaaja = "Ottamaton"

    st.session_state.v_up_laatu = st.radio("Laatu", ["Puhdas (Palo)", "Nakitus (Virhe)"], horizontal=True)

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
        # Nollaus seuraavaa lyöntiä varten
        for k in ['v_suunta', 'v_tyyppi', 'v_tulos', 'v_up_pelaaja']: st.session_state[k] = "-"
        st.rerun()

st.dataframe(st.session_state.data.head(2), use_container_width=True)
