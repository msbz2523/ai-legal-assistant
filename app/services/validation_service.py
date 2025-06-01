# validation_service.py

import re

BANNED_PHRASES = [
    "garantiert",
    "zweifelsfrei",
    "sicherlich",
    "muss unbedingt",
    "zweifellos",
    "wird auf jeden Fall"
]

# Ergänze juristische Begriffe, die nicht ohne Kontext vorkommen dürfen
CONTEXTUAL_FLAGS = [
    r"(?<!nicht )rechtsverbindlich",
    r"entspricht.*?§\s*\d+",
    r"ist.*?verpflichtet"
]

def validate_output(text: str) -> bool:
    """
    Validiert den juristischen Text auf riskante Aussagen oder Formulierungen.
    Gibt False zurück, wenn riskante Phrasen oder unreflektierte Rechtsansprüche enthalten sind.
    """
    text_lower = text.lower()
    for phrase in BANNED_PHRASES:
        if phrase in text_lower:
            return False

    for regex in CONTEXTUAL_FLAGS:
        if re.search(regex, text_lower):
            return False

    return True