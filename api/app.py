from flask import Flask, request, jsonify, render_template

from ocr.extract_text import process_pdf
from validation.post_process import post_process

import spacy
import os

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

# Load trained NER model
nlp = spacy.load("model_output")


@app.route('/')
def home():
    return render_template("index.html")
  
@app.route('/extract', methods=['POST'])
def extract():

    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected", 400

    os.makedirs("uploads", exist_ok=True)

    upload_path = os.path.join("uploads", file.filename)

    file.save(upload_path)

    # OCR
    ocr_result = process_pdf(upload_path)

    text = ocr_result["text"]
    
    # NER
    doc = nlp(text)

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
    
    return render_template(
        "result.html",
        result=final_output
    )


@app.route('/api/extract', methods=['POST'])
def api_extract():

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    os.makedirs("uploads", exist_ok=True)

    upload_path = os.path.join("uploads", file.filename)

    file.save(upload_path)

    ocr_result = process_pdf(upload_path)

    text = ocr_result["text"]
    
    doc = nlp(text)

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

    final_output = post_process(
        raw_entities,
        source_file=file.filename
    )

    return jsonify(final_output)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)