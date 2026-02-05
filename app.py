import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Live v2.1", layout="wide")

# CSS: Tiivistetään painikkeita ja asettelua, jotta kaikki mahtuu kerralla ruudulle
st.markdown("""
    <style>
    .stButton > button {
        padding: 4px 2px !important;
        font-size: 12px !important;
        height: auto !important;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 14px;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()
if 'v_lyoja' not in st.session_state: st.session_state.v_lyoja = "-"
if 'v_suunta' not in st.session_state: st.session_state.v_suunta = "-"
if 'v_tyyppi' not in st.session_state: st.session_state.v_tyyppi = "-"
if 'v_tulos' not in st.session_state: st.session_state.v_tulos = "-"

# --- 1. YLÄPALKKI (Muuttumattomat & Alasvetovalikot) ---
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1.2, 2, 2, 1, 1.2])
    pvm = c1.date_input("Pvm", datetime.now())
    koti_n = c2.text_input("Koti", "Kotijoukkue")
    vieras_n = c3.text_input("Vieras", "Vierailija")
    jakso = c4.selectbox("Jakso", ["1", "2", "S", "K"])
    # Vuoroparit alasvetovalikkoon
    vuorot = [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]]
    vuoro = c5.selectbox("Vuoro", vuorot)

st.divider()

# --- 2. PÄÄNÄKYMÄ ---
col_lyojat, col_toiminta, col_valinnat = st.columns([1.2, 3, 2.5])

# SARAKE 1: Lyöjät (Pienet numeronapit)
with col_lyojat:
    st.caption("Valitse Lyöjä")
    k_col, v_col = st.columns(2)
    with k_col:
        st.write(f"**{koti_n[:3]}**")
        for i in range(1, 13):
            if st.button(f"K{i}", key=f"k{i}", use_container_width=True):
                st.session_state.v_lyoja = f"{koti_n} #{i}"
    with v_col:
        st.write(f"**{vieras_n[:3]}**")
        for i in range(1, 13):
            if st.button(f"V{i}", key=f"v{i}", use_container_width=True):
                st.session_state.v_lyoja = f"{vieras_n} #{i}"

# SARAKE 2: Tilanteet ja Suunnat
with col_toiminta:
    # Tilanteet painonappeina
    st.caption("Tilanne ja Palot")
    t_lista = ["0 tilanne", "1 tilanne", "0-2 tilanne", "0-3 tilanne", "1-2 tilanne", "1-3 tilanne", "2-3 tilanne", "Ajolähtö"]
    tilanne = st.radio("Pelitilanne", t_lista, horizontal=True, label_visibility="collapsed")
    palot = st.radio("Palot", ["0", "1", "2"], horizontal=True)

    st.divider()
    
    # Suuntapainikkeet (Excel-lista)
    st.write(f"Suunta: **{st.session_state.v_suunta}**")
    s_c1, s_c2, s_c3 = st.columns(3)
    with s_c1: # 3-puoli
        for s in ["3 jatke", "3 taakse", "3 luukku", "3 sauma"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c2: # Keskus
        for s in ["keskitakanen", "keskisauma", "keskipieni"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s
    with s_c3: # 2-puoli
        for s in ["2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]:
            if st.button(s, use_container_width=True): st.session_state.v_suunta = s

# SARAKE 3: Tyyppi, Tulos ja Takapalo (Kaikki painonappeina)
with col_valinnat:
    st.write(f"Lyöjä: **{st.session_state.v_lyoja}**")
    
    # Lyöntityyppi painonappeina
    st.caption("Lyöntityyppi")
    ly_tyypit = ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]
    c_tyyppi1, c_tyyppi2, c_tyyppi3 = st.columns(3)
    for idx, t in enumerate(ly_tyypit):
        col = [c_tyyppi1, c_tyyppi2, c_tyyppi3][idx % 3]
        if col.button(t, use_container_width=True): st.session_state.v_tyyppi = t
    st.write(f"Tyyppi: **{st.session_state.v_tyyppi}**")

    st.divider()

    # Tulos painonappeina
    st.caption("Tulos")
    t_tulokset = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    c_tulos1, c_tulos2 = st.columns(2)
    for idx, t in enumerate(t_tulokset):
        col = [c_tulos1, c_tulos2][idx % 2]
        if col.button(t, use_container_width=True): st.session_state.v_tulos = t
    
    st.write(f"Tulos: **{st.session_state.v_tulos}**")
    
    # Takapalo ja muut extrat
    c_extra1, c_extra2 = st.columns(2)
    with c_extra1:
        merkattu = st.checkbox("MERKKI")
        takapalo = st.checkbox("TAKAPALO ⚠️")
    with c_extra2:
        up_kuvio = st.selectbox("UP-Kuvio", ["MIKE", "PERTSA", "PYP"])

    if st.button("💾 TALLENNA TAPAHTUMA", type="primary", use_container_width=True):
        onnistuminen = "Onnistunut" if st.session_state.v_tulos in ["juoksu", "vaihto", "eteni", "kentällemeno"] else "Epäonnistunut"
        uusi = {
            "Päivämäärä": pvm, "Jakso": jakso, "Vuoropari": vuoro, "Tilanne": tilanne,
            "Lyöjä": st.session_state.v_lyoja, "Palot ennen": palot,
            "Lyönnin tyyppi": st.session_state.v_tyyppi, "Merkattu": "Merkattu" if merkattu else "",
            "Lyönnin sijainti": st.session_state.v_suunta, "Lyönnin tulos": st.session_state.v_tulos,
            "Onnistuminen": onnistuminen, "UP-KUVIO": up_kuvio, "Takapalo": "Kyllä" if takapalo else "Ei"
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        # Nollataan valinnat seuraavaa varten
        st.session_state.v_suunta = "-"
        st.session_state.v_tyyppi = "-"
        st.session_state.v_tulos = "-"
        st.rerun()

# --- LOKI ---
st.dataframe(st.session_state.data.head(5), use_container_width=True)
