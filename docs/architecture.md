# System Architecture

## Overview

This document describes the architecture of the Phishing and Malware Link Detection system for social media posts.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │    Header    │  │  PostInput   │  │ ResultCard   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP REST API
                              │
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    API Routes                             │  │
│  │  • POST /detect - Phishing detection endpoint            │  │
│  │  • POST /batch-detect - Batch processing (future)        │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              URL Analysis Service                         │  │
│  │  • Feature extraction                                     │  │
│  │  • Model inference                                        │  │
│  │  • Result aggregation                                     │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Model Integration
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    ML Models (PyTorch)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  CNN Model   │  │  LSTM Model  │  │ Transformer  │          │
│  │              │  │              │  │    Model     │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Preprocessing Pipeline                       │  │
│  │  • URL tokenization                                       │  │
│  │  • Feature extraction                                     │  │
│  │  • Text processing                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer

**Technology**: React with Vite

**Components**:
- `Header`: Displays application title and description
- `PostInput`: Form for entering social media posts and URLs
- `ResultCard`: Displays detection results with risk levels
- `Footer`: Application footer with project information

**Services**:
- `api.js`: Handles HTTP communication with backend
- Includes fallback mock data for development

**Features**:
- Responsive design
- Real-time validation
- Error handling
- Loading states

### Backend Layer

**Technology**: Python FastAPI

**Structure**:
- `main.py`: Application entry point, CORS configuration
- `routes/detect.py`: Detection endpoint implementation
- `services/url_analysis.py`: URL analysis logic
- `models/response_models.py`: Pydantic response models

**API Endpoints**:

#### POST /detect
Analyzes a URL for phishing/malware indicators

**Request**:
```json
{
  "post_text": "Check out this deal!",
  "url": "http://example.com"
}
```

**Response**:
```json
{
  "risk_level": "High",
  "prediction": "Potential Phishing",
  "confidence": 0.92,
  "explanation": "Model identified suspicious patterns..."
}
```

### ML Layer

**Technology**: PyTorch

**Models**:

1. **CNN Model**
   - Purpose: Pattern detection in URLs
   - Architecture: Convolutional layers for feature extraction
   - Input: Tokenized URL sequences
   - Output: Binary classification (phishing/legitimate)

2. **LSTM Model**
   - Purpose: Sequential analysis of URLs and text
   - Architecture: Bidirectional LSTM with attention
   - Features: Attention weights for explainability
   - Output: Classification with attention visualization

3. **Transformer Model**
   - Purpose: Contextual understanding
   - Architecture: Multi-head self-attention
   - Alternative: Fine-tuned BERT/RoBERTa
   - Features: Long-range dependency capture

**Preprocessing**:
- URL tokenization (character/subword level)
- Feature extraction (URL structure, domain info)
- Text preprocessing (social media post context)
- Embedding generation

## Data Flow

### Detection Request Flow

1. **User Input**
   - User enters social media post and URL in frontend
   - Frontend validates input

2. **API Request**
   - Frontend sends POST request to `/detect` endpoint
   - Request includes post text and URL

3. **Backend Processing**
   - FastAPI receives request
   - URL Analysis Service processes input
   - Features are extracted from URL and text

4. **ML Inference** (TODO)
   - Preprocessed data sent to ML models
   - CNN analyzes URL patterns
   - LSTM analyzes sequential features
   - Transformer analyzes context
   - Ensemble predictions aggregated

5. **Result Generation**
   - Risk level determined (High/Medium/Low)
   - Confidence score calculated
   - Human-readable explanation generated
   - Explainability features extracted (attention weights)

6. **API Response**
   - Structured response sent to frontend
   - Includes prediction, confidence, explanation

7. **Display Results**
   - Frontend renders results in ResultCard
   - Risk level highlighted with color coding
   - Explanation displayed to user

## Security Considerations

### Current Implementation (Placeholder)
- CORS configured for development
- Input validation via Pydantic models
- Error handling for malformed requests

### Future Implementation (TODO)
- [ ] Rate limiting to prevent abuse
- [ ] API authentication/authorization
- [ ] Input sanitization for XSS prevention
- [ ] SQL injection prevention (if database added)
- [ ] HTTPS enforcement in production
- [ ] Secure model serving
- [ ] Logging and monitoring
- [ ] DDoS protection

## Scalability Considerations

### Future Enhancements (TODO)
- [ ] Asynchronous processing for batch requests
- [ ] Model caching for faster inference
- [ ] Database for storing analysis history
- [ ] Message queue for long-running tasks (Celery)
- [ ] Load balancing for multiple backend instances
- [ ] CDN for frontend assets
- [ ] Model versioning and A/B testing
- [ ] Monitoring and alerting (Prometheus, Grafana)

## Model Training Pipeline (Future)

```
Data Collection → Preprocessing → Feature Engineering
       ↓
Data Splitting (Train/Val/Test)
       ↓
Model Training (CNN/LSTM/Transformer)
       ↓
Hyperparameter Tuning
       ↓
Model Evaluation & Selection
       ↓
Model Deployment
       ↓
Monitoring & Retraining
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React + Vite | User interface |
| Backend | FastAPI | REST API server |
| ML Framework | PyTorch | Deep learning models |
| Preprocessing | Python | Text/URL processing |
| Deployment (Future) | Docker | Containerization |
| Database (Future) | PostgreSQL | Data persistence |
| Caching (Future) | Redis | Performance |

## Current Status

**Implemented**:
- ✅ Frontend UI with all components
- ✅ Backend API structure
- ✅ Placeholder ML model files
- ✅ Mock detection responses

**Pending**:
- ⏳ ML model implementations
- ⏳ Training pipeline
- ⏳ Real dataset integration
- ⏳ Model deployment
- ⏳ Production configuration

## Next Steps

1. Collect phishing and legitimate URL datasets
2. Implement preprocessing pipeline
3. Implement CNN model architecture
4. Implement LSTM model architecture
5. Implement Transformer model architecture
6. Train models on collected data
7. Evaluate and compare model performance
8. Integrate best-performing model with backend
9. Add explainability features
10. Deploy to production environment

