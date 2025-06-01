# validation_service.py

def validate_output(text: str) -> bool:
    """
    Validiert den juristischen Text auf unzulässige Aussagen.
    Gibt False zurück, wenn riskante Formulierungen enthalten sind.
    """
    banned_phrases = [
        "garantiert",
        "zweifelsfrei",
        "sicherlich",
        "muss unbedingt",
        "zweifellos",
        "wird auf jeden Fall"
    ]
    return not any(banned.lower() in text.lower() for banned in banned_phrases)