import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

def show_pkh():
    st.title("PKH Extractor")
    st.markdown("Upload a PDF file containing PKH scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="pkh")

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

        name = None
        participant_id = None

        for i, val in enumerate(result_lines):
            if 'nama kepala keluarga' in val.lower():
                try:
                    name = result_lines[i + 1]
                    participant_id = result_lines[i - 1].split()[2]
                except:
                    pass                    

        # Display extracted values
        if name is not None:
            st.success(f"Nama: `{name}`")
        if participant_id is not None:
            st.success(f"Participant ID: `{participant_id}`")

        # Show as JSON
        st.subheader("🧾 JSON Output")
        json = {
            "name": name,
            "participant_id": participant_id,
        }
        st.json(json)
