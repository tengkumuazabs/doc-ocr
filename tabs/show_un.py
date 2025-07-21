import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

def show_un():
    st.title("UN Score Extractor")
    st.markdown("Upload a PDF file containing UN Score scans for OCR extraction.")

    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="un_score")

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

        total_score = None
        average_score = None

        for i, val in enumerate(result_lines):
            if 'JUMLAH' in val.upper():
                try:
                    total_score = float(result_lines[i + 1])
                except:
                    pass
            elif 'RATA-RATA' in val.upper():
                try:
                    average_score = float(result_lines[i + 1])
                except:
                    pass

        # Display extracted values
        st.subheader("📊 Extracted Scores")
        if total_score is not None:
            st.success(f"Total Score: `{total_score}`")
        if average_score is not None:
            st.success(f"Average Score: `{average_score}`")

        # Show as JSON
        st.subheader("🧾 JSON Output")
        json = {
            "total_score": total_score,
            "average_score": average_score,
        }
        st.json(json)
