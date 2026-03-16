# Deep Learning–Based Detection of Phishing and Malware Links in Social Media Posts

**CSE543 - Cybersecurity Project**

A web application that analyzes social media posts to detect phishing and malicious URLs using deep learning models.

> ⚠️ **This is a prototype scaffold**. The ML models are placeholders and not yet implemented.

---

## 📋 Project Overview

This system allows users to submit social media posts containing URLs for analysis. The application uses deep learning models to determine if the URLs are potentially malicious or phishing attempts.

### Key Features

- 🎨 **Modern Web Interface**: Clean React-based UI for easy interaction
- 🔍 **URL Analysis**: Detect phishing and malware in URLs
- 🧠 **Deep Learning Models**: CNN, LSTM, and Transformer architectures (placeholder)
- 📊 **Risk Assessment**: High/Medium/Low risk classification
- 💡 **Explainability**: Human-readable explanations for predictions
- 🚀 **RESTful API**: FastAPI backend for scalability

---

## 📁 Project Structure

```
project-root/
│
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # React components
│   │   │   ├── Header.jsx
│   │   │   ├── PostInput.jsx
│   │   │   ├── ResultCard.jsx
│   │   │   └── Footer.jsx
│   │   ├── pages/            # Page components
│   │   │   └── Home.jsx
│   │   ├── services/         # API services
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── main.py           # Application entry point
│   │   ├── routes/
│   │   │   └── detect.py     # Detection endpoints
│   │   ├── services/
│   │   │   └── url_analysis.py  # URL analysis logic
│   │   └── models/
│   │       └── response_models.py  # API models
│   └── requirements.txt
│
├── ml/                       # Machine learning models
│   ├── models/
│   │   ├── cnn_model.py      # CNN placeholder
│   │   ├── lstm_model.py     # LSTM placeholder
│   │   └── transformer_model.py  # Transformer placeholder
│   ├── preprocessing/
│   │   └── text_processing.py    # Text preprocessing
│   ├── train.py              # Training script
│   └── README.md
│
├── datasets/                 # Dataset directory (empty)
│
├── docs/                     # Documentation
│   └── architecture.md       # System architecture
│
└── README.md                 # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v16+) and npm
- **Python** (3.9+)
- **pip** (Python package manager)

### Installation

#### 1. Clone the Repository

```bash
cd CSE543  # or your project directory
```

#### 2. Setup Frontend

```bash
cd frontend
npm install
```

#### 3. Setup Backend

```bash
cd ../backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Running the Application

#### Start Backend Server

```bash
cd backend
# Activate virtual environment if not already activated
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

#### Start Frontend Development Server

Open a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:3000` or `http://localhost:5173`

#### Access the Application

Open your browser and navigate to:
- Frontend: `http://localhost:3000` or `http://localhost:5173`
- Backend API Docs: `http://localhost:8000/docs`

---

## 🎯 Usage

### Web Interface

1. **Open the Application** in your browser
2. **Enter Social Media Post** content in the text area (optional)
3. **Enter URL** to analyze
4. **Click "Analyze Post"**
5. **View Results** showing:
   - Risk Level (High/Medium/Low)
   - Prediction (Phishing/Suspicious/Safe)
   - Confidence Score
   - Explanation

### API Usage

#### Detection Endpoint

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "post_text": "Check out this amazing deal!",
    "url": "http://example.com"
  }'
```

**Response**:
```json
{
  "risk_level": "High",
  "prediction": "Potential Phishing",
  "confidence": 0.92,
  "explanation": "Model identified suspicious URL patterns..."
}
```

---

## 🧠 Machine Learning Models

### Model Architecture (Placeholder)

This project is designed to use three deep learning models:

#### 1. CNN Model
- **Purpose**: Detect patterns in URL structure
- **Architecture**: Convolutional layers for feature extraction
- **Status**: ⏳ Placeholder - Implementation pending

#### 2. LSTM Model
- **Purpose**: Sequential analysis of URLs and text
- **Architecture**: Bidirectional LSTM with attention mechanism
- **Status**: ⏳ Placeholder - Implementation pending

#### 3. Transformer Model
- **Purpose**: Contextual understanding of posts and URLs
- **Architecture**: Multi-head self-attention (or fine-tuned BERT)
- **Status**: ⏳ Placeholder - Implementation pending

### Training (Future)

```bash
cd ml

# Train CNN model
python train.py --model cnn --data ../datasets --epochs 10

# Train LSTM model
python train.py --model lstm --data ../datasets --epochs 10

# Train Transformer model
python train.py --model transformer --data ../datasets --epochs 10

# Train all models
python train.py --model all --data ../datasets --epochs 10
```

**Note**: Training scripts are placeholders. Implementation required.

---

## 📊 Current Implementation Status

| Component | Status | Description |
|-----------|--------|-------------|
| Frontend UI | ✅ Complete | React components with clean design |
| Backend API | ✅ Complete | FastAPI with placeholder detection |
| Mock Detection | ✅ Working | Returns random mock results |
| CNN Model | ⏳ Placeholder | Architecture defined, implementation needed |
| LSTM Model | ⏳ Placeholder | Architecture defined, implementation needed |
| Transformer | ⏳ Placeholder | Architecture defined, implementation needed |
| Preprocessing | ⏳ Placeholder | Structure defined, implementation needed |
| Training Pipeline | ⏳ Placeholder | Script structure ready |
| Dataset | ⏳ Not Collected | Need phishing/legitimate URL datasets |

---

## 🔧 Technology Stack

### Frontend
- **React** - UI library
- **Vite** - Build tool and dev server
- **CSS3** - Styling

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Machine Learning (Planned)
- **PyTorch** - Deep learning framework
- **Transformers** - Pre-trained models (optional)
- **scikit-learn** - ML utilities
- **NLTK/spaCy** - Text processing

---

## 📝 Future Implementation Tasks

### High Priority
- [ ] Collect phishing and legitimate URL datasets
- [ ] Implement CNN model architecture
- [ ] Implement LSTM model architecture
- [ ] Implement Transformer model architecture
- [ ] Implement preprocessing pipeline
- [ ] Implement training pipeline
- [ ] Integrate trained models with backend

### Medium Priority
- [ ] Add batch processing endpoint
- [ ] Implement model explainability (SHAP, attention visualization)
- [ ] Add database for storing analysis history
- [ ] Implement user authentication
- [ ] Add rate limiting
- [ ] Create Docker containers

### Low Priority
- [ ] Add more URL features (WHOIS, SSL info)
- [ ] Implement ensemble model predictions
- [ ] Add real-time URL reputation checking
- [ ] Create admin dashboard
- [ ] Add analytics and reporting

---

## 📖 Documentation

- [Architecture Documentation](docs/architecture.md) - Detailed system architecture
- [ML Models README](ml/README.md) - Machine learning implementation details
- [API Documentation](http://localhost:8000/docs) - Interactive API docs (when server is running)

---

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test  # TODO: Add test scripts
```

### Backend Testing
```bash
cd backend
pytest  # TODO: Add test files
```

---

## 🤝 Contributing

This is a research project for CSE543. Contributions and suggestions are welcome!

### Development Workflow

1. Make changes to the code
2. Test locally (frontend + backend)
3. Ensure no linting errors
4. Document your changes
5. Submit for review

---

## ⚠️ Important Notes

1. **This is a research prototype** - Not production-ready
2. **ML models are placeholders** - No real detection capabilities yet
3. **Mock responses** - Current detection returns random results
4. **Security** - CORS is open for development, restrict in production
5. **Dataset required** - Need to collect training data before implementing models

---

## 🎓 Academic Context

**Course**: CSE543 - Cybersecurity  
**Project Type**: Research Prototype  
**Goal**: Demonstrate deep learning approaches to phishing detection  
**Institution**: University Project  

---

## 📧 Support

For questions or issues related to this project, please refer to:
- Architecture documentation in `docs/`
- Code comments in source files
- TODO comments indicating future implementation needs

---

## 📄 License

This is a university research project. All rights reserved.

---

## 🙏 Acknowledgments

- CSE543 Course Staff
- PyTorch and FastAPI communities
- React and Vite teams

---

**Built with ❤️ for Cybersecurity Research**

