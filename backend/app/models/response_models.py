"""
Pydantic response models for API endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional


class DetectionResponse(BaseModel):
    """
    Response model for phishing detection endpoint
    """
    risk_level: str = Field(
        ...,
        description="Risk level: High, Medium, or Low",
        example="High"
    )
    prediction: str = Field(
        ...,
        description="Prediction label",
        example="Potential Phishing"
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence score (0-1)",
        example=0.92
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the prediction",
        example="Model identified suspicious URL patterns including domain mimicry"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "risk_level": "High",
                "prediction": "Potential Phishing",
                "confidence": 0.92,
                "explanation": "Model identified suspicious URL patterns including domain mimicry and unusual TLD"
            }
        }


class BatchDetectionResponse(BaseModel):
    """
    Response model for batch detection endpoint
    TODO: Implement batch processing
    """
    results: list[DetectionResponse]
    total_analyzed: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int

