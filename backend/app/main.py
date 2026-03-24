"""FastAPI backend for phishing email detection research."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detect

# Initialize FastAPI app
app = FastAPI(
    title="Phishing Email Detection API",
    description="RNN-based phishing email detection with LSTM, GRU, and BiRNN evaluation",
    version="0.1.0"
)

# Configure CORS (browser sends Origin matching the page URL — localhost vs 127.0.0.1 are different)
_DEV_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_DEV_ORIGINS,
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
        "message": "Phishing Email Detection API",
        "status": "running",
        "version": "0.1.0",
        "note": "Research prototype with heuristic fallback and planned RNN-family model inference"
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

