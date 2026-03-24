# Project Pivot Summary

## New Project Direction

The project has been pivoted to:

**RNN-Based Phishing Email Detection Using LSTM, GRU, and BiRNN**

This replaces the earlier emphasis on social-media URL detection and aligns the repository with phishing email text classification research.

---

## Motivation

Phishing attacks continue to evolve through obfuscation and context-aware social engineering. Traditional rules and shallow ML can miss these patterns. Recurrent deep learning models are selected because they capture sequential context and long-range dependencies in email text.

---

## Scope (Pivoted)

### Included

- Supervised binary classification of emails (`phishing` vs `legitimate`)
- Text preprocessing and normalization pipeline
- Sequence modeling with recurrent neural architectures
- Baseline comparison using traditional ML + TF-IDF
- Evaluation emphasizing false-positive reduction

### Excluded

- Production deployment
- Enterprise email platform integration
- Real-time SOC/IR automation

---

## Implementation Approach

1. Load labeled phishing email datasets (CSV)
2. Remove null/duplicate records
3. Preprocess text (lowercase, URL cleanup, punctuation/noise removal)
4. Build tokenizer and transform emails into integer sequences
5. Pad/truncate sequences to fixed length
6. Train and evaluate deep learning models:
   - Simple RNN
   - LSTM
   - GRU
   - Bidirectional RNN
7. Train and evaluate baseline models:
   - Naive Bayes
   - Logistic Regression
   - SGD
   - Random Forest
   - MLP
8. Compare results with accuracy, precision, recall, F1, confusion matrix, and false-positive behavior

---

## Tools and Languages

- Python
- TensorFlow / Keras
- scikit-learn
- NLTK
- Pandas / NumPy
- Matplotlib / Seaborn
- Jupyter Notebook / Google Colab

---

## Documentation Updated in This Pivot

- `README.md` now reflects the phishing-email RNN direction
- `SETUP.md` now focuses on email dataset and recurrent-model workflow
- `PROJECT_SUMMARY.md` (this file) now tracks pivot scope and goals

---

## Immediate Next Steps

1. Align backend request/response schemas with email fields (`email_text`, optional metadata)
2. Implement the full preprocessing and training pipeline in `ml/`
3. Generate baseline-vs-RNN result tables and confusion matrices
4. Add error analysis focused on false positives and hard phishing variants

---

## Reference Base

The project uses a broad set of foundational and recent references on phishing detection, with emphasis on RNN-family models and comparative deep learning approaches for email security.

