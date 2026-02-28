"""Configuration settings for PDF chatbot RAG system."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for PDF chatbot application."""
    
    # API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # LLM Provider ("groq", "openai", or "openrouter")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
    
    # Model Configuration (Standard model IDs)
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # Recommendation: Use OpenRouter free models if testing
    # Or 'llama-3.1-8b-instant' for Groq
    LLM_MODEL = os.getenv("LLM_MODEL", "meta-llama/llama-3.1-8b-instruct:free")
    
    # RAG Configuration
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    TOP_K_RESULTS = 4
    
    # LLM Parameters
    TEMPERATURE = 0.3
    MAX_TOKENS = 512
    
    # Directory Paths
    PDF_UPLOAD_DIR = "data/pdfs"
    VECTOR_STORE_DIR = "data/vectorstore"
    
    @classmethod
    def validate_config(cls):
        """Validate configuration and create directories."""
        if cls.LLM_PROVIDER == "groq" and not cls.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        elif cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        elif cls.LLM_PROVIDER == "openrouter" and not cls.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
        # Create directories
        Path(cls.PDF_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(cls.VECTOR_STORE_DIR).mkdir(parents=True, exist_ok=True)

# Initialize configuration
Config.validate_config()