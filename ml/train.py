"""Training script for phishing email detection models.

Implements:
- Deep models: simple_rnn, lstm, gru, birnn (TensorFlow/Keras)
- Baselines: naive_bayes, logistic_regression, sgd, random_forest, mlp
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier

from preprocessing.text_processing import TextPreprocessor

TF_IMPORT_ERROR = None

try:
    from tensorflow.keras import Sequential
    from tensorflow.keras.layers import Bidirectional, Dense, Embedding, GRU, LSTM, SimpleRNN
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.preprocessing.text import Tokenizer
except Exception as exc:  # pragma: no cover - exercised in minimal environments
    Sequential = None
    Bidirectional = Dense = Embedding = GRU = LSTM = SimpleRNN = None
    pad_sequences = Tokenizer = None
    TF_IMPORT_ERROR = exc


# Single-column text fields (first match wins).
TEXT_COLUMN_PRIORITY = (
    "text_combined",
    "text",
    "email_text",
    "body",
    "content",
    "message",
)


def _pick_text_column(df: pd.DataFrame) -> Optional[str]:
    for col in TEXT_COLUMN_PRIORITY:
        if col in df.columns:
            return col
    return None


def _has_subject_and_body(df: pd.DataFrame) -> bool:
    return "subject" in df.columns and "body" in df.columns


def _merge_subject_body(df: pd.DataFrame) -> pd.Series:
    subj = df["subject"].fillna("").astype(str).str.strip()
    body = df["body"].fillna("").astype(str).str.strip()
    merged = (subj + " " + body).str.strip()
    return merged


def _normalize_labels(series: pd.Series) -> pd.Series:
    """Coerce labels to binary 0/1; supports numeric and common string aliases.

    Preserves the index; rows that cannot be parsed become NaN (caller drops them).
    """
    lower = series.astype(str).str.strip().str.lower()
    str_map = {
        "0": 0.0,
        "1": 1.0,
        "false": 0.0,
        "true": 1.0,
        "legitimate": 0.0,
        "ham": 0.0,
        "benign": 0.0,
        "safe": 0.0,
        "ok": 0.0,
        "phishing": 1.0,
        "spam": 1.0,
        "malicious": 1.0,
        "attack": 1.0,
    }
    from_map = lower.map(str_map)
    from_numeric = pd.to_numeric(series, errors="coerce")
    from_string_numeric = pd.to_numeric(lower, errors="coerce")
    out = from_numeric.fillna(from_map).fillna(from_string_numeric)
    out = pd.to_numeric(out, errors="coerce").round()
    bad_mask = out.notna() & ~out.isin([0.0, 1.0])
    if bad_mask.any():
        bad_vals = out.loc[bad_mask].unique().tolist()[:10]
        raise ValueError(
            f"Labels must be binary 0/1 after normalization. Unexpected values: {bad_vals}"
        )
    return out


def load_dataset(data_csv: str):
    """Load CSV dataset and return cleaned texts and labels."""
    df = pd.read_csv(data_csv).dropna(how="all")
    if "label" not in df.columns:
        raise ValueError("Dataset must contain a 'label' column (binary 0/1 or supported string aliases).")

    text_col = _pick_text_column(df)
    if text_col is not None:
        use = df[[text_col, "label"]].copy()
        use = use.rename(columns={text_col: "text"})
    elif _has_subject_and_body(df):
        use = df[["subject", "body", "label"]].copy()
        use["text"] = _merge_subject_body(use)
        use = use[["text", "label"]]
    else:
        raise ValueError(
            "Dataset must include either: "
            + ", ".join(TEXT_COLUMN_PRIORITY)
            + "; or both 'subject' and 'body' columns."
        )

    use["label"] = _normalize_labels(use["label"])
    use = use.dropna(subset=["label", "text"])
    use["label"] = use["label"].astype(int)
    use = use[use["text"].astype(str).str.strip() != ""]
    use = use.drop_duplicates()

    preprocessor = TextPreprocessor()
    texts = preprocessor.clean_corpus(use["text"].astype(str).tolist())
    labels = use["label"].to_numpy()
    return texts, labels


def compute_metrics(y_true, y_pred):
    """Compute key binary classification metrics."""
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "false_positive_rate": float(fp / (fp + tn)) if (fp + tn) else 0.0,
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
    }


def _stratify_or_none(labels, min_count: int = 2):
    """Return labels for stratification only when class counts are sufficient."""
    unique, counts = np.unique(labels, return_counts=True)
    if len(unique) < 2:
        return None
    if counts.min() < min_count:
        return None
    return labels


def _require_tensorflow():
    """Raise a clear runtime error when TensorFlow isn't installed."""
    if Tokenizer is None or pad_sequences is None or Sequential is None:
        raise RuntimeError(
            "TensorFlow is required for deep model training. Install with: pip install tensorflow"
        ) from TF_IMPORT_ERROR


def build_rnn_model(
    model_name: str,
    vocab_size: int,
    max_len: int,
    embedding_dim: int = 128,
    recurrent_units: int = 64,
):
    """Build requested recurrent model architecture."""
    if Sequential is None:
        raise RuntimeError(
            "TensorFlow is required for deep model training. Install with: pip install tensorflow"
        ) from TF_IMPORT_ERROR

    model = Sequential()
    model.add(Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_len))

    if model_name == "simple_rnn":
        model.add(SimpleRNN(recurrent_units))
    elif model_name == "lstm":
        model.add(LSTM(recurrent_units))
    elif model_name == "gru":
        model.add(GRU(recurrent_units))
    elif model_name == "birnn":
        model.add(Bidirectional(SimpleRNN(recurrent_units)))
    else:
        raise ValueError(f"Unsupported deep model: {model_name}")

    model.add(Dense(64, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


def train_deep_model(model_name: str, texts, labels, epochs: int, batch_size: int, max_len: int):
    """Train one deep recurrent model and evaluate."""
    _require_tensorflow()
    strat = _stratify_or_none(labels)
    X_train, X_temp, y_train, y_temp = train_test_split(
        texts, labels, test_size=0.3, random_state=42, stratify=strat
    )
    temp_strat = _stratify_or_none(y_temp)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=temp_strat
    )

    tokenizer = Tokenizer(num_words=20000, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train)

    train_seq = pad_sequences(tokenizer.texts_to_sequences(X_train), maxlen=max_len, padding="post", truncating="post")
    val_seq = pad_sequences(tokenizer.texts_to_sequences(X_val), maxlen=max_len, padding="post", truncating="post")
    test_seq = pad_sequences(tokenizer.texts_to_sequences(X_test), maxlen=max_len, padding="post", truncating="post")

    vocab_size = min(20000, len(tokenizer.word_index) + 1)
    model = build_rnn_model(model_name, vocab_size=vocab_size, max_len=max_len)
    model.fit(
        train_seq,
        y_train,
        validation_data=(val_seq, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=0,
    )

    probs = model.predict(test_seq, verbose=0).reshape(-1)
    preds = (probs >= 0.5).astype(int)
    metrics = compute_metrics(y_test, preds)
    return model, tokenizer, metrics


def train_baselines(texts, labels):
    """Train TF-IDF + classical ML baselines.

    Uses lighter RF/MLP settings when n is large so full-dataset runs finish in reasonable time.
    """
    strat = _stratify_or_none(labels)
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=strat
    )

    n_train = len(X_train)
    large = n_train >= 30_000

    max_feat = 20000 if large else 25000
    vectorizer = TfidfVectorizer(max_features=max_feat, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    rf_trees = 100 if large else 200
    mlp_hidden = (64, 32) if large else (128, 64)
    mlp_iter = 80 if large else 200

    models = {
        "naive_bayes": MultinomialNB(),
        "logistic_regression": LogisticRegression(max_iter=300 if large else 500),
        "sgd": SGDClassifier(loss="log_loss", max_iter=1000, tol=1e-3),
        "random_forest": RandomForestClassifier(
            n_estimators=rf_trees, random_state=42, n_jobs=-1
        ),
        "mlp": MLPClassifier(
            hidden_layer_sizes=mlp_hidden,
            max_iter=mlp_iter,
            early_stopping=True,
            n_iter_no_change=5,
            random_state=42,
        ),
    }

    results: Dict[str, Any] = {}
    fitted_models: Dict[str, Any] = {}
    for name, model in models.items():
        model.fit(X_train_vec, y_train)
        preds = model.predict(X_test_vec)
        results[name] = compute_metrics(y_test, preds)
        fitted_models[name] = model

    return vectorizer, fitted_models, results


def save_json(data: dict, path: Path):
    """Save JSON with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_text(data: str, path: Path):
    """Save raw text payload."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(data, encoding="utf-8")


def save_baseline_artifacts(baseline_dir: Path, vectorizer, fitted_models: Dict[str, Any]) -> None:
    """Persist TF-IDF vectorizer and fitted sklearn classifiers for inference."""
    baseline_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, baseline_dir / "vectorizer.joblib")
    for name, model in fitted_models.items():
        joblib.dump(model, baseline_dir / f"{name}.joblib")
    manifest = {
        "artifact_type": "tfidf_sklearn",
        "classifiers": sorted(fitted_models.keys()),
        "default_classifier": "logistic_regression",
    }
    save_json(manifest, baseline_dir / "manifest.json")


def main():
    parser = argparse.ArgumentParser(description="Train phishing email detection models")
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        choices=["simple_rnn", "lstm", "gru", "birnn", "baselines", "all"],
        help="Model family to train",
    )
    parser.add_argument("--data", type=str, required=True, help="Path to CSV dataset with text + label")
    parser.add_argument("--epochs", type=int, default=5, help="Epochs for deep models")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for deep models")
    parser.add_argument("--max-len", type=int, default=200, help="Max tokenized sequence length")
    parser.add_argument("--output", type=str, default="./saved_models", help="Output directory")
    parser.add_argument(
        "--max-rows",
        type=int,
        default=None,
        help="Optional cap on rows after load (stratified split; use for quick tests)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    texts, labels = load_dataset(args.data)

    if args.max_rows is not None and len(labels) > args.max_rows:
        strat = _stratify_or_none(labels)
        texts, _, labels, _ = train_test_split(
            texts,
            labels,
            train_size=args.max_rows,
            random_state=42,
            stratify=strat,
        )
        labels = np.asarray(labels)

    summary = {"dataset_size": int(len(labels)), "runs": {}}
    deep_targets = ["simple_rnn", "lstm", "gru", "birnn"] if args.model == "all" else [args.model]

    if args.model in {"simple_rnn", "lstm", "gru", "birnn", "all"}:
        for model_name in deep_targets:
            model, tokenizer, metrics = train_deep_model(
                model_name=model_name,
                texts=texts,
                labels=labels,
                epochs=args.epochs,
                batch_size=args.batch_size,
                max_len=args.max_len,
            )
            model_dir = output_dir / model_name
            model_dir.mkdir(parents=True, exist_ok=True)
            model.save(model_dir / "model.keras")
            save_text(tokenizer.to_json(), model_dir / "tokenizer.json")
            save_json(metrics, model_dir / "metrics.json")
            save_json(
                {"model_architecture": model_name, "max_len": args.max_len},
                model_dir / "meta.json",
            )
            summary["runs"][model_name] = metrics

    if args.model in {"baselines", "all"}:
        _vectorizer, fitted_models, baseline_metrics = train_baselines(texts, labels)
        baseline_dir = output_dir / "baselines"
        baseline_dir.mkdir(parents=True, exist_ok=True)
        save_baseline_artifacts(baseline_dir, _vectorizer, fitted_models)
        save_json(baseline_metrics, baseline_dir / "metrics.json")
        summary["runs"]["baselines"] = baseline_metrics

    save_json(summary, output_dir / "training_summary.json")
    print("Training completed. Summary saved to:", output_dir / "training_summary.json")


if __name__ == "__main__":
    main()

