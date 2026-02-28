"""Complete offline chatbot functionality."""

import re
from typing import Dict, List
from datetime import datetime

class OfflineChatbot:
    """Offline chatbot that works without API calls."""
    
    def __init__(self):
        self.document_content = ""
        self.document_chunks = []
    
    def load_document_content(self, file_path: str) -> str:
        """Load document content for offline processing."""
        try:
            if file_path.endswith('.pdf'):
                import PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                self.document_content = text
                return text
            elif file_path.endswith(('.txt', '.md')):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()
                self.document_content = text
                return text
        except Exception as e:
            return f"Error loading document: {str(e)}"
    
    def extract_keywords(self, text: str, limit: int = 10) -> List[str]:
        """Extract important keywords from text."""
        # Remove common words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'a', 'an', 'it', 'he', 'she', 'they', 'we', 'you', 'i', 'me', 'him', 'her', 'them', 'us'}
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter and count
        word_freq = {}
        for word in words:
            if word not in stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:limit]]
    
    def find_relevant_sentences(self, question: str, text: str, limit: int = 3) -> List[str]:
        """Find sentences most relevant to the question."""
        if not text:
            return []
        
        question_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', question.lower()))
        sentences = re.split(r'[.!?]+', text)
        
        sentence_scores = []
        for sentence in sentences:
            if len(sentence.strip()) < 20:  # Skip very short sentences
                continue
            
            sentence_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', sentence.lower()))
            overlap = len(question_words.intersection(sentence_words))
            
            if overlap > 0:
                sentence_scores.append((sentence.strip(), overlap))
        
        # Sort by relevance score
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        return [sentence for sentence, score in sentence_scores[:limit]]
    
    def generate_offline_response(self, question: str) -> Dict[str, any]:
        """Generate response without API."""
        question_lower = question.lower()
        
        if not self.document_content:
            return {
                "answer": "📄 **Document Not Loaded**\n\nPlease upload a document first to get answers.",
                "sources": [],
                "confidence": "low"
            }
        
        # Extract relevant content
        relevant_sentences = self.find_relevant_sentences(question, self.document_content)
        keywords = self.extract_keywords(self.document_content)
        
        # Generate response based on question type
        if any(word in question_lower for word in ['summarize', 'summary', 'what is', 'about']):
            response = f"📋 **Document Summary**\n\n"
            if relevant_sentences:
                response += f"Key information: {relevant_sentences[0][:200]}...\n\n"
            response += f"**Main topics:** {', '.join(keywords[:5])}\n\n"
            response += "*This is a basic analysis. Full AI features require API access.*"
            
        elif any(word in question_lower for word in ['main', 'key', 'important', 'topics']):
            response = f"🔑 **Key Topics**\n\n"
            response += f"**Important terms:** {', '.join(keywords[:8])}\n\n"
            if relevant_sentences:
                response += f"**Relevant content:** {relevant_sentences[0][:150]}...\n\n"
            response += "*Basic keyword extraction. Upgrade for detailed analysis.*"
            
        elif any(word in question_lower for word in ['how', 'why', 'when', 'where', 'who']):
            response = f"❓ **Question Analysis**\n\n"
            if relevant_sentences:
                response += f"**Found relevant information:**\n"
                for i, sentence in enumerate(relevant_sentences[:2], 1):
                    response += f"{i}. {sentence[:100]}...\n\n"
            else:
                response += "No directly relevant information found in the document.\n\n"
            response += "*Limited search capability. Full AI analysis requires API.*"
            
        elif 'list' in question_lower:
            response = f"📝 **List Information**\n\n"
            if relevant_sentences:
                response += "**Found items:**\n"
                for i, sentence in enumerate(relevant_sentences[:3], 1):
                    response += f"• {sentence[:80]}...\n"
                response += "\n"
            response += f"**Related terms:** {', '.join(keywords[:6])}\n\n"
            response += "*Basic list extraction. AI can provide better formatting.*"
            
        else:
            response = f"🔍 **Search Results**\n\n"
            if relevant_sentences:
                response += f"**Most relevant content:**\n{relevant_sentences[0][:200]}...\n\n"
                if len(relevant_sentences) > 1:
                    response += f"**Additional info:**\n{relevant_sentences[1][:150]}...\n\n"
            else:
                response += "No specific matches found. Try different keywords.\n\n"
            response += f"**Related terms:** {', '.join(keywords[:5])}"
        
        return {
            "answer": response,
            "sources": ["1"] if relevant_sentences else [],
            "confidence": "medium" if relevant_sentences else "low"
        }