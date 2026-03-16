# Machine Learning Models

This directory contains placeholder implementations for deep learning models used in phishing detection.

## Models

### 1. CNN Model (`models/cnn_model.py`)
- Convolutional Neural Network for pattern detection
- Designed to capture local patterns in URLs and text
- **Status**: Placeholder - Implementation pending

### 2. LSTM Model (`models/lstm_model.py`)
- Long Short-Term Memory network for sequential analysis
- Captures sequential patterns and dependencies
- Includes attention mechanism
- **Status**: Placeholder - Implementation pending

### 3. Transformer Model (`models/transformer_model.py`)
- Transformer-based model for contextual understanding
- Self-attention mechanism for long-range dependencies
- Option to use pre-trained BERT/RoBERTa
- **Status**: Placeholder - Implementation pending

## Preprocessing

### Text Processing (`preprocessing/text_processing.py`)
- URL feature extraction
- Text tokenization
- Feature engineering
- **Status**: Placeholder - Implementation pending

## Training

### Training Script (`train.py`)
```bash
# Train CNN model
python train.py --model cnn --data ./datasets --epochs 10

# Train LSTM model
python train.py --model lstm --data ./datasets --epochs 10

# Train Transformer model
python train.py --model transformer --data ./datasets --epochs 10

# Train all models
python train.py --model all --data ./datasets --epochs 10
```

**Status**: Placeholder - Implementation pending

## TODO

- [ ] Implement CNN architecture
- [ ] Implement LSTM architecture with attention
- [ ] Implement Transformer architecture
- [ ] Implement preprocessing pipeline
- [ ] Add data loading and batching
- [ ] Implement training loops
- [ ] Add evaluation metrics
- [ ] Add model checkpointing
- [ ] Add experiment tracking (TensorBoard)
- [ ] Implement ensemble methods
- [ ] Add model explainability (SHAP, attention visualization)
- [ ] Fine-tune pre-trained models (BERT, RoBERTa)

## Dataset Requirements

The models expect datasets in the following format:

```
datasets/
├── train/
│   ├── phishing_urls.csv
│   └── legitimate_urls.csv
├── val/
│   ├── phishing_urls.csv
│   └── legitimate_urls.csv
└── test/
    ├── phishing_urls.csv
    └── legitimate_urls.csv
```

Each CSV should contain:
- `url`: The URL string
- `text`: Optional social media post context
- `label`: 0 (legitimate) or 1 (phishing)

## Model Outputs

Models should output:
- **Prediction**: Phishing or Legitimate
- **Confidence**: Probability score (0-1)
- **Explanation**: Human-readable explanation
- **Attention Weights**: For visualization (LSTM, Transformer)

## Next Steps

1. Collect and prepare training datasets
2. Implement model architectures
3. Implement preprocessing pipeline
4. Train and evaluate models
5. Deploy best-performing model
6. Add explainability features

