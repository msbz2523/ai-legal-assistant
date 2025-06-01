from transformers import pipeline
import torch

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
    Nutzt stabiles Übersetzungsmodell, keine LLM-Fantasie.
    """
    translation = translator(text, max_length=600)[0]["translation_text"]
    return translation