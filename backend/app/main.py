"""
FastAPI backend for Phishing Detection System
CSE543 - Cybersecurity Research Project

This is a placeholder backend implementation.
TODO: Integrate real ML models for phishing detection
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detect

# Initialize FastAPI app
app = FastAPI(
    title="Phishing Detection API",
    description="Deep Learning-based Detection of Phishing and Malware Links",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(detect.router)


@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Phishing Detection API",
        "status": "running",
        "version": "0.1.0",
        "note": "This is a research prototype with placeholder ML models"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

