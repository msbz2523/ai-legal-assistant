import easyocr
import numpy as np
from PIL import Image
import io

ocr_reader = easyocr.Reader(['en', 'de'], gpu=False)

def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes)).convert('RGB')
    image_array = np.array(image)
    result = ocr_reader.readtext(image_array)
    return " ".join([res[1] for res in result])
