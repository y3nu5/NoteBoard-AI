import asyncio
from PIL import Image
from io import BytesIO

from surya.foundation import FoundationPredictor
from surya.recognition import RecognitionPredictor
from surya.detection import DetectionPredictor

foundation = None
recognizer = None
detector = None


def load_surya():
    global foundation, recognizer, detector
    if foundation is None:
        foundation = FoundationPredictor()
        recognizer = RecognitionPredictor(foundation)
        detector = DetectionPredictor()


def _run_ocr_sync(img):
    load_surya()
    result = recognizer([img], det_predictor=detector)
    result = result[0] if isinstance(result, list) else result
    return "\n".join([l.text for l in result.text_lines])


async def ocr_surya(image_bytes: bytes) -> str:
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        text = await asyncio.to_thread(_run_ocr_sync, img)
        return " ".join(text.split())
    except Exception as e:
        print("OCR Error:", e)
        return ""
