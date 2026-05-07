import spacy

nlp = spacy.load("model_output")

text = """
This Agreement is made effective as of April 10, 2025 between Delta Ltd and Omega Corp.
The payment amount is $12000.
"""

doc = nlp(text)

print("\nDetected Entities:\n")

if len(doc.ents) == 0:
    print("No entities detected yet.")
else:
    for ent in doc.ents:
        print(ent.text, ent.label_)