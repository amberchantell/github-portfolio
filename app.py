import streamlit as st

st.set_page_config(page_title="Technical Writing Doc-Ops", page_icon="📝", layout="wide")

st.markdown("""
    <style>
    .main-header {
        font-size: 2.25rem;
        font-weight: 700;
        color: #1E293B;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📝 Technical Writing Doc-Ops</div>', unsafe_allow_html=True)
st.write("Welcome to the Technical Writing Doc-Ops dashboard.")
