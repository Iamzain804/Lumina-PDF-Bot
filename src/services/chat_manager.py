"""Chat history management for PDF conversations."""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from threading import Lock

class ChatManager:
    """Manage chat conversations for PDF documents."""
    
    def __init__(self, storage_path: str = "data/chat_history.json"):
        """Initialize chat storage and load existing history.
        
        Args:
            storage_path: Path to JSON storage file
        """
        self.storage_path = Path(storage_path)
        self.lock = Lock()
        self.history = {}
        
        # Create directory if it doesn't exist
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing history
        self._load_history()
    
    def add_message(self, pdf_name: str, role: str, content: str, metadata: Dict = None) -> None:
        """Add message to chat history.
        
        Args:
            pdf_name: Name of PDF document
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata dict
        """
        try:
            with self.lock:
                timestamp = datetime.now().isoformat()
                
                # Initialize PDF history if not exists
                if pdf_name not in self.history:
                    self.history[pdf_name] = {
                        "messages": [],
                        "created_at": timestamp,
                        "updated_at": timestamp
                    }
                
                # Add message
                message = {
                    "role": role,
                    "content": content,
                    "timestamp": timestamp,
                    "metadata": metadata or {}
                }
                
                self.history[pdf_name]["messages"].append(message)
                self.history[pdf_name]["updated_at"] = timestamp
                
                # Save to disk
                self._save()
        
        except Exception as e:
            raise RuntimeError(f"Failed to add message: {e}")
    
    def get_chat_history(self, pdf_name: str, limit: int = 10) -> List[Dict]:
        """Retrieve chat history for a PDF.
        
        Args:
            pdf_name: Name of PDF document
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        try:
            if pdf_name not in self.history:
                return []
            
            messages = self.history[pdf_name]["messages"]
            return messages[-limit:] if limit > 0 else messages
        
        except Exception as e:
            return []
    
    def get_all_pdfs(self) -> List[str]:
        """Get list of all PDFs with chat history.
        
        Returns:
            List of PDF names
        """
        return list(self.history.keys())
    
    def clear_history(self, pdf_name: Optional[str] = None) -> None:
        """Clear chat history.
        
        Args:
            pdf_name: PDF to clear (None for all)
        """
        try:
            with self.lock:
                # Create backup before clearing
                self._create_backup()
                
                if pdf_name is None:
                    self.history = {}
                elif pdf_name in self.history:
                    del self.history[pdf_name]
                
                self._save()
        
        except Exception as e:
            raise RuntimeError(f"Failed to clear history: {e}")
    
    def export_chat(self, pdf_name: str, format: str = "json") -> str:
        """Export chat history to string format.
        
        Args:
            pdf_name: Name of PDF document
            format: Export format ('json' or 'csv')
            
        Returns:
            Formatted chat history string
        """
        try:
            if pdf_name not in self.history:
                return "No chat history found"
            
            chat_data = self.history[pdf_name]
            
            if format.lower() == "json":
                return json.dumps(chat_data, indent=2)
            
            elif format.lower() == "csv":
                lines = ["Role,Content,Timestamp"]
                for msg in chat_data["messages"]:
                    content = msg["content"].replace('"', '""')
                    lines.append(f'"{msg["role"]}","{content}","{msg["timestamp"]}"')
                return "\n".join(lines)
            
            else:
                raise ValueError(f"Unsupported format: {format}")
        
        except Exception as e:
            return f"Export error: {str(e)}"
    
    def get_statistics(self, pdf_name: str) -> Dict[str, any]:
        """Get chat statistics for a PDF.
        
        Args:
            pdf_name: Name of PDF document
            
        Returns:
            Statistics dictionary
        """
        try:
            if pdf_name not in self.history:
                return {
                    "total_messages": 0,
                    "first_chat": None,
                    "last_chat": None
                }
            
            chat_data = self.history[pdf_name]
            messages = chat_data["messages"]
            
            return {
                "total_messages": len(messages),
                "first_chat": chat_data["created_at"],
                "last_chat": chat_data["updated_at"]
            }
        
        except Exception as e:
            return {
                "total_messages": 0,
                "first_chat": None,
                "last_chat": None
            }
    
    def _load_history(self) -> None:
        """Load chat history from disk."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = {}
        
        except (json.JSONDecodeError, Exception):
            # Handle corrupted files
            self.history = {}
            if self.storage_path.exists():
                # Backup corrupted file
                backup_path = self.storage_path.with_suffix('.corrupted')
                shutil.copy2(self.storage_path, backup_path)
    
    def _save(self) -> None:
        """Save chat history to disk with atomic write."""
        try:
            # Write to temporary file first
            temp_path = self.storage_path.with_suffix('.tmp')
            
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
            
            # Atomic move
            temp_path.replace(self.storage_path)
        
        except Exception as e:
            # Clean up temp file if it exists
            if temp_path.exists():
                temp_path.unlink()
            raise RuntimeError(f"Failed to save chat history: {e}")
    
    def _create_backup(self) -> None:
        """Create backup of current history."""
        try:
            if self.storage_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = self.storage_path.with_suffix(f'.backup_{timestamp}')
                shutil.copy2(self.storage_path, backup_path)
        
        except Exception:
            pass  # Backup failure shouldn't stop the operation