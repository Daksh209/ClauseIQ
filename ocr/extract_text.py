import os
import re
import json
import pytesseract
import fitz

from pdf2image import convert_from_path
from PIL import Image
from docx import Document

# -----------------------------------
# TESSERACT CONFIG
# -----------------------------------

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# -----------------------------------
# OCR FOR SCANNED PDF
# -----------------------------------

def ocr_pdf(pdf_path):

    try:

        images = convert_from_path(pdf_path)

        text = ""

        for img in images:

            text += pytesseract.image_to_string(img)

        return text

    except Exception as e:

        print(f"OCR Error: {pdf_path} -> {e}")

        return ""


# -----------------------------------
# FAST PDF TEXT EXTRACTION
# -----------------------------------

def extract_text_fast(pdf_path):

    try:

        doc = fitz.open(pdf_path)

        return " ".join(
            [page.get_text() for page in doc]
        )

    except Exception as e:

        print(f"Extraction Error: {e}")

        return ""


# -----------------------------------
# IMAGE OCR
# -----------------------------------

def extract_image_text(image_path):

    try:

        image = Image.open(image_path)

        text = pytesseract.image_to_string(image)

        return text

    except Exception as e:

        print(f"Image OCR Error: {e}")

        return ""


# -----------------------------------
# DOCX EXTRACTION
# -----------------------------------

def extract_docx_text(docx_path):

    try:

        doc = Document(docx_path)

        text = "\n".join(
            [para.text for para in doc.paragraphs]
        )

        return text

    except Exception as e:

        print(f"DOCX Extraction Error: {e}")

        return ""


# -----------------------------------
# TXT EXTRACTION
# -----------------------------------

def extract_txt_text(txt_path):

    try:

        with open(
            txt_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as e:

        print(f"TXT Extraction Error: {e}")

        return ""


# -----------------------------------
# TEXT CLEANING
# -----------------------------------

def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# -----------------------------------
# UNIVERSAL DOCUMENT PROCESSOR
# -----------------------------------

def process_document(file_path):

    extension = os.path.splitext(
        file_path
    )[1].lower()

    text = ""

    method = ""

    # -----------------------------------
    # PDF DOCUMENTS
    # -----------------------------------

    if extension == ".pdf":

        text = extract_text_fast(file_path)

        method = "Direct PDF Extraction"

        # fallback OCR for scanned PDFs

        if len(text.strip()) < 50:

            text = ocr_pdf(file_path)

            method = "OCR PDF Extraction"

    # -----------------------------------
    # IMAGE FILES
    # -----------------------------------

    elif extension in [
        ".png",
        ".jpg",
        ".jpeg"
    ]:

        text = extract_image_text(file_path)

        method = "Image OCR Extraction"

    # -----------------------------------
    # DOCX FILES
    # -----------------------------------

    elif extension == ".docx":

        text = extract_docx_text(file_path)

        method = "DOCX Text Extraction"

    # -----------------------------------
    # TXT FILES
    # -----------------------------------

    elif extension == ".txt":

        text = extract_txt_text(file_path)

        method = "TXT Text Extraction"

    # -----------------------------------
    # UNSUPPORTED FILES
    # -----------------------------------

    else:

        return {

            "file_name": os.path.basename(file_path),

            "method": "Unsupported File",

            "text": ""
        }

    # -----------------------------------
    # CLEAN EXTRACTED TEXT
    # -----------------------------------

    cleaned = clean_text(text)

    # -----------------------------------
    # FINAL OUTPUT
    # -----------------------------------

    return {

        "file_name": os.path.basename(file_path),

        "method": method,

        "text": cleaned
    }


# -----------------------------------
# TESTING
# -----------------------------------

if __name__ == "__main__":

    file_path = "uploads/sample.pdf"

    result = process_document(file_path)

    print(json.dumps(result, indent=2))