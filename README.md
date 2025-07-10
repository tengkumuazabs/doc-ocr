# Indonesian NIK Extractor using DocTR

This is a simple Streamlit app that uses Optical Character Recognition (OCR) to extract the **NIK (Nomor Induk Kependudukan)** from an image of an Indonesian ID card (KTP).

Built using [DocTR](https://github.com/mindee/doctr), a deep learning-based OCR toolkit.

## Live Demo

Experience the app live here: [Live App](https://doc-ocr.streamlit.app/)  
*Note: If the app is inactive, please click the **REBOOT** button to start it.*

## Features

- Upload KTP image from your device
- Or input a URL to an image
- Automatically extracts and displays the NIK
- Uses pretrained OCR model (DocTR)
- Handles common OCR misreads (e.g., `O` → `0`, `L` → `1`)



## Supported Input

- `.jpg`, `.jpeg`, `.png` image files
- Publicly accessible image URLs



## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/doc-ocr.git
cd doc-ocr
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

