import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re

def show_income():
    st.title("Income Extractor")
    st.markdown("Upload a PDF file containing income scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="income")

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

        keywords = ["penghasilan rata-rata", "gaji bersih (a - b)"]
        income_raw = None

        for i, line in enumerate(result_lines):
            if any(keyword in line.lower() for keyword in keywords):
                if i + 1 < len(result_lines):
                    income_raw = result_lines[i + 1]
                break

        if income_raw:
            match = re.search(r'[\d\.]+,\d+', income_raw)
            if match:
                income_str = match.group()
                income_float = float(income_str.replace('.', '').replace(',', '.'))

                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"✅ Extracted Income: {income_float}")
                with col2:
                    if income_float > 4000000:
                        score = 0
                    elif income_float > 3000000:
                        score = 10
                    elif income_float > 2000000:
                        score = 20
                    elif income_float > 1000000:
                        score = 30
                    else:
                        score = 35
                    st.warning(f"Score : {score}")
        else:
            st.error("❌ Income field not found in OCR result.")

        # Show as JSON
        st.subheader("🧾 JSON Output")
        json = {
            "income_float": income_float,
            "score": score
        }
        st.json(json)