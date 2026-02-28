"""Main RAG pipeline orchestrator for PDF chatbot."""

import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.utils.utils import sanitize_filename, get_file_size

class RAGEngine:
    """Main RAG pipeline orchestrator - the brain of the application."""
    
    def __init__(self, config, llm_handler, vector_store, chat_manager):
        """Initialize RAG engine with all components.
        
        Args:
            config: Configuration object
            llm_handler: LLM handler instance
            vector_store: Vector store instance
            chat_manager: Chat manager instance
        """
        self.config = config
        self.llm_handler = llm_handler
        self.vector_store = vector_store
        self.chat_manager = chat_manager
        
        # Ensure directories exist
        Path(config.PDF_UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(config.VECTOR_STORE_DIR).mkdir(parents=True, exist_ok=True)
    
    def process_document(self, file, filename: str) -> Dict[str, any]:
        """Complete document processing pipeline.
        
        Args:
            file: Uploaded file object
            filename: Original filename
            
        Returns:
            Dict with status, summary, page_count
        """
        doc_path = None
        try:
            # Sanitize filename
            safe_filename = sanitize_filename(filename)
            doc_name = Path(safe_filename).stem
            doc_path = Path(self.config.PDF_UPLOAD_DIR) / safe_filename
            
            # Save uploaded file
            with open(doc_path, 'wb') as f:
                f.write(file.read())
            
            # Extract text from document
            text = self.vector_store.load_document(str(doc_path))
            
            # Count pages/sections
            page_count = self._get_document_pages(doc_path)
            
            # Split text into chunks
            chunks = self.vector_store.split_text(text)
            
            # Create embeddings and vectorstore
            vectorstore = self.vector_store.create_embeddings(chunks)
            
            # Save vectorstore
            self.vector_store.save_vectorstore(vectorstore, doc_name)
            
            # Generate initial summary
            summary = self.llm_handler.summarize_pdf(text)
            
            return {
                "status": "success",
                "summary": summary,
                "page_count": page_count,
                "pdf_name": doc_name,
                "chunks_created": len(chunks)
            }
        
        except Exception as e:
            # Cleanup on failure
            if doc_path and doc_path.exists():
                doc_path.unlink()
            
            return {
                "status": "error",
                "error": str(e),
                "summary": None,
                "page_count": 0
            }
    
    def _get_document_pages(self, doc_path: Path) -> int:
        """Get page/section count for different document types."""
        try:
            file_extension = doc_path.suffix.lower()
            
            if file_extension == '.pdf':
                import PyPDF2
                with open(doc_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    return len(pdf_reader.pages)
            elif file_extension in ['.txt', '.md']:
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Estimate sections by line breaks
                    return max(1, content.count('\n\n') + 1)
            elif file_extension == '.docx':
                try:
                    from docx import Document
                    doc = Document(doc_path)
                    return max(1, len(doc.paragraphs) // 10)  # Rough estimate
                except:
                    return 1
            else:
                return 1
        except:
            return 1
    
    def query(self, pdf_name: str, question: str) -> Dict[str, any]:
        """Main query pipeline for PDF questions.
        
        Args:
            pdf_name: Name of PDF document
            question: User question
            
        Returns:
            Dict with answer, sources, context_used
        """
        try:
            # Validate vectorstore exists
            if not self._validate_vectorstore(pdf_name):
                return {
                    "answer": "PDF not found or not processed yet.",
                    "sources": [],
                    "context_used": "",
                    "confidence": "low"
                }
            
            # Load vectorstore
            vectorstore = self.vector_store.load_vectorstore(pdf_name)
            if not vectorstore:
                return {
                    "answer": "Failed to load PDF data.",
                    "sources": [],
                    "context_used": "",
                    "confidence": "low"
                }
            
            # Retrieve relevant chunks
            search_results = self.vector_store.search(
                question, vectorstore, self.config.TOP_K_RESULTS
            )
            
            # Prepare context from chunks
            context = self._prepare_context(search_results)
            
            # Generate answer using LLM
            response = self.llm_handler.generate_answer(question, context)
            
            # Save to chat history
            self.chat_manager.add_message(pdf_name, "user", question)
            self.chat_manager.add_message(
                pdf_name, "assistant", response["answer"],
                {"sources": response["sources"], "confidence": response["confidence"]}
            )
            
            return {
                "answer": response["answer"],
                "sources": response["sources"],
                "context_used": context,
                "confidence": response["confidence"]
            }
        
        except Exception as e:
            return {
                "answer": f"Error processing question: {str(e)}",
                "sources": [],
                "context_used": "",
                "confidence": "low"
            }
    
    def get_document_summary(self, doc_name: str) -> str:
        """Get or generate document summary.
        
        Args:
            doc_name: Name of document
            
        Returns:
            Document summary string
        """
        try:
            # Find document file
            doc_files = list(Path(self.config.PDF_UPLOAD_DIR).glob(f"{doc_name}.*"))
            if not doc_files:
                return "Document file not found"
            
            doc_path = doc_files[0]
            
            # Load and summarize
            text = self.vector_store.load_document(str(doc_path))
            summary = self.llm_handler.summarize_pdf(text)
            
            return summary
        
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def delete_pdf(self, pdf_name: str) -> bool:
        """Delete PDF and all associated data.
        
        Args:
            pdf_name: Name of PDF document
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Remove PDF file
            pdf_files = list(Path(self.config.PDF_UPLOAD_DIR).glob(f"{pdf_name}.*"))
            for pdf_file in pdf_files:
                pdf_file.unlink()
            
            # Delete vectorstore
            vectorstore_path = Path(self.config.VECTOR_STORE_DIR) / pdf_name
            if vectorstore_path.exists():
                shutil.rmtree(vectorstore_path)
            
            # Clear chat history
            self.chat_manager.clear_history(pdf_name)
            
            return True
        
        except Exception as e:
            return False
    
    def list_available_documents(self) -> List[Dict[str, any]]:
        """List all processed documents with metadata.
        
        Returns:
            List of document metadata dictionaries
        """
        try:
            docs = []
            doc_dir = Path(self.config.PDF_UPLOAD_DIR)
            
            # Support multiple file extensions
            extensions = ['*.pdf', '*.txt', '*.md', '*.docx']
            
            for pattern in extensions:
                for doc_file in doc_dir.glob(pattern):
                    try:
                        doc_name = doc_file.stem
                        
                        # Get file stats
                        stat = doc_file.stat()
                        upload_date = datetime.fromtimestamp(stat.st_mtime).isoformat()
                        file_size = get_file_size(str(doc_file))
                        
                        # Get page count
                        page_count = self._get_document_pages(doc_file)
                        
                        # Get summary preview
                        try:
                            summary = self.get_document_summary(doc_name)
                            summary_preview = summary[:100] + "..." if len(summary) > 100 else summary
                        except:
                            summary_preview = "Summary not available"
                        
                        docs.append({
                            "filename": doc_file.name,
                            "pdf_name": doc_name,
                            "upload_date": upload_date,
                            "file_size": file_size,
                            "page_count": page_count,
                            "summary": summary_preview,
                            "has_vectorstore": self._validate_vectorstore(doc_name),
                            "file_type": doc_file.suffix.upper()[1:]
                        })
                    
                    except Exception:
                        continue
            
            return sorted(docs, key=lambda x: x["upload_date"], reverse=True)
        
        except Exception as e:
            return []
    
    def _prepare_context(self, search_results: List[tuple]) -> str:
        """Format search results into context string.
        
        Args:
            search_results: List of (document, score) tuples
            
        Returns:
            Formatted context string
        """
        try:
            if not search_results:
                return "No relevant context found."
            
            context_parts = []
            for i, (doc, score) in enumerate(search_results, 1):
                content = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                context_parts.append(f"Context {i}:\n{content}")
            
            return "\n\n---\n\n".join(context_parts)
        
        except Exception as e:
            return "Error preparing context"
    
    def _validate_vectorstore(self, pdf_name: str) -> bool:
        """Check if vectorstore exists and is valid.
        
        Args:
            pdf_name: Name of PDF document
            
        Returns:
            True if vectorstore exists and is valid
        """
        try:
            vectorstore_path = Path(self.config.VECTOR_STORE_DIR) / pdf_name
            return vectorstore_path.exists() and any(vectorstore_path.iterdir())
        
        except Exception:
            return False