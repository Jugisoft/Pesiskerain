import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis Live Syöttö", layout="wide")

st.markdown("""
    <style>
    .main .block-container { padding: 0.5rem 1rem !important; }
    .stButton > button { padding: 0px 2px !important; font-size: 11px !important; height: 24px !important; border-radius: 2px !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    div.stRadio > div { gap: 2px !important; padding: 0px !important; }
    div.stRadio label { font-size: 10px !important; }
    hr { margin: 0.3rem 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu', 'v_lyonti_nro']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. NIMIEN SYÖTTÖ (Käsin) ---
with st.expander("📝 ASETA JOUKKUEET JA PELAAJAT", expanded=False):
    c_k, c_v = st.columns(2)
    koti_nimi = c_k.text_input("Kotijoukkue", "KPL")
    vieras_nimi = c_v.text_input("Vierasjoukkue", "Tahko")
    
    koti_nimet_raw = c_k.text_area(f"{koti_nimi}: Pelaajat (1 per rivi)", "1. Saukko\n2. Vartama\n3. Pitkänen\n4. Ruuska\n5. J. Luoma\n6. V. Luoma\n7. Latvala\n8. Laine\n9. Pesonen\n10. Nikkanen\n11. Toivola\n12. Alanen", height=150)
    vieras_nimet_raw = c_v.text_area(f"{vieras_nimi}: Pelaajat (1 per rivi)", "1. Nurmio\n2. Kauppinen\n3. Kettunen\n4. Kortehisto\n5. Kyhyräinen\n6. Raesmaa\n7. Kuosmanen\n8. Heikkala\n9. Tuomi\n10. Niemi\n11. Patova\n12. Matikka", height=150)

    k_lista = [n.strip() for n in koti_nimet_raw.split('\n') if n.strip()]
    v_lista = [n.strip() for n in vieras_nimet_raw.split('\n') if n.strip()]

# --- 2. PELIN HALLINTA ---
st.divider()
c1, c2, c3 = st.columns([1.5, 1, 1])

sisalla = c1.selectbox("SISÄLLÄ NYT:", [koti_nimi, vieras_nimi])
jakso = c2.selectbox("JAKSO", ["1", "2", "S", "K"])
vuoro = c3.selectbox("VUORO", [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]])

ulkona = vieras_nimi if sisalla == koti_nimi else koti_nimi
lyoja_lista = k_lista if sisalla == koti_nimi else v_lista
up_lista = v_lista if sisalla == koti_nimi else k_lista

st.info(f"⚾ **{sisalla}** lyö | **{ulkona}** ulkona")

# --- 3. SYÖTTÖNÄKYMÄ ---
col_l, col_m, col_r = st.columns([1.8, 3.2, 2.5])

# SARAKE 1: LYÖJÄT
with col_l:
    st.caption("LYÖJÄ")
    for i, nimi in enumerate(lyoja_lista):
        if st.button(nimi, key=f"l_{i}", use_container_width=True):
            st.session_state.v_lyoja = nimi

# SARAKE 2: TILANNE, MERKKI JA LYÖNTI
with col_m:
    tc1, tc2, tc3 = st.columns([2, 1, 1])
    t_map = {"0": "0 til", "1": "1 til", "0-2": "0-2", "0-3": "0-3", "1-2": "1-2", "1-3": "1-3", "2-3": "2-3", "Ajo": "Ajo"}
    til_val = tc1.radio("Tilanne", list(t_map.keys()), horizontal=True)
    palot = tc2.radio("Palot", ["0", "1", "2"], horizontal=True)
    st.session_state.v_lyonti_nro = tc3.radio("Lyönti", ["1", "2", "3"], horizontal=True)

    # SIIRRETTY: Merkattu tähän väliin
    st.write("")
    merkattu = st.checkbox("Merkattu", key="merk_val")
    st.write("---")

    st.caption("LYÖNTITYYPPI")
    ly_cols = st.columns(3)
    tyypit = ["Pieni", "Pomppu", "Pussari", "Varsi", "Kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(tyypit):
        if ly_cols[i % 3].button(t, key=f"lt_{t}", use_container_width=True): st.session_state.v_tyyppi = t

    st.write("---")
    st.caption("SUUNTA")
    s_cols = st.columns(3)
    suunnat = ["3 jatke", "3 taakse", "3 luukku", "3 sauma", "keskitakanen", "keskisauma", "keskipieni", "2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]
    for i, s in enumerate(suunnat):
        if s_cols[i % 3].button(s, key=f"s_{s}", use_container_width=True): st.session_state.v_suunta = s

# SARAKE 3: TULOS JA ULKOPELI
with col_r:
    st.caption("TULOS")
    tr_cols = st.columns(2)
    tulokset = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    for i, t in enumerate(tulokset):
        if tr_cols[i % 2].button(t, key=f"tr_{t}", use_container_width=True): st.session_state.v_tulos = t

    st.write("---")
    st.caption(f"UP ({ulkona})")
    up_cols = st.columns(3)
    for i, nimi in enumerate(up_lista):
        if up_cols[i % 3].button(nimi, key=f"u_{i}", use_container_width=True):
            st.session_state.v_up = nimi
    if st.button("OTTAMATON", use_container_width=True):
        st.session_state.v_up = "Ottamaton"

    st.caption("LAATU")
    la1, la2 = st.columns(2)
    if la1.button("PUHDAS", use_container_width=True): st.session_state.v_up_laatu = "Puhdas"
    if la2.button("NAKITUS", use_container_width=True): st.session_state.v_up_laatu = "Nakitus"

    st.write("---")
    cx1, cx2 = st.columns(2)
    takapalo = cx1.checkbox("TAKAPALO")
    up_kuvio = cx2.selectbox("Kuvio", ["", "MIKE", "PERTSA", "PYP"])

    if st.button("💾 TALLENNA", type="primary", use_container_width=True):
        uusi = {
            "Jakso": jakso, "Vuoro": vuoro, "Tilanne": t_map[til_val], "Sisällä": sisalla,
            "Lyöjä": st.session_state.v_lyoja, "Lyönti nro": st.session_state.v_lyonti_nro,
            "Palot": palot, "Merkattu": "Kyllä" if merkattu else "Ei",
            "Lyönti": st.session_state.v_tyyppi, "Suunta": st.session_state.v_suunta, 
            "Tulos": st.session_state.v_tulos, "UP": st.session_state.v_up, 
            "UP-Laatu": st.session_state.v_up_laatu, "Kuvio": up_kuvio, "Takapalo": "K" if takapalo else ""
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([uusi])], ignore_index=True)
        # Nollataan valinnat
        for k in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu']: st.session_state[k] = "-"
        st.rerun()

    if st.button("❌ POISTA VIIMEISIN", use_container_width=True):
        if not st.session_state.data.empty:
            st.session_state.data = st.session_state.data.iloc[:-1]
            st.rerun()

# --- 4. DATA ---
st.write("---")
st.dataframe(st.session_state.data, use_container_width=True)
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Lataa CSV", csv, "peli_data.csv", "text/csv")
