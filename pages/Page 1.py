import streamlit as st

st.title("Page 1")

if st.button("← Retour à l'accueil"):
    st.switch_page("App.py")