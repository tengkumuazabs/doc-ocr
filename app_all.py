import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import numpy as np
from PIL import Image
import io
import re
import requests

st.set_page_config(page_title="OCR docs Extractor", layout="centered")

tab1, tab2, tab3 = st.tabs(["NIK", "Income", "Birth Certificate"])

# Tab for NIK Extraction
with tab1:
    st.title("NIK Extractor")
    st.markdown("Upload an image of an Indonesian ID card (KTP) or provide a URL to extract the NIK.")

    # Two input options: upload or URL
    uploaded_file = st.file_uploader("📁 Upload an image", type=["jpg", "jpeg", "png"])
    url_input = st.text_input("🌐 Or enter image URL")

    image = None

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded KTP", use_container_width=True)

    elif url_input:
        try:
            response = requests.get(url_input)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            st.image(image, caption="Image from URL", use_container_width=True)
        except Exception as e:
            st.error(f"❌ Failed to load image from URL: {e}")

    if image is not None:
        # Convert PIL Image to byte array
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        with st.spinner("🔍 Running OCR..."):
            model = ocr_predictor(pretrained=True)
            doc = DocumentFile.from_images([img_bytes])
            result = model(doc)
            result_list = result.render().split('\n')

        # Extract NIK
        try:
            nik_index = result_list.index('NIK')
            nik_raw = result_list[nik_index + 1]
        except (ValueError, IndexError):
            nik_raw = None

        if nik_raw:
            nik_fixed = nik_raw.replace('L', '1').replace('O', '0').replace('I', '1')
            nik_clean = ''.join(filter(str.isdigit, nik_fixed))

            if len(nik_clean) == 16:
                st.success(f"✅ Extracted NIK: `{nik_clean}`")
            else:
                st.warning(f"⚠️ NIK length is invalid after cleaning: `{nik_clean}` (Expected 16 digits)")
        else:
            st.error("❌ NIK field not found in OCR result.")

        with st.expander("🔎 Full OCR Result"):
            st.text("\n".join(result_list))

# Tab for Income Extraction
with tab2:
    st.title("Income Extractor")
    st.markdown("Upload a PDF file containing income scans for OCR extraction.")

    # File uploader: only accept PDF
    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="income")

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

with tab3:
    st.title("Birth Certificate Extractor")
    st.markdown("Upload a PDF file containing birth certificate scans for OCR extraction.")

    # File uploader: only accept PDF
    uploaded_file = st.file_uploader("📁 Upload a PDF", type=["pdf"], key="birth")

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

               # Information to extract
        birth_cert_number = None
        child_name = None
        dob = None
        father_name = None
        mother_name = None

        # Search through OCR lines
        for line in result_lines:
            line = line.strip()

            # Extract Birth Certificate Number
            match = re.search(r'akta kelahiran nomor\s+([A-Z0-9\-]+)', line, re.IGNORECASE)
            if match:
                birth_cert_number = match.group(1)

            # Extract Date of Birth
            match = re.search(r' pada tanggal\s+(\d{2}-\d{2}-\d{4})', line, re.IGNORECASE)
            if match:
                dob = match.group(1)

            # Extract Child's Name
            try:
                name_index = result_lines.index('was born :')
                child_name = result_lines[name_index + 1]
            except (ValueError, IndexError):
                child_name = None

            # Extract Child's DOB City
            match = re.search(r'bahwa di\s+([A-Z\s]+)\s+pada tanggal', line, re.IGNORECASE)
            if match:
                dob_city = match.group(1).strip()

        # Display extracted information
        st.subheader("Extracted Birth Certificate Data")
        if birth_cert_number:
            st.success(f"Birth Certificate Number: `{birth_cert_number}`")
        if child_name:
            st.success(f"Child's Name: `{child_name}`")
        if dob:
            st.success(f"Date of Birth: `{dob}`")
        if dob_city:
            st.success(f"City: `{dob_city}`")

        if not any([birth_cert_number, child_name, dob, father_name, mother_name]):
            st.warning("Could not extract birth certificate details. Please check the document quality.")
