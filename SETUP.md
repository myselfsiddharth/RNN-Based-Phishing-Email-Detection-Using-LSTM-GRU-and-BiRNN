# Setup Guide: RNN-Based Phishing Email Detection

This guide configures the project for experimentation with phishing email detection using `Simple RNN`, `LSTM`, `GRU`, and `Bidirectional RNN` models.

## Prerequisites

- Python 3.9+
- pip
- Node.js 16+ and npm (optional, for UI)
- Git

## 1) Environment Setup (Backend + ML)

```bash
cd backend
python -m venv venv
```

Activate virtual environment:

- Windows (PowerShell):
```powershell
venv\Scripts\Activate.ps1
```

- macOS/Linux:
```bash
source venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Install ML/training dependencies:

```bash
pip install -r ../ml/requirements.txt
```

## 2) Optional Frontend Setup

```bash
cd frontend
npm install
```

## 3) Datasets

Labeled CSVs live in `datasets/`. This repo includes:

| File | Notes |
|------|--------|
| `CEAS_08.csv` | Large; has `body`, `label`, plus metadata (`sender`, `subject`, …). |
| `Enron.csv` | `subject`, `body`, `label` — subject and body are merged automatically for training. |
| `phishing_email.csv` | `text_combined`, `label` (pre-merged text). |
| `Ling.csv`, `Nazario.csv`, `Nigerian_Fraud.csv`, `SpamAssasin.csv` | Mix of `body` + `label` and metadata columns; `body` is used when present. |

**Required:** a `label` column (`0` = legitimate, `1` = phishing). **Text:** one of `text_combined`, `text`, `email_text`, `body`, `content`, `message`, **or** both `subject` and `body` (combined into one input).

## 4) Start API (Optional Integration Testing)

After full training, artifacts are expected under `ml/saved_models_full/` (baselines + `simple_rnn`, `lstm`, `gru`, `birnn`). The backend loads them by default.

To use a different folder, set (PowerShell):

```powershell
$env:PHISHING_BASELINE_DIR="C:/path/to/ml/saved_models_full/baselines"
$env:PHISHING_DEEP_DIR="C:/path/to/ml/saved_models_full"
```

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

Expected startup output includes:

```text
Uvicorn running on http://127.0.0.1:8000
```

## 5) Start Frontend (Optional)

In a new terminal:

```bash
cd frontend
npm run dev
```

Default UI URL:

- `http://127.0.0.1:5173` (or `http://localhost:5173`)

If the page won’t load, run from `frontend/`: `npm install` then `npm run dev` (script binds to `127.0.0.1:5173`).

### “Failed to fetch” in the browser

1. **Backend must be running** on port 8000: open `http://127.0.0.1:8000/health` — you should see `{"status":"healthy"}`.
2. **CORS:** open the UI with the same host style as allowed by the API (the backend allows both `localhost` and `127.0.0.1` on ports 5173/5174).
3. If it still fails, in `frontend/` copy `.env.example` to `.env` and set `VITE_API_URL` to match how you reach the API (e.g. `http://127.0.0.1:8000`), then restart `npm run dev`.

## 6) Modeling Workflow

Quick training commands:

```bash
cd ml

# Baselines on a small sanity-check file
python train.py --model baselines --data ../datasets/sample_emails.csv --output ./saved_models

# Baselines on a full project dataset (examples)
python train.py --model baselines --data ../datasets/phishing_email.csv --output ./saved_models
python train.py --model baselines --data ../datasets/Enron.csv --output ./saved_models

# Deep model (requires TensorFlow; large CSVs need time and RAM)
python train.py --model lstm --data ../datasets/phishing_email.csv --epochs 3 --output ./saved_models

# CEAS_08 is very large — start with fewer epochs / smaller batch size if needed
python train.py --model baselines --data ../datasets/CEAS_08.csv --output ./saved_models

# Quick stratified subsample (faster smoke test; not full-data evaluation)
python train.py --model baselines --data ../datasets/phishing_email.csv --max-rows 5000 --output ./saved_models_quick
```

For datasets with **≥ ~30k** training rows, baseline mode automatically uses lighter RF/MLP settings so runs finish in reasonable time.

Use this sequence for larger experiments:

1. Clean and normalize text (lowercase, remove noise, normalize whitespace)
2. Tokenize text with Keras `Tokenizer`
3. Convert to sequences and apply `pad_sequences`
4. Train recurrent models:
   - Simple RNN
   - LSTM
   - GRU
   - Bidirectional RNN
5. Train baseline ML models with TF-IDF:
   - Naive Bayes
   - Logistic Regression
   - SGD
   - Random Forest
   - MLP
6. Evaluate with:
   - Accuracy
   - Precision
   - Recall
   - F1-score
   - Confusion matrix
   - False-positive rate

### Test saved ML model (CLI)

After training, run predictions against exported artifacts (`baselines/*.joblib` or deep `model.keras`):

```bash
cd ml

# TF-IDF + sklearn baseline (default: logistic_regression)
python predict.py --baseline-dir ./saved_models/baselines --text "Verify your account now at http://phish.example.com"

# Deep model (requires TensorFlow)
python predict.py --deep-dir ./saved_models/lstm --text "Urgent wire transfer needed"
```

Re-train baselines once if `vectorizer.joblib` is missing (older runs only saved `metrics.json`).

## 7) API Smoke Test

If `/detect` is active in backend, test with:

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{
    "email_text": "Your mailbox storage is full. Verify your account now.",
    "sender": "support-security@alerts-mail.com"
  }'
```

Current request fields are `email_text`, `sender`, and `subject`.

## Troubleshooting

### Port in Use

- Backend alternate port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Virtual Env Activation Fails (Windows)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Missing Dependencies

```bash
pip install -r requirements.txt --upgrade
```

### Frontend Dependency Issues

```bash
cd frontend
npm install
```

## Current Limitations

1. Backend inference uses a trained TF-IDF + sklearn baseline when artifacts are available (otherwise falls back to deterministic heuristics).
2. Trained deep models are saved, but not yet wired into runtime API inference.
3. `datasets/sample_emails.csv` is a tiny sanity-check dataset; use files like `phishing_email.csv` or `CEAS_08.csv` for meaningful evaluation.

