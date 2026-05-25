from fastapi import APIRouter, UploadFile, File  # type: ignore
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import chunk_text
from pathlib import Path
from app.services.embedding_service import store_chunks
import shutil

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

print("UPLOAD DIRECTORY:", UPLOAD_DIR)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        extracted_text = extract_text_from_pdf(file_path)

        chunks = chunk_text(extracted_text)

        store_chunks(chunks)

        return {
            "filename": file.filename,
            "message": "File uploaded successfully",
            "total_chunks": len(chunks),
            "sample_chunk": chunks[0]
        }

    except Exception as e:
        return {
            "error": str(e)
        }