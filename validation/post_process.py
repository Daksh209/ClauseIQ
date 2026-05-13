import json
from validation.validate_entities import validate_entities
from validation.normalize_entities import normalize_entities


def build_json_output(normalized_entities: list, source_file: str = "") -> dict:
    output = {
        "source_file": source_file,
        "parties": [],
        "effective_date": None,
        "payment_amount": None,
        "all_entities": normalized_entities,
        "confidence": "high" if len(normalized_entities) >= 3 else "low"
    }

    for ent in normalized_entities:
        label = ent["label"]
        value = ent["normalized"]

        if label == "ORG" and value not in output["parties"]:
            output["parties"].append(value)

        elif label == "DATE" and output["effective_date"] is None:
            output["effective_date"] = value

        elif label == "MONEY" and output["payment_amount"] is None:
            output["payment_amount"] = value

    return output


def post_process(raw_entities: list, source_file: str = "") -> dict:
    """
    Main function — Flask API இந்த function மட்டும் call பண்ணும்.

    raw_entities format:
        [(char_start, char_end, label, text), ...]

    Example:
        raw = [
            (22, 36, "DATE",  "10 April 2025"),
            (45, 54, "ORG",   "Delta Ltd"),
            (59, 65, "MONEY", "$12000"),
        ]
        result = post_process(raw, source_file="contract.pdf")
    """
    validation_result = validate_entities(raw_entities)
    valid = validation_result["valid"]
    invalid = validation_result["invalid"]

    normalized = normalize_entities(valid)

    output = build_json_output(normalized, source_file)

    output["invalid_entities"] = [
        {"entity": str(e[0]), "reason": e[1]} for e in invalid
    ]

    return output


if __name__ == "__main__":
    sample_entities = [
        (22, 36,  "DATE",  "10 April 2025"),
        (45, 54,  "ORG",   "Delta Ltd"),
        (59, 65,  "MONEY", "$12000"),
        (90, 99,  "ORG",   "Omega Corp"),
        (110, 115, "DATE", "not-a-date"),
        (120, 125, "MONEY", "abc"),
    ]

    result = post_process(sample_entities, source_file="sample_contract.pdf")
    print(json.dumps(result, indent=2))
