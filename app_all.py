import streamlit as st

# Import tab functions
from tabs.show_nik import show_nik
from tabs.show_income import show_income
from tabs.show_birth import show_birth
from tabs.show_un import show_un
from tabs.show_pkh import show_pkh  # Assuming you plan to use this

# List of (tab_name, function) pairs
tab_definitions = [
    ("NIK", show_nik),
    ("Income", show_income),
    ("Birth Certificate", show_birth),
    ("UN Score", show_un),
    ("PKH", show_pkh)
]

# Create tabs dynamically
tab_titles = [name for name, _ in tab_definitions]
tabs = st.tabs(tab_titles)

# Assign each function to the corresponding tab
for tab, (_, tab_function) in zip(tabs, tab_definitions):
    with tab:
        tab_function()
