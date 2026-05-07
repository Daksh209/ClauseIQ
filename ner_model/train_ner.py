import spacy
from spacy.training.example import Example
import json
import random
from sklearn.model_selection import train_test_split

# Load model (keep this for now)
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Load training data
with open("ner_model/data/train_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Split data
train_data, val_data = train_test_split(data, test_size=0.2, random_state=42)

# Get NER
ner = nlp.get_pipe("ner")

# Add labels
for item in train_data:
    for ent in item["entities"]:
        ner.add_label(ent[2])

# Convert to examples
def create_examples(dataset):
    examples = []
    for item in dataset:
        doc = nlp.make_doc(item["text"])
        example = Example.from_dict(doc, {"entities": item["entities"]})
        examples.append(example)
    return examples

train_examples = create_examples(train_data)
val_examples = create_examples(val_data)

# Initialize
optimizer = nlp.initialize()

EPOCHS = 15

for epoch in range(EPOCHS):
    random.shuffle(train_examples)

    losses = {}

    # 🔥 Training
    for example in train_examples:
        nlp.update(
            [example],
            drop=0.3,
            losses=losses
        )

    print(f"\nEpoch {epoch} Loss: {losses}")

    # 🔥 VALIDATION (FIXED)
    correct = 0
    total = 0

    for example in val_examples:
        doc = nlp(example.text)

        pred_ents = {(ent.start_char, ent.end_char, ent.label_) for ent in doc.ents}

        true_ents = {
            (ent.start_char, ent.end_char, ent.label_)
            for ent in example.reference.ents
        }

        correct += len(pred_ents & true_ents)
        total += len(true_ents)

    if total > 0:
        recall = correct / total
        print(f"Validation Recall: {recall:.3f}")
    else:
        print("Validation Recall: N/A")

# Save model
nlp.to_disk("model_output")

print("\n✅ Model training complete!")