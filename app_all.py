import streamlit as st

# Import tab functions
from tabs.show_nik import show_nik
from tabs.show_income import show_income
from tabs.show_birth import show_birth
from tabs.show_un import show_un
from tabs.show_pkh import show_pkh
from tabs.show_bukti_univ import show_bukti_univ
from tabs.show_prestasi import show_prestasi

# List of (tab_name, function) pairs
tab_definitions = [
    ("NIK", show_nik),
    ("Income", show_income),
    ("Birth Certificate", show_birth),
    ("UN Score", show_un),
    ("PKH", show_pkh),
    ("Bukti Penerimaan", show_bukti_univ),
    ("Bukti Prestasi", show_prestasi)
]

# Create tabs dynamically
tab_titles = [name for name, _ in tab_definitions]
tabs = st.tabs(tab_titles)

# Assign each function to the corresponding tab
for tab, (_, tab_function) in zip(tabs, tab_definitions):
    with tab:
        tab_function()
