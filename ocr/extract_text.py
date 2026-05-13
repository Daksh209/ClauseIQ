import os
import re
import json
import pytesseract
from pdf2image import convert_from_path
import fitz

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def ocr_pdf(pdf_path):
    """
    OCR extraction using Tesseract
    """

    try:
        images = convert_from_path(pdf_path)

        text = ""

        for img in images:
            text += pytesseract.image_to_string(img)

        return text

    except Exception as e:
        print(f"OCR Error: {pdf_path} -> {e}")
        return ""


def extract_text_fast(pdf_path):
    """
    Direct text extraction using PyMuPDF
    """

    try:
        doc = fitz.open(pdf_path)

        return " ".join(
            [page.get_text() for page in doc]
        )

    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""


def clean_text(text):
    """
    Clean extracted text
    """

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def process_pdf(pdf_path):
    """
    Full OCR pipeline
    """

    text = extract_text_fast(pdf_path)

    method = "Direct"

    # fallback to OCR
    if len(text.strip()) < 50:
        text = ocr_pdf(pdf_path)
        method = "OCR"

    cleaned = clean_text(text)

    return {
        "file_name": os.path.basename(pdf_path),
        "method": method,
        "text": cleaned
    }


if __name__ == "__main__":

    pdf_path = "ocr/sample.pdf"

    result = process_pdf(pdf_path)

    print(json.dumps(result, indent=2))