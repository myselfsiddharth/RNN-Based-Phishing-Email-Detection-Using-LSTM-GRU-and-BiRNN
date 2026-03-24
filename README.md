# RNN-Based Phishing Email Detection Using LSTM, GRU, and BiRNN

**CSE543 - Cybersecurity Project**

This project is now centered on phishing email detection using recurrent deep learning models and baseline machine learning classifiers.

---

## Project Overview

Phishing remains one of the most damaging cyber threats. Rule-based methods struggle with evolving attacker tactics such as obfuscation and context-aware social engineering. This project evaluates sequence-based neural models that learn contextual and temporal cues from email text.

### Core Objectives

- Build a clean, reproducible phishing email classification pipeline
- Compare `Simple RNN`, `LSTM`, `GRU`, and `Bidirectional RNN` models
- Benchmark deep learning models against classical baselines
- Emphasize low false-positive rates to support information assurance goals

---

## Scope

### Included

- Email text preprocessing (cleaning, tokenization, sequence construction, padding)
- Supervised binary classification (`phishing` vs `legitimate`)
- Deep learning model comparison across recurrent architectures
- Baseline ML model comparison using TF-IDF features
- Evaluation using accuracy, precision, recall, F1-score, confusion matrix

### Not Included

- Production deployment
- Real-time email gateway integration
- User-facing enterprise security operations workflow

---

## Implementation Approach

1. Load labeled CSV email datasets
2. Remove null rows and duplicates
3. Normalize text (lowercase, URL and punctuation cleanup)
4. Build vocabulary with Keras tokenizer
5. Convert text to integer sequences and pad/truncate to fixed length
6. Train recurrent deep learning models on embedded sequences
7. Train baseline ML classifiers on TF-IDF features
8. Compare model performance and error profiles

---

## Models

### Deep Learning Models

- `Simple RNN`
- `LSTM`
- `GRU`
- `Bidirectional RNN`

Each model follows:
- Embedding layer
- One or more recurrent layers
- Dense output layer with sigmoid activation

### Baseline Machine Learning Models

- Naive Bayes
- Logistic Regression
- SGD Classifier
- Random Forest
- MLP Classifier

---

## Evaluation Focus

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix
- False-positive reduction (primary assurance objective)

---

## Technology Stack

- **Language**: Python
- **Deep Learning**: TensorFlow / Keras
- **Machine Learning**: scikit-learn
- **NLP**: NLTK, Keras Tokenizer
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Environment**: Jupyter Notebook, Google Colab

---

## Repository Structure (Current)

```
CSE543/
├── backend/                  # API layer and integration surface
├── frontend/                 # UI prototype
├── ml/                       # Modeling and preprocessing modules
├── datasets/                 # Dataset files (add your CSVs here)
├── docs/                     # Architecture and reports
├── SETUP.md                  # Setup and execution instructions
└── README.md                 # Project overview
```

---

## Quick Start

See `SETUP.md` for the full environment setup and run instructions.

Minimal workflow:

```bash
# 1) Setup Python environment
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
pip install -r ../ml/requirements.txt

# 2) Run backend API
python -m uvicorn app.main:app --reload --port 8000
```

```bash
# 3) Run frontend (optional, for UI testing)
cd frontend
npm install
npm run dev
```

```bash
# 4) Run ML training sanity check
cd ml
python train.py --model baselines --data ../datasets/sample_emails.csv --output ./saved_models
```

---

## Current Status

- Project direction is pivoted to phishing email detection
- Documentation is aligned with RNN/LSTM/GRU/BiRNN evaluation goals
- Backend API is functional for `/health`, `/detect`, and `/batch-detect`
- ML training script is functional for baseline and deep-model runs (TensorFlow required for deep models)
- Runtime API currently serves heuristic inference while trained-model serving integration is pending

---

## Academic Context

- **Course**: CSE543 - Cybersecurity
- **Type**: Research implementation and comparative evaluation
- **Theme**: Deep learning for phishing email detection with information assurance focus

---

## References

The project reference list is maintained in course/project documentation and includes foundational and recent work on phishing detection using RNN, LSTM, BiLSTM, and transformer-based approaches.

