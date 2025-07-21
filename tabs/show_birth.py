import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

def show_birth():
    st.title("Birth Certificate Extractor")
    st.markdown("Upload a PDF file containing birth certificate scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="birth")

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

        birth_cert_number = child_name = dob = dob_city = None

        for line in result_lines:
            line = line.strip()
            match = re.search(r'akta kelahiran nomor\s+([A-Z0-9\-]+)', line, re.IGNORECASE)
            if match:
                birth_cert_number = match.group(1)

            match = re.search(r' pada tanggal\s+(\d{2}-\d{2}-\d{4})', line, re.IGNORECASE)
            if match:
                dob = match.group(1)

            match = re.search(r'bahwa di\s+([A-Z\s]+)\s+pada tanggal', line, re.IGNORECASE)
            if match:
                dob_city = match.group(1).strip()

        try:
            name_index = result_lines.index('was born :')
            child_name = result_lines[name_index + 1]
        except (ValueError, IndexError):
            pass

        st.subheader("Extracted Birth Certificate Data")
        if birth_cert_number:
            st.success(f"Birth Certificate Number: `{birth_cert_number}`")
        if child_name:
            st.success(f"Child's Name: `{child_name}`")
        if dob:
            st.success(f"Date of Birth: `{dob}`")
        if dob_city:
            st.success(f"City: `{dob_city}`")

        if not any([birth_cert_number, child_name, dob, dob_city]):
            st.warning("Could not extract birth certificate details.")
