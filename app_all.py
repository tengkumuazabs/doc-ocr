import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import numpy as np
from PIL import Image
import io
import re

st.set_page_config(page_title="Income Extractor", layout="centered")

st.title("🪪 Income Extractor")
# st.markdown("Upload a PDF file containing KTP scans for OCR extraction.")

# File uploader: only accept PDF
uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"])

if uploaded_file:
    st.info("📄 PDF uploaded.")

    with st.spinner("🔍 Running OCR..."):
        # Load document from uploaded PDF
        doc = DocumentFile.from_pdf(uploaded_file.read())
        
        # Load the OCR model
        model = ocr_predictor(pretrained=True)

        # Run OCR
        result = model(doc)
        result_text = result.render()
        result_lines = result_text.split('\n')

    # Show OCR Result
    with st.expander("🔎 Full OCR Result"):
        st.text(result_text)

    # # Attempt to find NIK
    # nik_raw = None
    # for i, line in enumerate(result_lines):
    #     if "NIK" in line.upper():
    #         try:
    #             nik_raw = result_lines[i + 1]
    #             break
    #         except IndexError:
    #             pass

    # if nik_raw:
    #     nik_fixed = nik_raw.replace('L', '1').replace('O', '0').replace('I', '1')
    #     nik_clean = ''.join(filter(str.isdigit, nik_fixed))

    #     if len(nik_clean) == 16:
    #         st.success(f"✅ Extracted NIK: {nik_clean}")
    #     else:
    #         st.warning(f"⚠️ NIK length is invalid after cleaning: {nik_clean} (Expected 16 digits)")
    # else:
    #     st.error("❌ NIK field not found in OCR result.")

    
     # Attempt to find Income
    keywords = ["penghasilan rata-rata", "gaji bersih (a - b)"]
    income_raw = None

    for i, line in enumerate(result_lines):
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in keywords):
            if i + 1 < len(result_lines):
                income_raw = result_lines[i + 1]
            break

    if income_raw:
        match = re.search(r'[\d\.]+,\d+', income_raw)
        if match:
            income_str = match.group()
            # Convert to float by replacing . with nothing and , with .
            income_float = float(income_str.replace('.', '').replace(',', '.'))
        
        col1, col2 = st.columns(2)

        score = 0

        with col1:
            st.success(f"✅ Extracted Income: {income_float}")

        with col2:
            if income_float > 4000000:
                score = 0
            elif (income_float <= 4000000) & (income_float > 3000000):
                score = 10
            elif (income_float <= 3000000) & (income_float > 2000000):
                score = 20
            elif (income_float <= 2000000) & (income_float > 1000000):
                score = 30
            else:
                score = 35
            st.warning(f"Score : {score}")
            
    else:
        st.error("❌ Income field not found in OCR result.")
