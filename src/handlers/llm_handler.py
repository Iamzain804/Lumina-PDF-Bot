"""Groq API integration with automatic key rotation on rate limit."""

import re
import time
from typing import Dict, List

from groq import Groq


class GroqLLMHandler:
    """Groq API handler with multi-key rotation on rate limit."""

    def __init__(self, config):
        try:
            self.keys = config.GROQ_API_KEYS
            if not self.keys:
                raise ValueError("No Groq API keys found in config")

            self.current_key_index = 0
            self.client = Groq(api_key=self.keys[0])
            self.model = config.LLM_MODEL
            self.temperature = config.TEMPERATURE
            self.max_tokens = config.MAX_TOKENS

            print(f"[GroqHandler] Loaded {len(self.keys)} API key(s). Rotation enabled.")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize GroqLLMHandler: {e}")

    # ------------------------------------------------------------------ #
    #  Key Rotation                                                        #
    # ------------------------------------------------------------------ #

    def _rotate_key(self):
        """Switch to next available key in loop."""
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        self.client = Groq(api_key=self.keys[self.current_key_index])
        print(f"[GroqHandler] Rotated to key #{self.current_key_index + 1}")

    def _is_rate_limit_error(self, error: Exception) -> bool:
        """Check if error is rate limit related."""
        msg = str(error).lower()
        return any(word in msg for word in ["rate_limit", "429", "too many requests", "quota"])

    def _call_with_rotation(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Make API call, rotate key on rate limit, try all keys before giving up."""
        total_keys = len(self.keys)

        for attempt in range(total_keys * 2):  # 2 full loops max
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=15,
                )
                if not response.choices or not response.choices[0].message.content:
                    raise ValueError("Empty response from API")
                return response.choices[0].message.content.strip()

            except Exception as e:
                if self._is_rate_limit_error(e):
                    print(f"[GroqHandler] Rate limit on key #{self.current_key_index + 1} — rotating...")
                    self._rotate_key()
                    time.sleep(1)
                else:
                    # Non-rate-limit error — retry same key max 2 times then raise
                    if attempt >= 2:
                        raise
                    time.sleep(1)

        raise RuntimeError("All Groq API keys exhausted. Try again later.")

    # ------------------------------------------------------------------ #
    #  Public Methods                                                      #
    # ------------------------------------------------------------------ #

    def generate_answer(self, query: str, context: str) -> Dict[str, any]:
        try:
            prompt = self._create_prompt(query, context)
            answer_text = self._call_with_rotation(
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return self._parse_response(answer_text, context)

        except Exception as e:
            return {
                "answer": f"Error generating response: {str(e)}",
                "sources": [],
                "confidence": "low",
            }

    def summarize_pdf(self, text: str, max_length: int = 200) -> str:
        try:
            words = text.split()
            if len(words) > 2000:
                text = " ".join(words[:2000]) + "..."

            prompt = (
                f"Summarize the following text in {max_length} words or less. "
                f"Focus on key points and main topics:\n\n{text}"
            )
            return self._call_with_rotation(
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=max_length + 50,
            )
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    # ------------------------------------------------------------------ #
    #  Internal Helpers                                                    #
    # ------------------------------------------------------------------ #

    def _create_prompt(self, query: str, context: str) -> str:
        system_prompt = (
            "You are a helpful PDF assistant. Answer based only on the provided context. "
            "Be concise and cite page numbers when available."
        )
        formatted_context = "\n---\n".join(context.split("\n\n")) if context else "No context available"
        return f"{system_prompt}\n\nContext:\n{formatted_context}\n\nQuestion: {query}\n\nAnswer:"

    def _parse_response(self, response: str, context: str) -> Dict[str, any]:
        try:
            clean_response = response.replace('<', '').replace('>', '')

            page_patterns = [r'page\s*(\d+)', r'Page\s*(\d+)', r'p\.\s*(\d+)', r'P\.\s*(\d+)']
            sources = []
            for pattern in page_patterns:
                sources.extend(re.findall(pattern, clean_response, re.IGNORECASE))
            sources = sorted(list(set(sources)))

            if not sources and context:
                context_pages = re.findall(r'page\s*(\d+)', context.lower())
                if context_pages:
                    sources = sorted(list(set(context_pages))[:3])

            response_words = set(clean_response.lower().split())
            context_words = set(context.lower().split()) if context else set()

            if not context_words:
                confidence = "low"
            else:
                overlap_ratio = len(response_words & context_words) / len(response_words) if response_words else 0
                confidence = "high" if overlap_ratio > 0.3 else "medium" if overlap_ratio > 0.15 else "low"

            return {"answer": clean_response, "sources": sources, "confidence": confidence}

        except Exception:
            return {"answer": response, "sources": [], "confidence": "low"}
