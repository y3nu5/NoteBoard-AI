# services/surya_ocr.py
from PIL import Image
from io import BytesIO
import asyncio

from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

# Load model sekali saja (global)
foundation = FoundationPredictor()
recognizer = RecognitionPredictor(foundation)
detector = DetectionPredictor()


def _run_surya_sync(img):
    """
    Fungsi sync (berat) yang menjalankan Surya OCR.
    Dibungkus dalam to_thread saat dipanggil oleh async.
    """
    result = recognizer([img], det_predictor=detector)

    # Jika result adalah list, ambil index 0
    if isinstance(result, list):
        result = result[0]

    lines = []
    for line in result.text_lines:
        lines.append(line.text)

    return "\n".join(lines)



async def ocr_surya(image_bytes: bytes) -> str:
    """
    Wrapper async untuk OCR.
    Model Surya dipanggil di threadpool supaya tidak blocking.
    """
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        result = await asyncio.to_thread(_run_surya_sync, img)

        cleaned = " ".join(result.split())
        return cleaned
    
    except Exception as e:
        print("Surya OCR Error:", e)
        return ""
