# app.py
import streamlit as st
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import numpy as np
from PIL import Image
import io # Import the io module

st.set_page_config(page_title="NIK Extractor", layout="centered")

st.title("🪪 Indonesian NIK Extractor using DocTR")
st.markdown("Upload an image of an Indonesian ID card (KTP) and this app will extract the NIK (Nomor Induk Kependudukan) using OCR.")

# File uploader
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded KTP", use_container_width=True)

    # Convert PIL Image to an in-memory byte stream
    # This is a more robust way to pass image data to doctr when starting from a PIL Image
    img_byte_arr = io.BytesIO()
    # Save the PIL image to the byte stream in PNG format (or JPEG, depending on preference)
    image.save(img_byte_arr, format='PNG')
    # Get the bytes from the stream
    img_bytes = img_byte_arr.getvalue()

    # Load OCR model
    with st.spinner("🔍 Running OCR..."):
        model = ocr_predictor(pretrained=True)
        # Pass the image bytes directly to from_images
        # doctr can read image files from bytes
        doc = DocumentFile.from_images([img_bytes])
        result = model(doc)
        result_list = result.render().split('\n')

    # Try to extract NIK
    try:
        # Find the index of 'NIK' in the OCR result list
        nik_index = result_list.index('NIK')
        # The NIK value is typically on the next line after 'NIK'
        nik_raw = result_list[nik_index + 1]
    except (ValueError, IndexError):
        # If 'NIK' is not found or there's no line after it, set nik_raw to None
        nik_raw = None

    if nik_raw:
        # Clean possible OCR mistakes: replace common letter-digit confusions
        nik_fixed = nik_raw.replace('L', '1').replace('O', '0').replace('I', '1')
        # Filter out non-digit characters to get a clean NIK
        nik_clean = ''.join(filter(str.isdigit, nik_fixed))

        # Check if the cleaned NIK has the correct length (16 digits for Indonesian NIK)
        if len(nik_clean) == 16:
            st.success(f"✅ Extracted NIK: `{nik_clean}`")
        else:
            st.warning(f"⚠️ NIK length is invalid after cleaning: `{nik_clean}` (Expected 16 digits)")
    else:
        st.error("❌ NIK field not found in OCR result.")

    with st.expander("🔎 Full OCR Result"):
        st.text("\n".join(result_list))

