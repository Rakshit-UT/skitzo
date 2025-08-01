"""
Embedding Service
Handles text embeddings and vector similarity search using FAISS
"""

import numpy as np
import faiss
import logging
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

from app.document_processor import DocumentChunk

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for handling embeddings and vector search"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name

        # Initialize embedding model
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_dim = self.model.get_sentence_embedding_dimension()
            logger.info(f"Loaded embedding model: {model_name} (dim: {self.embedding_dim})")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise

        # Initialize FAISS index
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.chunks_metadata = []
        self.is_indexed = False

    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = self.model.encode(texts, normalize_embeddings=True)
            return embeddings
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def index_chunks(self, chunks: List[DocumentChunk]) -> None:
        """Index document chunks for similarity search"""
        try:
            logger.info(f"Indexing {len(chunks)} chunks...")

            # Clear existing index
            self.index.reset()
            self.chunks_metadata = []

            # Generate embeddings
            texts = [chunk.text for chunk in chunks]
            embeddings = self.embed_texts(texts)

            # Add to FAISS index
            self.index.add(embeddings.astype(np.float32))

            # Store metadata
            self.chunks_metadata = [chunk.to_dict() for chunk in chunks]

            self.is_indexed = True
            logger.info(f"Successfully indexed {len(chunks)} chunks")

        except Exception as e:
            logger.error(f"Failed to index chunks: {e}")
            raise

    def search_similar(self, query: str, top_k: int = 5, score_threshold: float = 0.5) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity"""
        if not self.is_indexed:
            logger.warning("No chunks indexed yet")
            return []

        try:
            # Generate query embedding
            query_embedding = self.embed_texts([query])

            # Search in FAISS index
            scores, indices = self.index.search(query_embedding.astype(np.float32), top_k)

            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx != -1 and score >= score_threshold:
                    chunk_data = self.chunks_metadata[idx].copy()
                    chunk_data["similarity_score"] = float(score)
                    results.append(chunk_data)

            logger.info(f"Found {len(results)} similar chunks for query")
            return results

        except Exception as e:
            logger.error(f"Failed to search similar chunks: {e}")
            raise

    def get_context_for_query(self, query: str, max_chunks: int = 3) -> str:
        """Get concatenated context text for a query"""
        similar_chunks = self.search_similar(query, top_k=max_chunks)

        context_parts = []
        for i, chunk in enumerate(similar_chunks, 1):
            text = chunk.get("text", "")
            score = chunk.get("similarity_score", 0)
            context_parts.append(f"[Context {i}] (Score: {score:.2f})\n{text}")

        return "\n\n".join(context_parts)
