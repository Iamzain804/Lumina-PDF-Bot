"""Helper functions for PDF chatbot application."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Tuple

def create_directories(paths: list) -> None:
    """Create directories if they don't exist.
    
    Args:
        paths: List of directory paths to create
    """
    try:
        for path in paths:
            Path(path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise OSError(f"Failed to create directories: {e}")

def get_file_size(file_path: str) -> str:
    """Return human-readable file size.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Human-readable file size (e.g., "2.5 MB")
    """
    try:
        size_bytes = os.path.getsize(file_path)
        
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
    except Exception as e:
        return "Unknown size"

def validate_pdf(file) -> Tuple[bool, str]:
    """Validate uploaded PDF file.
    
    Args:
        file: Uploaded file object
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file type
        if not file.name.lower().endswith('.pdf'):
            return False, "File must be a PDF"
        
        # Check file size (50MB limit)
        if file.size > 50 * 1024 * 1024:
            return False, "File size must be less than 50MB"
        
        # Check if file is empty
        if file.size == 0:
            return False, "File is empty"
        
        return True, "Valid PDF file"
    
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def sanitize_filename(filename: str) -> str:
    """Remove special characters and make filename safe.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for storage
    """
    try:
        # Remove file extension
        name, ext = os.path.splitext(filename)
        
        # Remove special characters, keep only alphanumeric, spaces, hyphens, underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-_]', '', name)
        
        # Replace multiple spaces with single space
        sanitized = re.sub(r'\s+', ' ', sanitized).strip()
        
        # Replace spaces with underscores
        sanitized = sanitized.replace(' ', '_')
        
        # Limit length to 100 characters
        sanitized = sanitized[:100]
        
        return f"{sanitized}{ext}"
    
    except Exception as e:
        return f"file_{get_timestamp()}.pdf"

def get_timestamp() -> str:
    """Return formatted timestamp.
    
    Returns:
        Timestamp in format "YYYY-MM-DD_HH-MM-SS"
    """
    try:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    except Exception as e:
        return "unknown_time"

def calculate_reading_time(text: str) -> int:
    """Estimate reading time in minutes.
    
    Args:
        text: Text content to analyze
        
    Returns:
        Estimated reading time in minutes (250 words/min)
    """
    try:
        # Count words (split by whitespace)
        word_count = len(text.split())
        
        # Calculate reading time (250 words per minute)
        reading_time = max(1, round(word_count / 250))
        
        return reading_time
    
    except Exception as e:
        return 1