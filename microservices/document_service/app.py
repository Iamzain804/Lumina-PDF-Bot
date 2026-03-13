"""📄 Document Service - PDF/DOCX Processing Microservice"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from pathlib import Path
import shutil
from typing import Dict
from datetime import datetime

app = FastAPI(title="Document Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("data/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict:
    """Upload and process document"""
    try:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        # Extract text based on file type
        text = extract_text(file_path)
        page_count = get_page_count(file_path)
        
        return {
            "status": "success",
            "filename": file.filename,
            "text": text,
            "page_count": page_count,
            "file_size": file_path.stat().st_size,
            "upload_date": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_text(file_path: Path) -> str:
    """Extract text from document"""
    ext = file_path.suffix.lower()
    
    if ext == '.pdf':
        text = ""
        with open(file_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    
    elif ext in ['.txt', '.md']:
        return file_path.read_text(encoding='utf-8')
    
    elif ext == '.docx':
        from docx import Document
        doc = Document(file_path)
        return "\n".join([p.text for p in doc.paragraphs])
    
    return ""

def get_page_count(file_path: Path) -> int:
    """Get page count"""
    ext = file_path.suffix.lower()
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            return len(PyPDF2.PdfReader(f).pages)
    return 1

@app.get("/documents")
async def list_documents():
    """List all uploaded documents"""
    docs = []
    for file in UPLOAD_DIR.glob("*"):
        if file.is_file():
            docs.append({
                "filename": file.name,
                "size": file.stat().st_size,
                "modified": datetime.fromtimestamp(file.stat().st_mtime).isoformat()
            })
    return {"documents": docs}

@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete document"""
    file_path = UPLOAD_DIR / filename
    if file_path.exists():
        file_path.unlink()
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    print("Starting Document Service on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
