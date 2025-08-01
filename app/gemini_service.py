"""
Gemini Service
Handles Google Gemini API integration for query processing and response generation
"""

import google.generativeai as genai
import logging
from typing import List, Dict, Any
import os
import asyncio

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for Gemini operations using Google Gemini API"""

    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash"):
        # Set up API key - you can get this from Google AI Studio
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        self.model = model

        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(model)

        logger.info(f"Initialized Gemini service with model: {model}")

    async def generate_answer(self, query: str, context: str) -> str:
        """
        Generate answer based on query and retrieved context using Gemini

        Args:
            query: User query
            context: Retrieved document context

        Returns:
            Generated answer string
        """

        # System prompt for answer generation
        system_prompt = """You are an expert assistant specializing in insurance, legal, HR, and compliance document analysis.

Your task is to provide accurate, helpful answers based solely on the provided context. Follow these guidelines:

1. Answer based only on the provided context
2. If the context doesn't contain enough information, say so clearly
3. Be specific and cite relevant details from the context
4. For insurance/legal queries, be precise about terms, conditions, and limitations
5. If asked about specific clauses, quote them directly when possible
6. Maintain a professional, helpful tone
7. Keep answers concise but comprehensive"""

        user_prompt = f"""Context from retrieved documents:
{context}

Question: {query}

Please provide a comprehensive answer based on the context above."""

        try:
            # Create the full prompt
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            # Generate response using Gemini
            response = await asyncio.to_thread(
                self.client.generate_content,
                full_prompt
            )

            return response.text.strip()

        except Exception as e:
            logger.error(f"Error generating answer with Gemini: {e}")
            return f"I apologize, but I encountered an error while processing your query: {str(e)}"

    async def generate_batch_answers(self, queries: List[str], contexts: List[str]) -> List[str]:
        """
        Generate answers for multiple queries efficiently using Gemini

        Args:
            queries: List of user queries
            contexts: List of context strings for each query

        Returns:
            List of answers
        """
        tasks = []

        for query, context in zip(queries, contexts):
            task = self.generate_answer(query, context)
            tasks.append(task)

        try:
            # Process all queries concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            answers = []
            for result in results:
                if isinstance(result, Exception):
                    answers.append(f"Error processing query: {str(result)}")
                else:
                    answers.append(result)

            return answers

        except Exception as e:
            logger.error(f"Error in batch processing with Gemini: {e}")
            return [f"Error processing queries: {str(e)}"] * len(queries)

    def test_connection(self) -> bool:
        """Test Gemini API connection"""
        try:
            response = self.client.generate_content("Hello, test connection")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini API connection test failed: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            "model": self.model,
            "api_key_configured": bool(self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE"),
            "connection_test": self.test_connection()
        }
