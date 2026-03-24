"""Pydantic API models for phishing email detection."""

from pydantic import BaseModel, Field


class DetectionResponse(BaseModel):
    """Response model for single email phishing detection."""

    risk_level: str = Field(
        ...,
        description="Risk level: High, Medium, or Low",
        examples=["High"],
    )
    prediction: str = Field(
        ...,
        description="Prediction label",
        examples=["Potential Phishing"],
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence score between 0 and 1",
        examples=[0.91],
    )
    explanation: str = Field(
        ...,
        description="Human-readable rationale for prediction",
        examples=["Email uses urgent account-verification language and suspicious links."],
    )
    model_used: str = Field(
        ...,
        description="Model or pipeline used to generate this result",
        examples=["heuristic-email-v1"],
    )
    email_preview: str = Field(
        ...,
        description="Short sanitized preview of analyzed email text",
        examples=["your mailbox is full verify your account now..."],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "risk_level": "High",
                "prediction": "Potential Phishing",
                "confidence": 0.91,
                "explanation": (
                    "Detected urgent tone, credential-harvesting cues, and suspicious wording "
                    "common in phishing campaigns."
                ),
                "model_used": "heuristic-email-v1",
                "email_preview": "your mailbox storage is full. verify your account now...",
            }
        }
    }


class BatchDetectionResponse(BaseModel):
    """Response model for batch detection requests."""

    results: list[DetectionResponse]
    total_analyzed: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int

