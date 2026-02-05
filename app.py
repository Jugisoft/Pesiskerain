import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET JA ÄÄRIMMÄINEN TIIVISTYS ---
st.set_page_config(page_title="Pesis Live v3.0", layout="wide")

st.markdown("""
    <style>
    /* Pakotetaan koko sovellus mahtumaan yhdelle näytölle */
    .main .block-container { padding: 0.5rem 1rem !important; }
    .stButton > button { padding: 0px 0px !important; font-size: 10px !important; height: 22px !important; line-height: 22px !important; }
    .stRadio > div { gap: 2px !important; padding: 0px !important; }
    label { font-size: 11px !important; margin-bottom: 0px !important; }
    hr { margin: 0.5rem 0 !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
for var in ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up_pelaaja', 'v_up_laatu']:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. YLÄRIVI (Kompakti) ---
c1, c2, c3, c4, c5 = st.columns([1, 1.5, 1.5, 0.7, 0.8])
pvm = c1.date_input("Pvm", datetime.now(), label_visibility="collapsed")
koti_n = c2.text_input("Koti", "Kouvola", label_visibility="collapsed")
vieras_n = c3.text_input("Vieras", "Hyvinkää", label_visibility="collapsed")
jakso = c4.selectbox("J", ["1", "2", "S", "K"], label_visibility="collapsed")
vuorot = [f"{n}{v}" for n in range(1,5) for v in ["A", "L"]]
vuoro = c5.selectbox("V", vuorot, label_visibility="collapsed")

# --- 2. TILANNE JA PALOT (Yksi tiivis rivi) ---
t_map = {"0": "0 tilanne", "1": "1 tilanne", "0-2": "0-2 tilanne", "0-3": "0-3 tilanne", 
         "1-2": "1-2 tilanne", "1-3": "1-3 tilanne", "2-3": "2-3 tilanne", "Ajo": "Ajolähtö"}
tc1, tc2 = st.columns([3, 1])
til_lyhyt = tc1.radio("Tilanne", list(t_map.keys()), horizontal=True, label_visibility="collapsed")
palot = tc2.radio("Palot", ["0", "1", "2"], horizontal=True, label_visibility="collapsed")

st.write(f"**L:** {st.session_state.v_lyoja} | **S:** {st.session_state.v_suunta} | **T:** {st.session_state.v_tyyppi} | **R:** {st.session_state.v_tulos} | **UP:** {st.session_state.v_up_pelaaja} ({st.session_state.v_up_laatu})")

# --- 3. PÄÄGRIDI ---
col1, col2, col3, col4 = st.columns([0.8, 1.5, 1.5, 1.5])

# SARAKE 1: Lyöjät
with col1:
    st.caption("Lyöjä")
    k_c, v_c = st.columns(2)
    for i in range(1, 13):
        if k_c.button(f"K{i}", key=f"lk{i}", use_container_width=True): st.session_state.v_lyoja = f"K{i}"
        if v_c.button(f"V{i}", key=f"lv{i}", use_container_width=True): st.session_state.v_lyoja = f"V{i}"

# SARAKE 2: Lyöntityyppi ja Suunnat
with col2:
    st.caption("Tyyppi")
    lt1, lt2 = st.columns(2)
    l_tyypit = ["Pieni", "Pomppu", "Pussari", "Varsi", "M-Kova", "Hämy", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(l_tyypit):
        col = lt1 if i % 2 == 0 else lt2
        if col.button(t, key=f"lt_{t}", use_container_width=True): st.session_state.v_tyyppi = t
    
    st.caption("Suunta")
    s1, s2 = st.columns(2)
    kaikki_suunnat = ["3 jatke", "3 taakse", "3 luukku", "3 sauma", "keskitakanen", "keskisauma", "keskipieni", "2 taakse", "2 luukku", "2 sauma", "2 raja", "1 raja"]
    for i, s in enumerate(kaikki_suunnat):
        col = s1 if i % 2 == 0 else s2
        if col.button(s, key=f"s_{s}", use_container_width=True): st.session_state.v_suunta = s

# SARAKE 3: Tulos ja UP-pelaaja
with col3:
    st.caption("Tulos")
    tr1, tr2 = st.columns(2)
    t_lista = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno"]
    for i, t in enumerate(t_lista):
        col = tr1 if i % 2 == 0 else tr2
        if col.button(t, key=f"tr_{t}", use_container_width=True): st.session_state.v_tulos = t

    st.caption("Ulkopelaaja")
    up1, up2 = st.columns(2)
    for i in range(1, 13):
        col = up1 if i % 2 == 0 else up2
        if col.button(f"#{i}", key=f"up{i}", use_container_width=True): st.session_state.v_up_pelaaja = str(i)
    if st.button("OTTAMATON", use_container_width=True): st.session_state.v_up_pelaaja = "Ottamaton"

# SARAKE 4: Laatu ja Tallennus
with col4:
    st.caption("UP-Laatu")
    # Poistettu oletus (index=None Streamlitissä vaatisi selectboxin, käytetään "-" alustusta)
    if st.button("PUHDAS (PALO)", use_container_width=True): st.session_state.v_up_laatu = "Puhdas"
    if st.button("NAKITUS (VIRHE)", use_container_width=True): st.session_state.v_up_laatu = "Nakitus"
    
    st.divider()
    merkattu = st.checkbox("MERKKI")
    takapalo = st.checkbox("TAKAPALO")
    up_kuvio = st.selectbox("UP-Kuvio", ["", "MIKE", "PERTSA", "PYP"], label_visibility="collapsed")
    
    st.write("---")
    if st.button("💾 TALLENNA", type="primary", use_container_width=True):
        onnistuminen = "Onnistunut" if st.session_state.v_tulos in ["juoksu", "vaihto", "eteni", "kentällemeno"] else "Epäonnistunut"
        uusi = {
            "Pvm": pvm, "Jakso": jakso, "Vuoro": vuoro, "Tilanne": t_map[til_lyhyt], "Lyöjä": st.session_state.v_lyoja,
            "Palot": palot, "Lyönti": st.session_state.v_tyyppi, "Merkattu": "M" if merkattu else "",
            "Suunta": st.session_state.v_suunta, "Tulos": st.session_state.v_tulos,
            "Onnistuminen": onnistuminen, "UP-Pelaaja": st.session_state.v_up_pelaaja, 
            "UP-Laatu": st.session_state.v_up_laatu, "UP-KUVIO": up_kuvio, "Takapalo": "K" if takapalo else ""
        }
        st.session_state.data = pd.concat([pd.DataFrame([uusi]), st.session_state.data], ignore_index=True)
        # Nollaus
        for k in ['v_suunta', 'v_tyyppi', 'v_tulos', 'v_up_pelaaja', 'v_up_laatu']: st.session_state[k] = "-"
        st.rerun()

st.dataframe(st.session_state.data.head(1), use_container_width=True)
