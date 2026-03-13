"""🤖 LLM Service - AI Response Generation Microservice"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LLM Service", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    context: str
    temperature: float = 0.3
    max_tokens: int = 512

class SummaryRequest(BaseModel):
    text: str
    max_length: int = 200

def get_llm_client():
    """Get LLM client based on provider"""
    provider = os.getenv("LLM_PROVIDER", "groq")
    print(f"Initializing LLM client for provider: {provider}")
    
    try:
        if provider == "groq":
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                print("ERROR: GROQ_API_KEY not found in environment")
                return None
            print(f"GROQ_API_KEY found: {api_key[:10]}...")
            from groq import Groq
            return Groq(api_key=api_key)
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("ERROR: OPENAI_API_KEY not found in environment")
                return None
            from openai import OpenAI
            return OpenAI(api_key=api_key)
        elif provider == "openrouter":
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                print("ERROR: OPENROUTER_API_KEY not found in environment")
                return None
            from openai import OpenAI
            return OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            print(f"ERROR: Unknown provider: {provider}")
            return None
    except Exception as e:
        print(f"ERROR initializing LLM client: {e}")
        return None

@app.post("/generate")
async def generate_answer(request: QueryRequest) -> Dict:
    """Generate answer using LLM"""
    try:
        client = get_llm_client()
        if not client:
            print("ERROR: LLM client is None")
            return {
                "answer": "❌ LLM client not configured. Please check API keys in .env file.",
                "sources": [],
                "confidence": "low"
            }
        
        model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        print(f"Using model: {model}")
        print(f"Provider: {os.getenv('LLM_PROVIDER', 'groq')}")
        
        prompt = f"""Based on the following context, answer the question accurately.

Context:
{request.context}

Question: {request.question}

Answer:"""
        
        print("Calling LLM API...")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        answer = response.choices[0].message.content
        print("LLM response received successfully")
        
        # Extract sources (page numbers)
        sources = extract_sources(request.context)
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": "high" if len(request.context) > 500 else "medium"
        }
    except Exception as e:
        print(f"ERROR in generate_answer: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return error in proper format instead of raising exception
        return {
            "answer": f"❌ Error generating answer: {str(e)}\n\nPlease check:\n1. API key is correct in .env\n2. Internet connection\n3. API service is available",
            "sources": [],
            "confidence": "low"
        }

@app.post("/summarize")
async def summarize_text(request: SummaryRequest) -> Dict:
    """Summarize document text"""
    try:
        client = get_llm_client()
        if not client:
            return {"summary": "LLM client not configured. Please check API keys."}
        
        model = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
        
        # Truncate text if too long
        text = request.text[:4000]
        
        prompt = f"""Summarize the following document in {request.max_length} words or less:

{text}

Summary:"""
        
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=300
        )
        
        summary = response.choices[0].message.content
        
        return {"summary": summary}
    except Exception as e:
        return {"summary": f"Error generating summary: {str(e)}"}

def extract_sources(context: str) -> List[int]:
    """Extract page numbers from context"""
    import re
    pages = re.findall(r'Page (\d+)', context)
    return [int(p) for p in pages[:5]]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "LLM Service"}

if __name__ == "__main__":
    import uvicorn
    print("Starting LLM Service on http://127.0.0.1:8003")
    uvicorn.run(app, host="127.0.0.1", port=8003)
