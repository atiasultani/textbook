import cohere
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import os
from ..models.chat import Source
from dotenv import load_dotenv
load_dotenv()   # <-- THIS MUST RUN BEFORE ANYTHING ELSE


class CohereConfig(BaseModel):
    """Configuration for Cohere API"""
    model_name: str = "command-r-plus"
    temperature: float = 0.3
    max_tokens: int = 1000
    supports_streaming: bool = True


class CohereService:
    """Service for interacting with Cohere API for RAG responses"""

    def __init__(self):
        api_key = os.getenv("COHERE_API_KEY")
        if not api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(api_key)
        self.config = CohereConfig()

    def generate_response(
        self,
        query: str,
        context_sources: List[Source],
        selected_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a response using Cohere based on the query and context sources.

        Args:
            query: The user's query
            context_sources: List of sources with relevant content
            selected_text: Optional text that was selected by the user for targeted questioning

        Returns:
            Dictionary containing the response, sources, confidence score, and hallucination flag
        """
        # Validate inputs
        if not query or len(query.strip()) == 0:
            raise ValueError("Query cannot be empty")

        if len(query) > 2000:
            raise ValueError("Query is too long (max 2000 characters)")

        if selected_text and len(selected_text) > 2000:
            raise ValueError("Selected text is too long (max 2000 characters)")

        # Prepare the context from sources
        context_texts = []
        for source in context_sources:
            context_texts.append(f"Chapter: {source.chapter_title}\nContent: {source.content}")

        # If selected text is provided, prioritize it in the context
        if selected_text:
            context_texts.insert(0, f"Selected text for specific question: {selected_text}")

        # Create a prompt for the Cohere model
        context_str = "\n\n".join(context_texts)

        prompt = f"""
        You are an educational assistant for a textbook on Physical AI and Humanoid Robotics.
        Answer the user's question based ONLY on the provided textbook content.
        Do not use any external knowledge or make up information.

        Context from textbook:
        {context_str}

        User question: {query}

        Provide a helpful, accurate answer based only on the textbook content provided above.
        If the answer cannot be found in the provided context, say so explicitly.
        """

        try:
            # Use Cohere's chat endpoint for generation
            response = self.client.chat(
                message=prompt,
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                documents=[{"text": source.content} for source in context_sources]  # Provide documents for grounding
            )

            # Calculate a basic confidence score based on response details
            confidence_score = self._calculate_confidence_score(response, context_sources)

            # Check for potential hallucination (simplified check)
            is_hallucinated = self._check_for_hallucination(response.text, context_str)

            return {
                "response": response.text,
                "sources": context_sources,
                "confidence_score": confidence_score,
                "is_hallucinated": is_hallucinated
            }

        except Exception as e:
            # Log the error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Cohere API error: {str(e)}")

            # In case of error, return a safe response
            return {
                "response": f"Sorry, I encountered an error processing your request: {str(e)}",
                "sources": [],
                "confidence_score": 0.0,
                "is_hallucinated": True
            }

    def _calculate_confidence_score(self, response, context_sources) -> float:
        """
        Calculate a basic confidence score based on response characteristics.
        This is a simplified implementation - a real system would use more sophisticated methods.
        """
        # Simple heuristic: if response mentions "I don't know" or similar phrases, lower confidence
        text = response.text.lower()

        if any(phrase in text for phrase in ["i don't know", "not mentioned", "not provided", "not found in context"]):
            return 0.3  # Low confidence when acknowledging lack of information

        # Higher confidence if the response directly references the provided context
        return 0.8  # Default high confidence for valid responses

    def _check_for_hallucination(self, response_text: str, context: str) -> bool:
        """
        Check if the response contains information not present in the context.
        This is a simplified implementation - a real system would use more sophisticated methods.
        """
        # For now, we'll assume responses based on provided documents are not hallucinated
        # In a real implementation, we would compare the response against the context more rigorously
        return False  # Assuming Cohere's grounding prevents hallucination when documents are provided

    def get_config(self) -> CohereConfig:
        """Get current Cohere configuration"""
        return self.config