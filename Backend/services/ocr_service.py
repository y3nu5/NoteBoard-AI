from paddleocr import PaddleOCR
import tempfile

ocr = PaddleOCR(use_angle_cls=True, lang='en')

async def extract_text(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        content = await file.read()  # wajib pakai await karena UploadFile.read() adalah async
        tmp.write(content)
        tmp_path = tmp.name

    result = ocr.ocr(tmp_path)
    
    text_blocks = []
    for page in result:
        for line in page:
            text_blocks.append(line[1][0])
    
    return " ".join(text_blocks).strip() or "No text detected."
