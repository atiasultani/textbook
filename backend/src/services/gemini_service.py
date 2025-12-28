import os
from google import genai
from typing import List
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
            logger.warning("GEMINI_API_KEY not provided, using simple fallback embedding method")
            self.use_api = False
        else:
            # Initialize the new client
            self.client = genai.Client(api_key=api_key)
            self.use_api = True

    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings using Google GenAI API or fallback method"""
        if self.use_api:
            try:
                # Truncate long texts for safety (adjust if needed)
                if len(text) > 10000:
                    text = text[:10000]

                response = self.client.embeddings.create(
                    model="text-embedding-004",
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"Error generating Gemini embeddings: {e}")
                return [0.0] * 768
        else:
            return self._simple_text_embedding(text)

    def _simple_text_embedding(self, text: str) -> List[float]:
        """Fallback hash-based embedding"""
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        embedding = []
        for i in range(0, len(text_hash), 2):
            if i + 1 < len(text_hash):
                hex_pair = text_hash[i:i+2]
                value = int(hex_pair, 16) / 255.0
                value = (value * 2) - 1
                embedding.append(value)
        while len(embedding) < 768:
            embedding.append(0.0)
        if len(embedding) > 768:
            embedding = embedding[:768]
        return embedding

    def generate_text(self, prompt: str) -> str:
        """Generate text using Google GenAI API"""
        if self.use_api:
            try:
                response = self.client.generations.create(
                    model="gemini-pro",
                    prompt=prompt,
                    max_output_tokens=500
                )
                # The new API returns the text in response.output[0].content[0].text
                return response.output[0].content[0].text
            except Exception as e:
                logger.error(f"Error generating text with Gemini: {e}")
                return "Sorry, I encountered an error processing your request."
        else:
            return "Gemini API key not provided. Text generation not available."
