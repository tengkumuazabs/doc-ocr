import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

def show_prestasi():
    st.title("Bukti Prestasi Extractor")
    st.markdown("Upload a PDF file containing Bukti Prestasi scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="bukti_prestasi")

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

        # Define regex patterns
        patterns = {
            "nama": r"Nama\s*:?\s*(.+)",
            "nisn": r"NISN\s*:?\s*(.+)",
            "kelas": r"Kelas\s*:?\s*(.+)",
            "prestasi": r"adalah benar siswa kami yang aktif dan telah berhasil meraih prestasi sebagai berikut:\s*:?\s*(.+)"
        }

        # Extract fields
        extracted = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, result_text, re.IGNORECASE)
            if match:
                extracted[key] = match.group(1).strip()

        # Display extracted values
        st.subheader("✅ Extracted Data")
        for key, value in extracted.items():
            st.success(f"**{key.replace('_', ' ').title()}**: `{value}`")

        # Show as JSON
        st.subheader("🧾 JSON Output")
        st.json(extracted)
