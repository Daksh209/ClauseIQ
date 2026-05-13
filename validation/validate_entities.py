import re

def validate_entities(entities: list) -> dict:
    valid = []
    invalid = []

    for ent in entities:
        start, end, label, text = ent
        text = text.strip()

        if label == "DATE":
            if is_valid_date(text):
                valid.append(ent)
            else:
                invalid.append((ent, "Invalid date format"))

        elif label == "ORG":
            if is_valid_org(text):
                valid.append(ent)
            else:
                invalid.append((ent, "ORG is empty or too short"))

        elif label == "MONEY":
            if is_valid_money(text):
                valid.append(ent)
            else:
                invalid.append((ent, "No number found in MONEY entity"))

        else:
            invalid.append((ent, f"Unknown label: {label}"))

    return {"valid": valid, "invalid": invalid}


def is_valid_date(text: str) -> bool:
    patterns = [
        r"\d{1,2}\s+\w+\s+\d{4}",
        r"\d{1,2}(st|nd|rd|th)?\s+day\s+of\s+\w+\s+\d{4}",
        r"\d{4}-\d{2}-\d{2}",
        r"\w+\s+\d{1,2},?\s+\d{4}",
        r"\d{1,2}/\d{1,2}/\d{4}",
        r"\d{1,2}(st|nd|rd|th)?\s+day\s+of\s+\w+,\s+\d{4}"
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def is_valid_org(text: str) -> bool:

    text = text.strip()

    # too short
    if len(text) < 2:
        return False

    # reject very long sentences
    if len(text) > 80:
        return False

    # reject full sentence-like predictions
    bad_patterns = [
        "shall",
        "agreement",
        "liable",
        "rights",
        "damages",
        "technology",
        "clients"
    ]

    lowered = text.lower()

    if any(word in lowered for word in bad_patterns):
        return False

    return True


def is_valid_money(text: str) -> bool:
    return bool(re.search(r"\d", text))
