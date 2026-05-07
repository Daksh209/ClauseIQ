import json

input_path = "CUAD_v1/CUAD_v1.json"
output_path = "ner_model/data/train_data.json"

train_data = []

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["data"]:
    for para in item["paragraphs"]:
        text = para["context"]
        entities = []

        for qa in para["qas"]:
            q = qa["question"].lower()

            for ans in qa["answers"]:
                start = ans["answer_start"]
                end = start + len(ans["text"])

                # 🔥 Improved label mapping
                if "date" in q:
                    label = "DATE"

                elif "party" in q or "parties" in q:
                    label = "ORG"

                elif "amount" in q or "price" in q or "payment" in q:
                    label = "MONEY"

                else:
                    continue

                entity = (start, end, label)

                # avoid duplicates
                if entity not in entities:
                    entities.append(entity)

        # 🔥 Remove overlapping entities
        entities = sorted(entities, key=lambda x: (x[0], x[1]))

        filtered = []
        last_end = -1

        for ent in entities:
            if ent[0] >= last_end:
                filtered.append(ent)
                last_end = ent[1]

        entities = filtered

        # ✅ ADD THIS (THIS WAS MISSING)
        if entities:
            train_data.append({
                "text": text,
                "entities": entities
            })

extra_data = [
    {
        "text": "Agreement signed on 10 April 2025 between Delta Ltd for $12000.",
        "entities": [
            (22, 36, "DATE"),
            (45, 54, "ORG"),
            (59, 65, "MONEY")
        ]
    },
    {
        "text": "ABC Pvt Ltd agrees to pay $50000 on 5 May 2024.",
        "entities": [
            (0, 12, "ORG"),
            (24, 30, "MONEY"),
            (34, 44, "DATE")
        ]
    },
    {
        "text": "The contract between Omega Corp and Sigma Ltd is valued at $75000.",
        "entities": [
            (21, 31, "ORG"),
            (36, 45, "ORG"),
            (62, 68, "MONEY")
        ]
    }
]

train_data.extend(extra_data)

# 🔥 Limit dataset for faster training
train_data = train_data[:800]

# Save
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(train_data, f, indent=2)

print("Conversion complete!")
print("Total samples:", len(train_data))
