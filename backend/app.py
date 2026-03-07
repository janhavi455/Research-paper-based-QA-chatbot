from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from typing import List

UPLOAD_FOLDER = Path(__file__).parent / "data" / "uploaded_pdf"

app = FastAPI(title="PDF Metadata API")

# Allow CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.post("/upload_pdfs")
async def upload_pdfs(pdfs: List[UploadFile] = File(...)):
    try:


        saved_files = []
        UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

        for pdf in pdfs:
            safe_filename = Path(pdf.filename).name
            file_path = UPLOAD_FOLDER / safe_filename

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(pdf.file, buffer)

            saved_files.append(safe_filename)

        return {
            "message": "All files uploaded successfully",
            "files": saved_files
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))