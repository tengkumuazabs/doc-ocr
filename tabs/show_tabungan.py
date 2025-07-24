import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

def extract_fields(lines):
    bank_name = None
    bank_location = None
    account_number = None
    account_type = None
    name = None
    opening_date = None
    address = None

    for i, line in enumerate(lines):
        l = line.strip().upper()

        # Bank name: look for line containing "BANK"
        if not bank_name and "BANK" in l:
            bank_name = line.strip()

        # Bank location: line starts with KC
        if not bank_location and l.startswith("KC"):
            bank_location = line.strip()

        # Account number and type are under "Jenis Tabungan"
        if "JENIS TABUNGAN" in l and i + 2 < len(lines):
            acc_num_candidate = lines[i + 1].strip()
            if re.match(r"^\d{10,16}$", acc_num_candidate):
                account_number = acc_num_candidate
                account_type = lines[i + 2].strip()

        # Name is 2 lines below "Nama Lengkap"
        if "NAMA LENGKAP" in l and i + 2 < len(lines):
            name = lines[i + 2].strip()

        # Opening date is 3 lines below "Tanggal Pembukaan"
        if "TANGGAL PEMBUKAAN" in l and i + 2 < len(lines):
            opening_date = lines[i + 2].strip()

        # Address is 1 line below "Alamat"
        if "ALAMAT" in l and i + 1 < len(lines):
            address = lines[i + 1].strip()

    return {
        "bank_name": bank_name,
        "bank_location": bank_location,
        "account_number": account_number,
        "account_type": account_type,
        "name": name,
        "opening_date": opening_date,
        "address": address,
    }

def show_tabungan():
    st.title("Tabungan Extractor")
    st.markdown("Upload a PDF file containing Tabungan scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="tabungan")

    if uploaded_file:
        st.info("📄 PDF uploaded.")
        with st.spinner("🔍 Running OCR..."):
            doc = DocumentFile.from_pdf(uploaded_file.read())
            model = ocr_predictor(pretrained=True)
            result = model(doc)
            result_text = result.render()
            result_lines = result_text.split('\n')

        with st.expander("🔎 Full OCR Result"):
            st.text(result_text)

        # Extract fields using revised method
        extracted_data = extract_fields(result_lines)

        # Display extracted values
        for key, value in extracted_data.items():
            if value:
                st.success(f"**{key.replace('_', ' ').title()}**: `{value}`")

        # Show as JSON
        st.subheader("🧾 JSON Output")
        st.json(extracted_data)
