"""Detection API endpoints for phishing email analysis."""

from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.models.response_models import BatchDetectionResponse, DetectionResponse
from app.services.url_analysis import URLAnalysisService

router = APIRouter(
    prefix="",
    tags=["detection"]
)

# Backward-compatible service import path; class now analyzes email content.
analysis_service = URLAnalysisService()


class DetectionRequest(BaseModel):
    """Request model for phishing email detection."""

    email_text: str = Field(..., min_length=1, description="Raw email body text")
    sender: Optional[str] = Field(default=None, description="Optional sender address")
    subject: Optional[str] = Field(default=None, description="Optional email subject")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email_text": (
                    "Urgent: Your mailbox storage is full. Verify your account now at "
                    "http://secure-login-alerts.example.com."
                ),
                "sender": "support-security@alerts-mail.com",
                "subject": "Action required: verify your mailbox",
            }
        }
    }


@router.post("/detect", response_model=DetectionResponse)
async def detect_phishing(request: DetectionRequest):
    """Detect phishing likelihood from email text."""
    try:
        result = analysis_service.analyze_email(
            email_text=request.email_text,
            sender=request.sender,
            subject=request.subject,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/batch-detect", response_model=BatchDetectionResponse)
async def batch_detect_phishing(requests: list[DetectionRequest]):
    """Batch detection for multiple emails."""
    if not requests:
        raise HTTPException(status_code=400, detail="Request list cannot be empty")

    results = [
        analysis_service.analyze_email(
            email_text=req.email_text,
            sender=req.sender,
            subject=req.subject,
        )
        for req in requests
    ]

    return {
        "results": results,
        "total_analyzed": len(results),
        "high_risk_count": sum(result["risk_level"] == "High" for result in results),
        "medium_risk_count": sum(result["risk_level"] == "Medium" for result in results),
        "low_risk_count": sum(result["risk_level"] == "Low" for result in results),
    }

