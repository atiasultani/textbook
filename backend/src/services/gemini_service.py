import os
import google.generativeai as genai
from typing import List, Optional
from dotenv import load_dotenv
import logging
import hashlib

load_dotenv()

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for interacting with Google Gemini API for embeddings and generation"""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            # If no API key is provided, we'll use a simple fallback method
            logger.warning("GEMINI_API_KEY not provided, using simple fallback embedding method")
            self.use_api = False
        else:
            genai.configure(api_key=api_key)
            self.embedding_model = genai.EmbeddingModel("embedding-001")  # Gemini embedding model
            self.generative_model = genai.GenerativeModel("gemini-pro")  # or another appropriate model
            self.use_api = True

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Google Gemini API or fallback method"""
        if self.use_api:
            try:
                # Handle text that might be too long for the API
                # The Gemini embedding model has a limit, so we might need to chunk very long texts
                if len(text) > 10000:  # Adjust this limit based on actual API constraints
                    text = text[:10000]  # Truncate to safe length, or implement proper chunking

                response = self.embedding_model.embed_content(text)
                return response.embedding
            except Exception as e:
                logger.error(f"Error generating Gemini embeddings: {e}")
                # Return a zero vector with the expected dimension (768 for Gemini embeddings)
                return [0.0] * 768
        else:
            # Fallback: simple hash-based embedding (not ideal for semantic similarity, but functional)
            return self._simple_text_embedding(text)

    def _simple_text_embedding(self, text: str) -> List[float]:
        """
        Simple fallback embedding method using text hashing.
        This is not semantically meaningful but provides a consistent vector representation.
        """
        # Create a hash of the text
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

        # Convert hex hash to a list of floats between -1 and 1
        embedding = []
        for i in range(0, len(text_hash), 2):
            if i + 1 < len(text_hash):
                hex_pair = text_hash[i:i+2]
                value = int(hex_pair, 16) / 255.0  # Normalize to 0-1
                value = (value * 2) - 1  # Adjust to -1 to 1 range
                embedding.append(value)

        # Pad or truncate to 768 dimensions (Gemini's embedding size)
        while len(embedding) < 768:
            embedding.append(0.0)
        if len(embedding) > 768:
            embedding = embedding[:768]

        return embedding

    def generate_text(self, prompt: str) -> str:
        """Generate text using Google Gemini API"""
        if self.use_api:
            try:
                response = self.generative_model.generate_content(prompt)
                return response.text
            except Exception as e:
                logger.error(f"Error generating text with Gemini: {e}")
                return "Sorry, I encountered an error processing your request."
        else:
            return "Gemini API key not provided. Text generation not available."