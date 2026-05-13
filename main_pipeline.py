from ocr.extract_text import process_pdf
import spacy
import json

# Load trained NER model
nlp = spacy.load("model_output")

# Process PDF
ocr_result = process_pdf("ocr/sample.pdf")

text = ocr_result["text"]

# Run NER
doc = nlp(text)

# Store entities
entities = []

for ent in doc.ents:
    entities.append({
        "text": ent.text,
        "label": ent.label_
    })

# Final output
final_output = {
    "file_name": ocr_result["file_name"],
    "method": ocr_result["method"],
    "entities": entities
}

print(json.dumps(final_output, indent=2))