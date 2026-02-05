import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Live v4.0", layout="wide")

st.markdown("""
    <style>
    .main .block-container { padding: 0.5rem 1rem !important; }
    .stButton > button { padding: 0px 2px !important; font-size: 11px !important; height: 24px !important; border-radius: 2px !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    div.stRadio > div { gap: 2px !important; padding: 0px !important; }
    div.stRadio label { font-size: 10px !important; }
    .stTextInput input, .stSelectbox div { height: 30px !important; font-size: 12px !important; }
    hr { margin: 0.3rem 0 !important; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu', 'v_lyonti_nro']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 2. YLÄPALKKI & KOKOONPANO ---
with st.container():
    c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1.5, 0.7, 0.8])
    pvm = c1.date_input("Pvm", datetime.now())
    koti_n = c2.text_input("Kotijoukkue", "Koti")
    vieras_n = c3.text_input("Vierailija", "Vieras")
    jakso = c4.selectbox("Jakso", ["1", "2", "S", "K"])
    vuoro = st.session_state.get('vuoro_val', '1A')
    vuoro = c5.selectbox("Vuoro", [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]], key='vuoro_val')

with st.expander("⚙️ Aseta pelaajien nimet (1 per rivi)"):
    ec1, ec2 = st.columns(2)
    koti_pelaajat_raw = ec1.text_area(f"{koti_n} pelaajat", "1.\n2.\n3.\n4.\n5.\n6.\n7.\n8.\n9.\n10.\n11.\n12.", height=200)
    vieras_pelaajat_raw = ec2.text_area(f"{vieras_n} pelaajat", "1.\n2.\n3.\n4.\n5.\n6.\n7.\n8.\n9.\n10.\n11.\n12.", height=200)
    
    k_list = [n.strip() for n in koti_pelaajat_raw.split('\n') if n.strip()][:12]
    v_list = [n.strip() for n in vieras_pelaajat_raw.split('\n') if n.strip()][:12]
    # Täytetään tyhjällä jos listat liian lyhyitä
    k_list += [f"K{i}" for i in range(len(k_list)+1, 13)]
    v_list += [f"V{i}" for i in range(len(v_list)+1, 13)]

# Statusrivi
st.warning(f"**VALITTU:** L: {st.session_state.v_lyoja} | Nro: {st.session_state.v_lyonti_nro} | S: {st.session_state.v_suunta} | T: {st.session_state.v_tyyppi} | R: {st.session_state.v_tulos} | UP: {st.session_state.v_up}")

# --- 3. PÄÄNÄKYMÄ ---
col_l, col_m, col_r = st.columns([1.5, 3.5, 2.5])

# SARAKE 1: LYÖJÄT (Nimet päivittyvät asetuksista)
with col_l:
    st.caption("LYÖJÄ")
    k_c, v_c = st.columns(2)
    for i in range(12):
        if k_c.button(k_list[i], key=f"lk{i}", use_container_width=True): st.session_state.v_lyoja = k_list[i]
        if v_c.button(v_list[i], key=f"lv{i}", use_container_width=True): st.session_state.v_lyoja = v_list[i]

# SARAKE 2: PELITAPAHTUMAT
with col_m:
    tc1, tc2, tc3 = st.columns([2, 1, 1])
    t_map = {"0": "0 til", "1": "1 til", "0-2": "0-2", "0-3": "0-3", "1-2": "1-2", "1-3": "1-3", "2-3": "2-3", "Ajo": "Ajo"}
    til_val = tc1.radio("Tilanne", list(t_map.keys()), horizontal=True)
    palot = tc2.radio("Palot", ["0", "1", "2"], horizontal=True)
    st.session_state.v_lyonti_nro = tc3.radio("Lyönti", ["1", "2", "3"], horizontal=True)

    st.write("---")
    st.caption("LYÖNTITYYPPI")
    ly_cols = st.columns(3)
    ly_lista = ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(ly_lista):
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
    t_lista = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    for i, t in enumerate(t_lista):
        if tr_cols[i % 2].button(t, key=f"tr_{t}", use_container_width=True): st.session_state.v_tulos = t

    st.write("---")
    st.caption("SUORITTAVA UP")
    # Ulkopelaajat määräytyvät lyöjän joukkueen mukaan
    up_nimet = v_list if (st.session_state.v_lyoja in k_list) else k_list
    up_cols = st.columns(3)
    for i in range(12):
        if up_cols[i % 3].button(up_nimet[i], key=f"up{i}", use_container_width=True): st.session_state.v_up = up_nimet[i]
    if st.button("OTTAMATON", use_container_width=True): st.session_state.v_up = "Ottamaton"

    st.caption("LAATU")
    la1, la2 = st.columns(2)
    if la1.button("PUHDAS", use_container_width=True): st.session_state.v_up_laatu = "Puhdas"
    if la2.button("NAKITUS", use_container_width=True): st.session_state.v_up_laatu = "Nakitus"

    st.write("---")
    cx1, cx2 = st.columns(2)
    merkattu = cx1.checkbox("MERKKI")
    takapalo = cx1.checkbox("TAKAPALO")
    up_kuvio = cx2.selectbox("Kuvio", ["", "MIKE", "PERTSA", "PYP"])

    save_col, undo_col = st.columns([2, 1])
    if save_col.button("💾 TALLENNA", type="primary", use_container_width=True):
        uusi = {
            "Pvm": pvm, "Jakso": jakso, "Vuoro": vuoro, "Tilanne": t_map[til_val], 
            "Lyöjä": st.session_state.v_lyoja, "Lyönti nro": st.session_state.v_lyonti_nro,
            "Palot": palot, "Lyönti": st.session_state.v_tyyppi, "Merkattu": "M" if merkattu else "", 
            "Suunta": st.session_state.v_suunta, "Tulos": st.session_state.v_tulos, "UP": st.session_state.v_up, 
            "UP-Laatu": st.session_state.v_up_laatu, "Kuvio": up_kuvio, "Takapalo": "K" if takapalo else ""
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([uusi])], ignore_index=True)
        for k in ['v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu']: st.session_state[k] = "-"
        st.rerun()
    
    if undo_col.button("❌ POISTA", use_container_width=True):
        if not st.session_state.data.empty:
            st.session_state.data = st.session_state.data.iloc[:-1]
            st.rerun()

# --- 4. LOKI ---
st.write("---")
st.write("### 📋 Tapahtumaloki")
st.dataframe(st.session_state.data, use_container_width=True)

# Export-nappi
if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Lataa ottelun data (CSV)", csv, f"ottelu_{pvm}.csv", "text/csv")
