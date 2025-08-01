"""
LLM-Powered Intelligent Query-Retrieval System using Google Gemini API
FastAPI Application Entry Point
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import logging
import os

from app.document_processor import DocumentProcessor
from app.embedding_service import EmbeddingService
from app.gemini_service import GeminiService
from app.query_processor import QueryProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LLM Query-Retrieval System with Gemini",
    description="Intelligent document processing and query system using Google Gemini API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Authentication
BEARER_TOKEN = "c0df38f44acb385ecd42f8e0c02ee14acd6d145835643ee57acd84f79afeb798"

async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate Bearer token"""
    if credentials.credentials != BEARER_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Request/Response Models
class HackRxRequest(BaseModel):
    """Request model for /hackrx/run endpoint"""
    documents: str  # URL to document
    questions: List[str]

class HackRxResponse(BaseModel):
    """Response model for /hackrx/run endpoint"""
    answers: List[str]

# Global services
doc_processor = DocumentProcessor()
embedding_service = EmbeddingService()
gemini_service = GeminiService()
query_processor = QueryProcessor(doc_processor, embedding_service, gemini_service)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "LLM Query-Retrieval System with Gemini is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "model": "Google Gemini",
        "services": {
            "document_processor": True,
            "embedding_service": True,
            "gemini_service": True,
        }
    }

@app.post("/hackrx/run", response_model=HackRxResponse, dependencies=[Depends(authenticate)])
async def run_hackrx(request: HackRxRequest) -> HackRxResponse:
    """
    Main endpoint to process documents and answer questions using Gemini

    Args:
        request: Contains document URL and list of questions

    Returns:
        HackRxResponse with answers for each question
    """
    try:
        logger.info(f"Processing request with {len(request.questions)} questions")

        # Process the request using Gemini
        answers = await query_processor.process_request(
            document_url=request.documents,
            questions=request.questions
        )

        logger.info(f"Successfully processed {len(answers)} answers")

        return HackRxResponse(answers=answers)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process request: {str(e)}"
        )

@app.get("/status")
async def get_status():
    """Get system status"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "model": "Google Gemini",
        "endpoints": [
            "/hackrx/run"
        ]
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False
    )
