"""🧠 Vector Service - Embeddings & Search Microservice"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import pickle
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Vector Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VECTOR_DIR = Path("data/vectors")
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

class TextChunks(BaseModel):
    doc_id: str
    chunks: List[str]

class SearchQuery(BaseModel):
    doc_id: str
    query: str
    top_k: int = 4

def split_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Split text into chunks"""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

@app.post("/create_embeddings")
async def create_embeddings(data: TextChunks) -> Dict:
    """Create and store embeddings"""
    try:
        chunks = data.chunks
        
        # Limit features for faster processing
        vectorizer = TfidfVectorizer(max_features=300)
        vectors = vectorizer.fit_transform(chunks).toarray()
        
        # Save to disk
        vector_path = VECTOR_DIR / f"{data.doc_id}.pkl"
        with open(vector_path, "wb") as f:
            pickle.dump({
                "vectors": vectors,
                "chunks": chunks,
                "vectorizer": vectorizer
            }, f)
        
        return {
            "status": "success",
            "doc_id": data.doc_id,
            "num_chunks": len(chunks),
            "vector_dim": vectors.shape[1]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_vectors(query: SearchQuery) -> Dict:
    """Search for similar chunks"""
    try:
        vector_path = VECTOR_DIR / f"{query.doc_id}.pkl"
        
        if not vector_path.exists():
            raise HTTPException(status_code=404, detail="Vectors not found")
        
        # Load vectors
        with open(vector_path, "rb") as f:
            data = pickle.load(f)
        
        vectors = data["vectors"]
        chunks = data["chunks"]
        vectorizer = data["vectorizer"]
        
        # Transform query
        query_vector = vectorizer.transform([query.query]).toarray()
        
        # Calculate similarity
        similarities = cosine_similarity(query_vector, vectors)[0]
        top_indices = np.argsort(similarities)[::-1][:query.top_k]
        
        results = [
            {
                "chunk": chunks[idx],
                "score": float(similarities[idx]),
                "index": int(idx)
            }
            for idx in top_indices
        ]
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/split_text")
async def split_document_text(text: str, chunk_size: int = 1000) -> Dict:
    """Split text into chunks"""
    chunks = split_text(text, chunk_size)
    return {"chunks": chunks, "count": len(chunks)}

@app.delete("/vectors/{doc_id}")
async def delete_vectors(doc_id: str):
    """Delete vector store"""
    vector_path = VECTOR_DIR / f"{doc_id}.pkl"
    if vector_path.exists():
        vector_path.unlink()
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Vectors not found")

if __name__ == "__main__":
    import uvicorn
    print("Starting Vector Service on http://127.0.0.1:8002")
    uvicorn.run(app, host="127.0.0.1", port=8002)
