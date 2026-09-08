"""Small, transparent KAP disclosure sentiment filter.

This is intentionally rule-based. It is a filter, not an attempt to predict
price from a disclosure title alone. Unknown disclosures remain neutral.
"""

POSITIVE = (
    "yeni sözleşme", "yeni sipariş", "ihale", "temettü", "geri alım",
    "kapasite artışı", "yatırım teşvik", "stratejik işbirliği",
    "iş ilişkisi", "pozitif", "kar artışı", "net kar artışı",
)

NEGATIVE = (
    "bedelli sermaye", "sermaye azaltımı", "iflas", "konkordato",
    "temerrüt", "ceza", "dava", "borç yapılandırma",
    "net zarar", "zarar artışı", "olumsuz", "faaliyet durdurma",
)


def classify(text: str) -> int:
    """Return +1 positive, -1 negative, 0 neutral/unknown."""
    normalized = " ".join(text.lower().split())
    positive_hits = sum(term in normalized for term in POSITIVE)
    negative_hits = sum(term in normalized for term in NEGATIVE)

    if positive_hits > negative_hits:
        return 1
    if negative_hits > positive_hits:
        return -1
    return 0
