from transformers import pipeline
import torch

LEGAL_GLOSSARY_DE_AR = {
    "Schadensersatz": "التعويض القانوني",
    "Verjährung": "تقادم دعوى",
    "notleidende Forderung": "دين متعثر",
    "Mahnung": "إنذار بالدفع",
    "Vertrag": "عقد قانوني",
    "Pflicht": "واجب قانوني",
    "Haftung": "مسؤولية قانونية",
    "Klage": "دعوى قضائية"
}

translator = pipeline(
    "translation",
    model="Helsinki-NLP/opus-mt-de-ar",
    tokenizer="Helsinki-NLP/opus-mt-de-ar",
    framework="pt",
    device=0 if torch.cuda.is_available() else -1
)

def translate_to_arabic(text: str) -> str:
    """
    Übersetzt deutschen Text professionell ins Arabische.
    Nutzt stabiles Übersetzungsmodell + juristisches Glossar.
    """
    for de_term, ar_term in LEGAL_GLOSSARY_DE_AR.items():
        text = text.replace(de_term, ar_term)

    translation = translator(text, max_length=600)[0]["translation_text"]
    return translation