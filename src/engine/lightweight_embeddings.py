"""Lightweight embeddings without PyTorch dependency."""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from pathlib import Path

class LightweightEmbeddings:
    """Simple TF-IDF based embeddings as PyTorch alternative."""
    
    def __init__(self, model_name="tfidf"):
        self.model_name = model_name
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.is_fitted = False
    
    def embed_documents(self, texts):
        """Create embeddings for documents."""
        if not self.is_fitted:
            vectors = self.vectorizer.fit_transform(texts)
            self.is_fitted = True
        else:
            vectors = self.vectorizer.transform(texts)
        return vectors.toarray()
    
    def embed_query(self, query):
        """Create embedding for query."""
        if not self.is_fitted:
            raise ValueError("Vectorizer not fitted yet")
        vector = self.vectorizer.transform([query])
        return vector.toarray()[0]