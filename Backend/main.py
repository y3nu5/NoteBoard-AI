# main.py
import os
import asyncio
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List

# --- Import services ---
from services.surya_ocr import ocr_surya
from services.grammar_service import check_grammar
from services.summarize_service import summarize_text
from services.pdf_service import export_pdf

app = FastAPI(title="NoteBoard AI Backend")

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in ALLOWED_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# OCR Endpoint
# ---------------------------------------------------------
@app.post("/ocr")
async def ocr_endpoint(files: List[UploadFile] = File(...)):
    """
    Menerima beberapa file dan mengembalikan hasil OCR (list).
    """
    results = []

    for file in files:
        content = await file.read()
        text = await ocr_surya(content)  # Surya OCR async
        results.append(text)

    return {"results": results}


# ---------------------------------------------------------
# Grammar Check Endpoint - DIPERBAIKI
# ---------------------------------------------------------
@app.post("/grammar")
async def grammar_endpoint(text: str = Form(...)):
    """
    Menerima text dari FormData dan mengembalikan hasil grammar check.
    """
    # Jalankan di thread pool karena check_grammar adalah fungsi sinkron
    result = await asyncio.to_thread(check_grammar, text)
    return result


# ---------------------------------------------------------
# Summarization Endpoint
# ---------------------------------------------------------
@app.post("/summarize")
async def summarize_endpoint(text: str = Form(...)):
    """
    Meringkas teks menggunakan AI.
    """
    summary = await summarize_text(text)
    return {"summary": summary}


# ---------------------------------------------------------
# Export PDF Endpoint
# ---------------------------------------------------------
@app.post("/export-pdf")
async def export_pdf_endpoint(text: str = Form(...)):
    """
    Generate PDF lalu mengirim kembali file. Karena sinkron,
    dijalankan di thread terpisah.
    """
    pdf_path = await asyncio.to_thread(export_pdf, text, "output.pdf")

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="output.pdf"
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "NoteBoard AI Backend is running!", "status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
