import streamlit as st
import pandas as pd
from datetime import datetime

# --- ASETUKSET ---
st.set_page_config(page_title="Pesis Live Syöttö", layout="wide")

# Lisätty värejä ja korostuksia CSS:ään
st.markdown("""
    <style>
    .main .block-container { padding: 0.5rem 1rem !important; }
    .stButton > button { padding: 0px 2px !important; font-size: 11px !important; height: 26px !important; border-radius: 2px !important; }
    /* Korostetaan valittuja elementtejä */
    .stAlert { padding: 0.5rem !important; margin-bottom: 0.5rem !important; }
    div[data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
    div.stRadio > div { gap: 2px !important; padding: 0px !important; }
    hr { margin: 0.3rem 0 !important; }
    
    /* Aktiivisen valinnan korostusväri (vihreä sävy) */
    .selected-box {
        background-color: #e1f5fe;
        padding: 5px;
        border-radius: 5px;
        border-left: 5px solid #0288d1;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Alustukset
if 'data' not in st.session_state: st.session_state.data = pd.DataFrame()
vars_to_init = ['v_lyoja', 'v_suunta', 'v_tyyppi', 'v_tulos', 'v_up', 'v_up_laatu', 'v_lyonti_nro', 'v_sisapeli']
for var in vars_to_init:
    if var not in st.session_state: st.session_state[var] = "-"

# --- 1. NIMIEN SYÖTTÖ ---
with st.expander("📝 ASETA JOUKKUEET JA PELAAJAT", expanded=False):
    c_k, c_v = st.columns(2)
    koti_nimi = c_k.text_input("Kotijoukkue", "KPL")
    vieras_nimi = c_v.text_input("Vierasjoukkue", "Tahko")
    koti_nimet_raw = c_k.text_area(f"{koti_nimi}: Pelaajat", "1. Saukko\n2. Vartama\n3. Pitkänen\n4. Ruuska\n5. J. Luoma\n6. V. Luoma\n7. Latvala\n8. Laine\n9. Pesonen\n10. Nikkanen\n11. Toivola\n12. Alanen", height=150)
    vieras_nimet_raw = c_v.text_area(f"{vieras_nimi}: Pelaajat", "1. Nurmio\n2. Kauppinen\n3. Kettunen\n4. Kortehisto\n5. Kyhyräinen\n6. Raesmaa\n7. Kuosmanen\n8. Heikkala\n9. Tuomi\n10. Niemi\n11. Patova\n12. Matikka", height=150)
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

# --- VISUAALINEN KOONTI (Mitä on painettu) ---
st.markdown(f"""
    <div class="selected-box">
        <b>NYKYINEN VALINTA:</b><br>
        👤 {st.session_state.v_lyoja} | 🎯 {st.session_state.v_tyyppi} ({st.session_state.v_suunta}) | 
        🏁 {st.session_state.v_tulos} | ⭐ {st.session_state.v_sisapeli} | 🛡️ {st.session_state.v_up} ({st.session_state.v_up_laatu})
    </div>
    """, unsafe_allow_html=True)

# --- 3. SYÖTTÖNÄKYMÄ ---
col_l, col_m, col_r = st.columns([1.8, 3.2, 2.5])

with col_l:
    st.caption("LYÖJÄ")
    for i, nimi in enumerate(lyoja_lista):
        # Muutetaan napin tyyliä jos se on valittu
        type_style = "primary" if st.session_state.v_lyoja == nimi else "secondary"
        if st.button(nimi, key=f"l_{i}", use_container_width=True, type=type_style):
            st.session_state.v_lyoja = nimi
            st.rerun()

with col_m:
    tc1, tc2, tc3 = st.columns([2, 1, 1])
    t_map = {"0": "0 til", "1": "1 til", "0-2": "0-2", "0-3": "0-3", "1-2": "1-2", "1-3": "1-3", "2-3": "2-3", "Ajo": "Ajo"}
    til_val = tc1.radio("Tilanne", list(t_map.keys()), horizontal=True)
    palot = tc2.radio("Palot", ["0", "1", "2"], horizontal=True)
    st.session_state.v_lyonti_nro = tc3.radio("Lyönti", ["1", "2", "3"], horizontal=True)

    merkattu = st.checkbox("Merkattu", key="merk_val")
    st.write("---")

    st.caption("LYÖNTITYYPPI")
    ly_cols = st.columns(3)
    tyypit = ["Pieni", "Pomppu", "Pussari", "Varsi", "Kova", "Hämylähtö", "Koppi", "Vapaa", "Kumura"]
    for i, t in enumerate(tyypit):
        t_style = "primary" if st.session_state.v_tyyppi == t else "secondary"
        if ly_cols[i % 3].button(t, key=f"lt_{t}", use_container_width=True, type=t_style):
            st.session_state.v_tyyppi = t
            st.rerun()

    st.write("---")
    st.caption("SUUNTA")
    s_cols = st.columns(3)
    suunnat = ["3 jatke", "3 taakse", "3 luukku", "3 sauma", "keskitakanen", "keskisauma", "keskipieni", "2 jatke", "2 taakse", "2 luukku", "2 sauma", "2 raja", "3 raja"]
    for i, s in enumerate(suunnat):
        s_style = "primary" if st.session_state.v_suunta == s else "secondary"
        if s_cols[i % 3].button(s, key=f"s_{s}", use_container_width=True, type=s_style):
            st.session_state.v_suunta = s
            st.rerun()

with col_r:
    st.caption("TULOS")
    tr_cols = st.columns(2)
    tulokset = ["palo", "haava", "eteni", "laiton", "vaihto", "juoksu", "kentällemeno", "vapaataival", "tuottamaton"]
    for i, t in enumerate(tulokset):
        tr_style = "primary" if st.session_state.v_tulos == t else "secondary"
        if tr_cols[i % 2].button(t, key=f"tr_{t}", use_container_width=True, type=tr_style):
            st.session_state.v_tulos = t
            st.rerun()

    st.caption("ONNISTUNUT / EPÄONNISTUNUT")
    s_col1, s_col2 = st.columns(2)
    # Vihreä onnistuneelle, punainen epäonnistuneelle jos valittu
    if s_col1.button("✅ ONNISTUNUT", use_container_width=True, type="primary" if st.session_state.v_sisapeli == "Onnistunut" else "secondary"):
        st.session_state.v_sisapeli = "Onnistunut"
        st.rerun()
    if s_col2.button("❌ EPÄONNISTUNUT", use_container_width=True, type="primary" if st.session_state.v_sisapeli == "Epäonnistunut" else "secondary"):
        st.session_state.v_sisapeli = "Epäonnistunut"
        st.rerun()

    st.write("---")
    st.caption(f"UP ({ulkona})")
    up_cols = st.columns(3)
    for i, nimi in enumerate(up_lista):
        u_style = "primary" if st.session_state.v_up == nimi else "secondary"
        if up_cols[i % 3].button(nimi, key=f"u_{i}", use_container_width=True, type=u_style):
            st.session_state.v_up = nimi
            st.rerun()
    
    if st.button("OTTAMATON", use_container_width=True, type="primary" if st.session_state.v_up == "Ottamaton" else "secondary"):
        st.session_state.v_up = "Ottamaton"
        st.rerun()

    st.caption("UP-SUORITUS")
    la_cols = st.columns(3)
    for i, la in enumerate(["PUHDAS", "NAKITUS", "HARHAHEITTO"]):
        la_style = "primary" if st.session_state.v_up_laatu == la else "secondary"
        if la_cols[i].button(la, key=f"la_{la}", use_container_width=True, type=la_style):
            st.session_state.v_up_laatu = la
            st.rerun()

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
            "Tulos": st.session_state.v_tulos, "Sisäpeli": st.session_state.v_sisapeli,
            "UP": st.session_state.v_up, "UP-Laatu": st.session_state.v_up_laatu, 
            "Kuvio": up_kuvio, "Takapalo": "Takapalo" if takapalo else ""
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([uusi])], ignore_index=True)
        for k in vars_to_init: st.session_state[k] = "-"
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
