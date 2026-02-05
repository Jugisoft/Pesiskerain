import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. ASETUKSET JA TYYLIT ---
st.set_page_config(page_title="Pesis Live v4.2 - KPL vs Tahko", layout="wide")

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

# --- 2. JOUKKUEDATA (KPL vs Tahko) ---
koti_n = "Kouvolan Pallonlyöjät"
vieras_n = "Hyvinkään Tahko"

# Pelaajat linkin mukaisessa järjestyksessä
k_nimet = ["1. T. Saukko", "2. P. Vartama", "3. E. Pitkänen", "4. A. Ruuska", "5. J. Luoma", 
           "6. V. Luoma", "7. M. Latvala", "8. E. Laine", "9. I. Pesonen", "10. T. Nikkanen", "11. J. Toivola", "12. P. Alanen"]

v_nimet = ["1. T. Nurmio", "2. J. Kauppinen", "3. V. Kettunen", "4. V. Kortehisto", "5. S. Kyhyräinen", 
           "6. L. Raesmaa", "7. K. Kuosmanen", "8. J. Heikkala", "9. E. Tuomi", "10. J. Niemi", "11. S. Patova", "12. J. Matikka"]

# --- 3. YLÄPALKKI ---
with st.container():
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    sisalla = c1.selectbox("Sisävuoro", [koti_n, vieras_n])
    jakso = c2.selectbox("Jakso", ["1", "2", "S", "K"])
    vuoro = c3.selectbox("Vuoro", [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]])
    
    ulkona = vieras_n if sisalla == koti_n else koti_n
    lyoja_lista = k_nimet if sisalla == koti_n else v_nimet
    up_lista = v_nimet if sisalla == koti_n else k_nimet

st.warning(f"**TILANNE:** {sisalla} lyö | {ulkona} ulkona")

# --- 4. PÄÄNÄKYMÄ ---
col_l, col_m, col_r = st.columns([1.8, 3.2, 2.5])

# SARAKE 1: LYÖJÄT
with col_l:
    st.caption(f"LYÖJÄ ({sisalla})")
    for i in range(12):
        if st.button(lyoja_lista[i], key=f"lk{i}", use_container_width=True): 
            st.session_state.v_lyoja = lyoja_lista[i]

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
    for i, t in enumerate(["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]):
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
    for i, t in enumerate(["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]):
        if tr_cols[i % 2].button(t, key=f"tr_{t}", use_container_width=True): st.session_state.v_tulos = t

    st.write("---")
    st.caption(f"SUORITTAVA UP ({ulkona})")
    up_cols = st.columns(3)
    for i in range(12):
        if up_cols[i % 3].button(up_lista[i], key=f"up{i}", use_container_width=True): st.session_state.v_up = up_lista[i]
    if st.button("OTTAMATON", use_container_width=True): st.session_state.v_up = "Ottamaton"

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
            "Jakso": jakso, "Vuoro": vuoro, "Tilanne": t_map[til_val], 
            "Sisällä": sisalla, "Lyöjä": st.session_state.v_lyoja, "Lyönti nro": st.session_state.v_lyonti_nro,
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

# --- 5. LOKI ---
st.write("---")
st.dataframe(st.session_state.data, use_container_width=True)

if not st.session_state.data.empty:
    csv = st.session_state.data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Lataa CSV", csv, "kpl_tahko_data.csv", "text/csv")
