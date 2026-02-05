import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Pesis-Tilastoija", layout="wide")

# Tiedoston nimi, johon data tallentuu (Streamlit-pilvessä tämä on väliaikainen)
TIEDOSTO = "otteludata.csv"

st.title("⚾ Pesis-Tilastoija Web")

# Ottelun perustiedot
with st.expander("Ottelun tiedot", expanded=True):
    c1, c2 = st.columns(2)
    koti = c1.text_input("Koti", "Koti")
    vieras = c2.text_input("Vieras", "Vieras")
    ottelu_id = f"{datetime.now().strftime('%Y%m%d')}_{koti}_{vieras}"

# Syöttölomake (vastaa pesis_kerain.py:n toiminnallisuutta)
with st.form("syotto"):
    col1, col2, col3 = st.columns(3)
    with col1:
        joukkue = st.radio("Joukkue", [koti, vieras])
        lyoja = st.number_input("Lyöjä nro", 1, 12)
    with col2:
        tilanne = st.selectbox("Tilanne", ["0-tilanne", "1-tilanne", "2-tilanne", "3-tilanne", "Ajolähtö"])
        tulos = st.selectbox("Tulos", ["PALO", "HAAVA", "VAIHTO", "KENTÄLLEMENO", "JUOKSU"])
    with col3:
        tyyppi = st.selectbox("Lyönti", ["Kova", "Kumura", "Pomppu", "Pieni"])
        suunta = st.selectbox("Suunta", ["2-puoli", "Keskelle", "3-puoli"])
    
    submit = st.form_submit_button("Tallenna tapahtuma")

if submit:
    uusi = [[ottelu_id, tilanne, joukkue, f"P{lyoja}", tyyppi, suunta, tulos]]
    df = pd.DataFrame(uusi, columns=["ID", "Tilanne", "Joukkue", "Lyöjä", "Tyyppi", "Suunta", "Tulos"])
    df.to_csv(TIEDOSTO, mode='a', index=False, header=not os.path.isfile(TIEDOSTO))
    st.success("Tallennettu!")

# Näytetään loki
if os.path.isfile(TIEDOSTO):
    st.dataframe(pd.read_csv(TIEDOSTO).tail(5))
