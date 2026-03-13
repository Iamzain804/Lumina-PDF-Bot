"""Shared configuration for all microservices"""
import os
from dotenv import load_dotenv

load_dotenv()

class SharedConfig:
    # Service URLs
    DOCUMENT_SERVICE_URL = os.getenv("DOCUMENT_SERVICE_URL", "http://localhost:8001")
    VECTOR_SERVICE_URL = os.getenv("VECTOR_SERVICE_URL", "http://localhost:8002")
    LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8003")
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    LLM_MODEL = os.getenv("LLM_MODEL", "google/gemini-2.0-flash-lite-preview-02-05:free")
    
    # RAG Settings
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 4
    TEMPERATURE = 0.3
    MAX_TOKENS = 512
