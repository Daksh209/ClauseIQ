import re
from datetime import datetime


def normalize_entities(valid_entities: list) -> list:
    normalized = []

    for ent in valid_entities:
        start, end, label, text = ent
        text = text.strip()

        if label == "DATE":
            norm = normalize_date(text)
        elif label == "ORG":
            norm = normalize_org(text)
        elif label == "MONEY":
            norm = normalize_money(text)
        else:
            norm = text

        normalized.append({
            "label": label,
            "raw": text,
            "normalized": norm,
            "char_start": start,
            "char_end": end,
        })

    return normalized


def normalize_date(text: str) -> str:

    # remove st/nd/rd/th
    cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text)

    cleaned = cleaned.replace("day of", "").strip()

    formats = [
        "%d %B %Y",
        "%B %d, %Y",
        "%B %d %Y",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(
                cleaned,
                fmt
            ).strftime("%Y-%m-%d")

        except ValueError:
            continue

    return text


def normalize_org(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def normalize_money(text: str):
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    try:
        return float(cleaned)
    except ValueError:
        return text
