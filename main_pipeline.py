from ocr.extract_text import process_pdf
from validation.post_process import post_process

import spacy
import json

# Load trained model
nlp = spacy.load("model_output")

# OCR step
ocr_result = process_pdf("ocr/sample.pdf")

text = ocr_result["text"]

# NER step
doc = nlp(text)

# Convert entities into validation format
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
    source_file=ocr_result["file_name"]
)

# Print final JSON
print(json.dumps(final_output, indent=2))