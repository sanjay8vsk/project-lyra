from fastapi import APIRouter, UploadFile, File # type: ignore
from pypdf import PdfReader # type: ignore
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

DOCUMENT_TEXT = ""

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    global DOCUMENT_TEXT

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Extract PDF text
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    DOCUMENT_TEXT = text

    return {
        "message": "PDF uploaded successfully",
        "text_length": len(DOCUMENT_TEXT)
    }