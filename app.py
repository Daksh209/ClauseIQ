from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# Load trained model
nlp = spacy.load(".")

@app.route('/')
def home():
    return "LexiScan API Running"

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    text = data.get("text")

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    return jsonify({
        "entities": entities
    })

if __name__ == '__main__':
    app.run(debug=True)