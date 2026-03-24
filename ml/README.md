# Machine Learning Module

This directory contains the phishing email model training pipeline.

## Implemented Models

### Deep Learning
- `simple_rnn`
- `lstm`
- `gru`
- `birnn` (Bidirectional SimpleRNN)

### Baselines (TF-IDF)
- `naive_bayes`
- `logistic_regression`
- `sgd`
- `random_forest`
- `mlp`

## Dataset Requirements

Training expects a CSV with:

- **`label`**: `0` (legitimate) or `1` (phishing). String aliases like `ham` / `spam` are mapped when possible.
- **Text** (first match wins):
  - Single column: `text_combined`, `text`, `email_text`, `body`, `content`, or `message`
  - **Or** both **`subject`** and **`body`**: they are concatenated (e.g. `Enron.csv`)

Included project files (under `../datasets/`): `CEAS_08.csv`, `Enron.csv`, `phishing_email.csv`, `Ling.csv`, `Nazario.csv`, `Nigerian_Fraud.csv`, `SpamAssasin.csv`, plus `sample_emails.csv` for quick tests.

**Note:** `CEAS_08.csv` is very large; baseline training may take significant time and memory.

For large CSVs, `train.py` automatically uses lighter Random Forest / MLP settings when training rows ≥ 30k. Use `--max-rows 10000` for a faster stratified subsample (quick tests only).

## Install

```bash
pip install -r requirements.txt
```

## Training Commands

```bash
# Baselines only (does not require TensorFlow)
python train.py --model baselines --data ../datasets/sample_emails.csv --output ./saved_models

# Full datasets (examples)
python train.py --model baselines --data ../datasets/phishing_email.csv --output ./saved_models
python train.py --model baselines --data ../datasets/Enron.csv --output ./saved_models

# One deep model (requires TensorFlow)
python train.py --model lstm --data ../datasets/phishing_email.csv --epochs 3 --output ./saved_models

# Train all deep models + baselines (long run on large CSVs)
python train.py --model all --data ../datasets/phishing_email.csv --epochs 3 --output ./saved_models
```

## Outputs

Saved under `--output` (default: `./saved_models`):
- `<model_name>/model.keras` (deep models)
- `<model_name>/tokenizer.json` (deep models)
- `<model_name>/meta.json` (deep models: `max_len`, architecture name)
- `<model_name>/metrics.json`
- `baselines/vectorizer.joblib` + `baselines/<classifier>.joblib` + `baselines/manifest.json`
- `baselines/metrics.json`
- `training_summary.json`

## Test inference (after training)

Baseline (no TensorFlow needed):
```bash
cd ml
python predict.py --baseline-dir ./saved_models/baselines --text "Verify your account now at http://evil.com"
# Optional: --classifier naive_bayes | sgd | random_forest | mlp
```

Deep model (requires TensorFlow):
```bash
python predict.py --deep-dir ./saved_models/lstm --text "Urgent: wire transfer required"
```

If you trained **before** `vectorizer.joblib` existed, run `train.py --model baselines` once more so the `baselines/` folder includes joblib artifacts.

## Notes

- Deep model training and deep inference require TensorFlow.
- Backend API inference is currently heuristic-based and does not yet load trained artifacts.

