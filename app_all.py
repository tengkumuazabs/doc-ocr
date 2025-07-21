import streamlit as st

# Import tab modules
from tabs.show_nik import show_nik
from tabs.show_income import show_income
from tabs.show_birth import show_birth
from tabs.show_un import show_un

st.set_page_config(page_title="OCR docs Extractor", layout="centered")

tab1, tab2, tab3, tab4 = st.tabs(["NIK", "Income", "Birth Certificate", "UN Score"])

with tab1:
    show_nik()

with tab2:
    show_income()

with tab3:
    show_birth()

with tab4:
    show_un()
