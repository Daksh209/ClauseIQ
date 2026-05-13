from flask import Flask, request, jsonify

from ocr.extract_text import process_pdf
from validation.post_process import post_process

import spacy
import os

app = Flask(__name__)

# Load trained NER model
nlp = spacy.load("model_output")


@app.route('/')
def home():
    return "LexiScan Auto API Running"


@app.route('/extract', methods=['POST'])
def extract():

    # Check uploaded file
    if 'file' not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files['file']

    # Save uploaded file
    upload_path = os.path.join("uploads", file.filename)

    os.makedirs("uploads", exist_ok=True)

    file.save(upload_path)

    # OCR step
    ocr_result = process_pdf(upload_path)

    text = ocr_result["text"]

    # NER step
    doc = nlp(text)

    # Convert entities
    raw_entities = []

    for ent in doc.ents:
        raw_entities.append(
            (
                ent.start_char,
                ent.end_char,
                ent.label_,
                ent.text
            )
        )

    # Validation + normalization
    final_output = post_process(
        raw_entities,
        source_file=file.filename
    )

    return jsonify(final_output)


if __name__ == '__main__':
    app.run(debug=True)