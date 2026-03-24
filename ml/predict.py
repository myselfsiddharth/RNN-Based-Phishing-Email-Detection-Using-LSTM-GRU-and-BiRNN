"""Run inference on saved baseline (TF-IDF + sklearn) or deep (Keras) models.

Examples:
  python predict.py --baseline-dir ./saved_models/baselines --text "Verify your account now at http://evil.com"
  python predict.py --deep-dir ./saved_models/lstm --text "Urgent wire transfer needed"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Optional

import joblib
import numpy as np

from preprocessing.text_processing import TextPreprocessor

TF_IMPORT_ERROR = None
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.keras.preprocessing.text import tokenizer_from_json
except Exception as exc:  # pragma: no cover
    load_model = None
    pad_sequences = None
    tokenizer_from_json = None
    TF_IMPORT_ERROR = exc


def _clean_text(raw: str) -> str:
    return TextPreprocessor().clean_email_text(raw)


def _phishing_proba_sklearn(clf, X) -> tuple[int, float]:
    """Return (predicted_label 0/1, P(phishing)) when possible."""
    pred = int(clf.predict(X)[0])
    if hasattr(clf, "predict_proba"):
        proba = clf.predict_proba(X)[0]
        p_phish = float(proba[1]) if len(proba) > 1 else float(proba[0])
    elif hasattr(clf, "decision_function"):
        # Not a true probability; map with sigmoid for display only
        s = float(np.asarray(clf.decision_function(X)).ravel()[0])
        p_phish = float(1.0 / (1.0 + np.exp(-s)))
    else:
        p_phish = float(pred)
    return pred, p_phish


def predict_baseline(baseline_dir: Path, raw_text: str, classifier: str) -> dict:
    """Load vectorizer + classifier from train.py baseline export."""
    vec_path = baseline_dir / "vectorizer.joblib"
    clf_path = baseline_dir / f"{classifier}.joblib"
    if not vec_path.is_file():
        raise FileNotFoundError(
            f"Missing {vec_path}. Re-run training with a recent ml/train.py so baselines export joblib artifacts."
        )
    if not clf_path.is_file():
        raise FileNotFoundError(
            f"Missing {clf_path}. Available classifiers: {list(baseline_dir.glob('*.joblib'))}"
        )

    vectorizer = joblib.load(vec_path)
    clf = joblib.load(clf_path)
    cleaned = _clean_text(raw_text)
    X = vectorizer.transform([cleaned])
    pred, p_phish = _phishing_proba_sklearn(clf, X)

    return {
        "model_type": "baseline",
        "classifier": classifier,
        "label": pred,
        "prediction": "phishing" if pred == 1 else "legitimate",
        "phishing_probability": round(p_phish, 4),
        "text_preview": cleaned[:200] + ("..." if len(cleaned) > 200 else ""),
    }


def predict_deep(deep_dir: Path, raw_text: str, max_len: Optional[int]) -> dict:
    """Load Keras model + tokenizer from train.py deep export."""
    if load_model is None or pad_sequences is None or tokenizer_from_json is None:
        raise RuntimeError(
            "TensorFlow is required for deep model inference. Install with: pip install tensorflow"
        ) from TF_IMPORT_ERROR

    model_path = deep_dir / "model.keras"
    tok_path = deep_dir / "tokenizer.json"
    meta_path = deep_dir / "meta.json"

    if not model_path.is_file():
        raise FileNotFoundError(f"Missing {model_path}")
    if not tok_path.is_file():
        raise FileNotFoundError(f"Missing {tok_path}")

    meta: dict = {}
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))

    seq_len = max_len if max_len is not None else int(meta.get("max_len", 200))

    model = load_model(model_path)
    tokenizer = tokenizer_from_json(tok_path.read_text(encoding="utf-8"))
    cleaned = _clean_text(raw_text)
    seq = tokenizer.texts_to_sequences([cleaned])
    padded = pad_sequences(seq, maxlen=seq_len, padding="post", truncating="post")
    p_phish = float(model.predict(padded, verbose=0).reshape(-1)[0])
    pred = 1 if p_phish >= 0.5 else 0

    return {
        "model_type": "deep",
        "architecture": meta.get("model_architecture"),
        "label": pred,
        "prediction": "phishing" if pred == 1 else "legitimate",
        "phishing_probability": round(p_phish, 4),
        "max_len": seq_len,
        "text_preview": cleaned[:200] + ("..." if len(cleaned) > 200 else ""),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Test saved phishing detection models")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--baseline-dir",
        type=str,
        help="Path to .../baselines folder (with vectorizer.joblib and *.joblib)",
    )
    group.add_argument(
        "--deep-dir",
        type=str,
        help="Path to a deep model folder (e.g. .../lstm with model.keras)",
    )
    parser.add_argument("--text", type=str, required=True, help="Email body text to classify")
    parser.add_argument(
        "--classifier",
        type=str,
        default="logistic_regression",
        help="Baseline classifier name (default: logistic_regression)",
    )
    parser.add_argument(
        "--max-len",
        type=int,
        default=None,
        help="Sequence length for deep models (overrides meta.json if set)",
    )
    args = parser.parse_args()

    if args.baseline_dir:
        out = predict_baseline(Path(args.baseline_dir), args.text, args.classifier)
    else:
        out = predict_deep(Path(args.deep_dir), args.text, args.max_len)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
