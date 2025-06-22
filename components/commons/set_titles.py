import streamlit as st

def set_main_title(name):
    st.markdown(f"""
        <h1 style='text-align: center; font-size: 2.5rem; margin-bottom: 2rem;'>{name}</h1>
    """, unsafe_allow_html=True)

def set_sub_title(name):
    st.markdown(f"""
        <h2 style='text-align: center; margin-bottom: 0.5rem; margin-top: -2rem;'>{name}</h2>
    """, unsafe_allow_html=True)