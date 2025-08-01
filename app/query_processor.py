"""
Query Processor
Orchestrates the entire pipeline: document processing, embedding search, and Gemini responses
"""

import logging
from typing import List, Dict, Any
import asyncio
import time

from app.document_processor import DocumentProcessor, DocumentChunk
from app.embedding_service import EmbeddingService
from app.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class QueryProcessor:
    """Main orchestrator for the query-retrieval pipeline using Gemini"""

    def __init__(self, document_processor: DocumentProcessor,
                 embedding_service: EmbeddingService,
                 gemini_service: GeminiService):

        self.doc_processor = document_processor
        self.embedding_service = embedding_service
        self.gemini_service = gemini_service

        # Performance settings
        self.max_context_chunks = 3
        self.similarity_threshold = 0.5

        logger.info("QueryProcessor initialized with Gemini")

    async def process_request(self, document_url: str, questions: List[str]) -> List[str]:
        """
        Process a request with document URL and questions using Gemini

        Args:
            document_url: URL to document to process
            questions: List of questions to answer

        Returns:
            List of answers
        """
        start_time = time.time()
        logger.info(f"Processing request with {len(questions)} questions using Gemini")

        try:
            # Step 1: Process document
            chunks = await self._process_document(document_url)

            # Step 2: Index chunks
            self._index_chunks(chunks)

            # Step 3: Process questions with Gemini
            answers = await self._process_questions_with_gemini(questions)

            end_time = time.time()
            logger.info(f"Request processed successfully in {end_time - start_time:.2f} seconds")

            return answers

        except Exception as e:
            logger.error(f"Error processing request: {e}")
            raise Exception(f"Failed to process request: {str(e)}")

    async def _process_document(self, document_url: str) -> List[DocumentChunk]:
        """Process document from URL"""
        logger.info(f"Processing document: {document_url}")

        try:
            chunks = await self.doc_processor.process_document_from_url(document_url)
            logger.info(f"Document processed into {len(chunks)} chunks")
            return chunks

        except Exception as e:
            logger.error(f"Error processing document: {e}")
            raise

    def _index_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Index chunks for similarity search"""
        logger.info(f"Indexing {len(chunks)} chunks")

        try:
            self.embedding_service.index_chunks(chunks)
            logger.info("Chunks indexed successfully")

        except Exception as e:
            logger.error(f"Error indexing chunks: {e}")
            raise

    async def _process_questions_with_gemini(self, questions: List[str]) -> List[str]:
        """Process multiple questions efficiently using Gemini"""
        logger.info(f"Processing {len(questions)} questions with Gemini")

        try:
            # Retrieve context for all questions
            contexts = []
            for question in questions:
                context = self.embedding_service.get_context_for_query(
                    question, 
                    max_chunks=self.max_context_chunks
                )
                contexts.append(context)

            # Generate answers using Gemini
            answers = await self.gemini_service.generate_batch_answers(questions, contexts)

            return answers

        except Exception as e:
            logger.error(f"Error processing questions with Gemini: {e}")
            raise

    def health_check(self) -> Dict[str, Any]:
        """Check health of all services"""
        health = {
            "query_processor": True,
            "document_processor": True,
            "embedding_service": self.embedding_service.is_indexed,
            "gemini_service": self.gemini_service.test_connection(),
            "timestamp": time.time()
        }

        return health

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            "max_context_chunks": self.max_context_chunks,
            "similarity_threshold": self.similarity_threshold,
            "embedding_model": self.embedding_service.model_name,
            "gemini_model": self.gemini_service.model,
            "indexed_chunks": len(self.embedding_service.chunks_metadata)
        }
