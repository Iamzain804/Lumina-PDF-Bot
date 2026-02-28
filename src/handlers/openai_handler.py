"""OpenAI API integration for LLM responses."""

import re
import time
from typing import Dict, List

from openai import OpenAI

class OpenAILLMHandler:
    """OpenAI API handler for generating responses."""
    
    def __init__(self, config):
        """Initialize OpenAI client with configuration.
        
        Args:
            config: Configuration object with API settings
        """
        try:
            self.client = OpenAI(
                api_key=config.OPENAI_API_KEY
            )
            self.model = config.LLM_MODEL or "gpt-3.5-turbo"
            self.temperature = config.TEMPERATURE
            self.max_tokens = config.MAX_TOKENS
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAILLMHandler: {e}")
    
    def generate_answer(self, query: str, context: str) -> Dict[str, any]:
        """Generate answer using OpenAI API with retry logic.
        
        Args:
            query: User question
            context: Retrieved context from PDF
            
        Returns:
            Dict with answer, sources, and confidence
        """
        for attempt in range(3):
            try:
                prompt = self._create_prompt(query, context)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    timeout=15
                )
                
                if not response.choices or not response.choices[0].message.content:
                    raise ValueError("Empty response from API")
                
                answer_text = response.choices[0].message.content.strip()
                return self._parse_response(answer_text, context)
                
            except Exception as e:
                if attempt == 2:  # Last attempt
                    return {
                        "answer": f"Error generating response: {str(e)}",
                        "sources": [],
                        "confidence": "low"
                    }
                time.sleep(1)  # Wait before retry
    
    def _create_prompt(self, query: str, context: str) -> str:
        """Create optimized prompt for OpenAI API.
        
        Args:
            query: User question
            context: Retrieved context chunks
            
        Returns:
            Complete formatted prompt
        """
        system_prompt = (
            "You are a helpful PDF assistant. Answer based only on the provided context. "
            "Be concise and cite page numbers when available."
        )
        
        formatted_context = "\n---\n".join(context.split("\n\n")) if context else "No context available"
        
        prompt = f"{system_prompt}\n\nContext:\n{formatted_context}\n\nQuestion: {query}\n\nAnswer:"
        
        return prompt
    
    def _parse_response(self, response: str, context: str) -> Dict[str, any]:
        """Parse API response and extract structured information.
        
        Args:
            response: Raw response from API
            context: Original context for confidence estimation
            
        Returns:
            Structured response dict
        """
        try:
            # Clean response from HTML tags
            clean_response = response.replace('<', '').replace('>', '')
            
            # Extract page references - look for various patterns
            page_patterns = [
                r'page\s*(\d+)',
                r'Page\s*(\d+)', 
                r'p\.\s*(\d+)',
                r'P\.\s*(\d+)'
            ]
            
            sources = []
            for pattern in page_patterns:
                matches = re.findall(pattern, clean_response, re.IGNORECASE)
                sources.extend(matches)
            
            # Remove duplicates and sort
            sources = sorted(list(set(sources)))
            
            # If no page references found, try to extract from context
            if not sources and context:
                # Look for page indicators in context
                context_pages = re.findall(r'page\s*(\d+)', context.lower())
                if context_pages:
                    sources = sorted(list(set(context_pages))[:3])  # Max 3 pages
            
            # Estimate confidence based on context overlap
            response_words = set(clean_response.lower().split())
            context_words = set(context.lower().split()) if context else set()
            
            if not context_words:
                confidence = "low"
            else:
                overlap = len(response_words.intersection(context_words))
                overlap_ratio = overlap / len(response_words) if response_words else 0
                
                if overlap_ratio > 0.3:
                    confidence = "high"
                elif overlap_ratio > 0.15:
                    confidence = "medium"
                else:
                    confidence = "low"
            
            return {
                "answer": clean_response,
                "sources": sources,
                "confidence": confidence
            }
        
        except Exception as e:
            return {
                "answer": response,
                "sources": [],
                "confidence": "low"
            }
    
    def summarize_pdf(self, text: str, max_length: int = 200) -> str:
        """Generate concise PDF summary.
        
        Args:
            text: Full PDF text content
            max_length: Maximum summary length in words
            
        Returns:
            PDF summary string
        """
        try:
            # Truncate text if too long
            words = text.split()
            if len(words) > 2000:
                text = " ".join(words[:2000]) + "..."
            
            prompt = (
                f"Summarize the following text in {max_length} words or less. "
                f"Focus on key points and main topics:\n\n{text}"
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=max_length + 50,
                timeout=30
            )
            
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
            else:
                return "Unable to generate summary"
                
        except Exception as e:
            return f"Error generating summary: {str(e)}"