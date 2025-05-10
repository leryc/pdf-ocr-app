
import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
import re

st.title("📄 PDF OCR Extractor")

uploaded_file = st.file_uploader("Upload a scanned PDF", type=["pdf"])

def clean_text(text):
    # Remove common OCR artifacts
    text = re.sub(r'[~|✓→►•◦■¤©®™¨]', '', text)
    text = re.sub(r'\b(?:J-|SY|v|—|_~|~~|¥|“|”|‘|’|†)\b', '', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

if uploaded_file is not None:
    st.info("⏳ Processing PDF...")
    try:
        images = convert_from_bytes(uploaded_file.read())
        full_text = ""
        for page in images:
            full_text += pytesseract.image_to_string(page) + "\n"
        cleaned = clean_text(full_text)
        st.success("✅ Text extracted!")
        st.text_area("Extracted Text", cleaned, height=400)
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
