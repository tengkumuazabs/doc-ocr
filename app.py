# app.py
import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import numpy as np
from PIL import Image
import io
import requests

st.set_page_config(page_title="NIK Extractor", layout="centered")

st.title("🪪 Indonesian NIK Extractor using DocTR")
st.markdown("Upload an image of an Indonesian ID card (KTP) or provide a URL to extract the NIK using OCR.")

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
