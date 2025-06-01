import easyocr
import numpy as np
from PIL import Image, ImageFilter
import io

def extract_text_from_image(file_bytes: bytes) -> str:
    """
    Verbessertes OCR-Modul mit Bildoptimierung und easyocr.
    - Graustufen
    - Hochskalierung
    - Schärfen
    - paragraph=True
    """
    image = Image.open(io.BytesIO(file_bytes)).convert('L')
    image = image.resize((int(image.width * 1.5), int(image.height * 1.5)))
    image = image.filter(ImageFilter.SHARPEN)

    image_array = np.array(image)
    ocr_reader = easyocr.Reader(['de'], gpu=False)
    result = ocr_reader.readtext(image_array, detail=0, paragraph=True)

    return " ".join(result)