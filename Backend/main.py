from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from services.ocr_service import extract_text
from services.grammar_service import check_grammar
from services.summarize_service import summarize_text
from services.pdf_service import export_pdf

app = FastAPI()

# Izinkan frontend (Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract-text")
async def extract(file: UploadFile = File(...)):
    text = await extract_text(file)
    return {"text": text}

@app.post("/check-grammar")
async def grammar(text: str = Form(...)):
    return {"corrected": check_grammar(text)}

@app.post("/summarize")
async def summarize(text: str = Form(...)):
    return {"summary": summarize_text(text)}

@app.post("/export-pdf")
async def export(text: str = Form(...)):
    file_path = export_pdf(text)
    return {"pdf_path": file_path}
