import streamlit as st
import base64
import html


def set_main_title(name, logo):
    with open(logo, "rb") as f:
        logo = base64.b64encode(f.read()).decode()

    st.html(f"""
        <div style="
            width: 100%;
            display: grid;
            grid-template-columns: 1fr;
            justify-items: center;
            text-align: center;
        ">
            <img
                src="data:image/png;base64,{logo}"
                style="
                    display: block;
                    width: 150px;
                    height: auto;
                    margin: 0 auto 20px auto;
                "
            />

            <div style="
                display: block;
                width: 100%;
                text-align: center;
                font-family: sans-serif;
                font-size: 36px;
                font-weight: bold;
                margin: 0 0 30px 0;
            ">
                {html.escape(name)}
            </div>
        </div>
        """)


def set_sub_title(name):
    st.markdown(f"""
        <h2 style='text-align: center; margin-bottom: 0.5rem; margin-top: -2rem;'>{name}</h2>
    """, unsafe_allow_html=True)


def set_sub_sub_title(name):
    st.markdown(f"""
        <h3 style='text-align: center; margin-bottom: 0.5rem; margin-top: 0rem;'>{name}</h3>
    """, unsafe_allow_html=True)


def set_sub_sub_sub_title(name):
    st.markdown(f"""
        <h4 style='text-align: center; margin-bottom: 0.5rem; margin-top: 0rem;'>{name}</h4>
    """, unsafe_allow_html=True)
