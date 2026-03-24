"""Email analysis service for phishing detection.

MVP inference strategy:
- Prefer trained TF-IDF + sklearn baseline artifacts when available.
- Fallback to deterministic heuristics if artifacts are missing/unloadable.
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib


class URLAnalysisService:
    """Legacy class name retained for import compatibility."""

    HIGH_RISK_PATTERNS = [
        r"verify\s+your\s+account",
        r"update\s+your\s+password",
        r"urgent(?:ly)?",
        r"click\s+here",
        r"suspended",
        r"unusual\s+activity",
        r"act\s+now",
        r"confirm\s+your\s+identity",
        r"bank",
        r"wire\s+transfer",
        r"gift\s+card",
        r"crypto",
        r"login\s+immediately",
    ]

    CREDENTIAL_CUES = ["password", "pin", "otp", "ssn", "login", "account number", "cvv"]

    # Keep these regexes aligned with `ml/preprocessing/text_processing.py` defaults:
    # - keep_urls_token=True
    # - keep_numbers=False
    _URL_RE = re.compile(r"https?://\S+|www\.\S+")
    _NON_ALNUM_RE = re.compile(r"[^a-z0-9\s]")
    _MULTISPACE_RE = re.compile(r"\s+")

    def __init__(self) -> None:
        root = Path(__file__).resolve().parents[3]
        # Default to full-dataset training output (`train.py --output ./saved_models_full`).
        baseline_dir_default = root / "ml" / "saved_models_full" / "baselines"
        deep_root_default = root / "ml" / "saved_models_full"

        self._baseline_dir = Path(os.getenv("PHISHING_BASELINE_DIR", str(baseline_dir_default)))
        self._deep_root_dir = Path(os.getenv("PHISHING_DEEP_DIR", str(deep_root_default)))

        # Loaded models
        self._baseline_vectorizer = None
        self._baseline_classifiers: Dict[str, Any] = {}
        self._deep_models: Dict[str, Tuple[Any, Any, int]] = {}  # name -> (keras_model, tokenizer, max_len)

        self._try_load_baseline_artifacts()
        self._try_load_deep_artifacts()

    def analyze_email(self, email_text: str, sender: str | None = None, subject: str | None = None) -> dict:
        """Analyze email content and return phishing risk prediction."""
        # For baseline TF-IDF inference, training text is either:
        # - `text_combined` (already merged), or
        # - `subject` + `body` merged by the training script.
        combined = self._merge_for_model(email_text=email_text, subject=subject, sender=sender)
        baseline_scores: List[Tuple[str, float]] = []
        deep_scores: List[Tuple[str, float]] = []

        # --- Baselines (TF-IDF + sklearn) ---
        if self._baseline_vectorizer is not None and self._baseline_classifiers:
            cleaned = self._clean_email_text(combined)
            X = self._baseline_vectorizer.transform([cleaned])
            for name, clf in self._baseline_classifiers.items():
                proba = self._get_phishing_probability(clf, X)
                baseline_scores.append((f"baseline-{name}", proba))

        # --- Deep models (Keras) ---
        if self._deep_models:
            cleaned = self._clean_email_text(combined)
            for name, (model, tokenizer, max_len) in self._deep_models.items():
                seq = tokenizer.texts_to_sequences([cleaned])
                padded = self._pad_sequences(seq, maxlen=max_len, padding="post", truncating="post")
                proba = float(model.predict(padded, verbose=0).reshape(-1)[0])
                deep_scores.append((f"deep-{name}", proba))

        # --- Ensemble across all loaded models ---
        all_scores = baseline_scores + deep_scores
        if all_scores:
            mean_score = sum(score for _, score in all_scores) / len(all_scores)
            risk_level, prediction = self._risk_from_score(mean_score)

            parts = [f"{name}={score:.2f}" for name, score in all_scores]
            explanation = (
                "Ensemble prediction using trained TF-IDF/sklearn baselines and deep models. "
                + ", ".join(parts)
                + f". Ensemble mean={mean_score:.2f} -> {risk_level}."
            )
            model_used = f"ensemble-{len(all_scores)}-models-v1"

            return {
                "risk_level": risk_level,
                "prediction": prediction,
                "confidence": mean_score,
                "explanation": explanation,
                "model_used": model_used,
                "email_preview": self._preview(self._normalize(combined)),
            }

        # --- Heuristic fallback (only if no trained artifacts loaded) ---
        normalized = self._normalize(combined)
        score = self._score_text(normalized)

        # Sender/subject modifiers (only for heuristics).
        if sender and re.search(r"(support|security|help)[\W_]*(team|alert|notice)", sender.lower()):
            score += 0.03
        if subject and re.search(r"(urgent|action required|verify|suspended|payment)", subject.lower()):
            score += 0.05

        score = max(0.01, min(0.99, score))
        risk_level, prediction = self._risk_from_score(score)
        explanation = self._build_explanation(normalized, score)

        return {
            "risk_level": risk_level,
            "prediction": prediction,
            "confidence": score,
            "explanation": explanation,
            "model_used": "heuristic-email-v1",
            "email_preview": self._preview(normalized),
        }

    def _try_load_baseline_artifacts(self) -> None:
        """Load TF-IDF vectorizer and all sklearn baseline classifiers from disk."""
        try:
            vec_path = self._baseline_dir / "vectorizer.joblib"
            if not vec_path.is_file():
                return

            self._baseline_vectorizer = joblib.load(vec_path)
            self._baseline_classifiers = {}

            for clf_path in self._baseline_dir.glob("*.joblib"):
                if clf_path.name == "vectorizer.joblib":
                    continue
                # e.g. logistic_regression.joblib -> logistic_regression
                clf_name = clf_path.stem
                self._baseline_classifiers[clf_name] = joblib.load(clf_path)
        except Exception:
            self._baseline_vectorizer = None
            self._baseline_classifiers = {}

    def _try_load_deep_artifacts(self) -> None:
        """Load any available deep models (simple_rnn/lstm/gru/birnn) from disk."""
        model_names = ["simple_rnn", "lstm", "gru", "birnn"]
        try:
            import tensorflow as tf  # noqa: F401
            from tensorflow.keras.preprocessing.sequence import pad_sequences
            from tensorflow.keras.preprocessing.text import tokenizer_from_json
            from tensorflow.keras.models import load_model
        except Exception:
            return

        # Capture pad_sequences and tokenizer loader for later inference.
        self._pad_sequences = pad_sequences
        self._tokenizer_from_json = tokenizer_from_json
        self._deep_load_model = load_model

        for name in model_names:
            model_dir = self._deep_root_dir / name
            model_path = model_dir / "model.keras"
            tok_path = model_dir / "tokenizer.json"
            meta_path = model_dir / "meta.json"

            if not (model_path.is_file() and tok_path.is_file()):
                continue

            try:
                keras_model = self._deep_load_model(model_path)
                tokenizer = self._tokenizer_from_json(tok_path.read_text(encoding="utf-8"))
                max_len = 200
                if meta_path.is_file():
                    import json as _json

                    meta = _json.loads(meta_path.read_text(encoding="utf-8"))
                    max_len = int(meta.get("max_len", max_len))
                self._deep_models[name] = (keras_model, tokenizer, max_len)
            except Exception:
                continue

    def _merge_for_model(self, *, email_text: str, subject: str | None, sender: str | None) -> str:
        # Match the training script behavior: subject is merged; sender is not.
        subject_part = (subject or "").strip()
        body_part = (email_text or "").strip()
        if subject_part:
            return f"{subject_part} {body_part}".strip()
        return body_part

    def _risk_from_score(self, score: float) -> tuple[str, str]:
        if score >= 0.75:
            return "High", "Potential Phishing"
        if score >= 0.45:
            return "Medium", "Suspicious"
        return "Low", "Likely Legitimate"

    def _get_phishing_probability(self, clf: Any, X) -> float:
        # Expected: logistic regression / SGD / random forest / MLP support predict_proba.
        if hasattr(clf, "predict_proba"):
            proba = clf.predict_proba(X)[0]
            # class order should be [0,1]
            return float(proba[1]) if len(proba) > 1 else float(proba[0])

        if hasattr(clf, "decision_function"):
            # For classifiers without predict_proba, map decision score into (0,1).
            import numpy as np

            s = float(np.asarray(clf.decision_function(X)).ravel()[0])
            return float(1.0 / (1.0 + np.exp(-s)))

        # Last-resort: use predicted label as "confidence".
        pred = int(clf.predict(X)[0])
        return float(pred)

    def _clean_email_text(self, text: str) -> str:
        """Align with `ml.preprocessing.text_processing.TextPreprocessor.clean_email_text`."""
        if not text:
            return ""

        normalized = (text or "").lower().strip()
        normalized = self._URL_RE.sub(" urltoken ", normalized)
        normalized = re.sub(r"\d+", " ", normalized)
        normalized = self._NON_ALNUM_RE.sub(" ", normalized)
        normalized = self._MULTISPACE_RE.sub(" ", normalized).strip()
        return normalized

    def _normalize(self, text: str) -> str:
        collapsed = re.sub(r"\s+", " ", text or "").strip().lower()
        return collapsed

    def _score_text(self, text: str) -> float:
        if not text:
            return 0.5

        score = 0.1
        pattern_hits = sum(bool(re.search(pattern, text)) for pattern in self.HIGH_RISK_PATTERNS)
        score += min(pattern_hits * 0.12, 0.6)

        # Link and domain cue signals.
        if "http://" in text:
            score += 0.08
        if "https://" in text:
            score += 0.03
        if re.search(r"(bit\.ly|tinyurl|shorturl|rb\.gy|t\.co)", text):
            score += 0.12

        # Credential harvesting language.
        cred_hits = sum(word in text for word in self.CREDENTIAL_CUES)
        score += min(cred_hits * 0.05, 0.2)

        # Aggressive punctuation / urgency patterns.
        if text.count("!") >= 3:
            score += 0.04
        if re.search(r"(within\s+\d+\s*(hours?|minutes?)|immediately|now)", text):
            score += 0.07

        return score

    def _build_explanation(self, text: str, score: float) -> str:
        signals = []
        if re.search(r"(verify your account|confirm your identity|login immediately)", text):
            signals.append("account-verification phrasing")
        if re.search(r"(urgent|immediately|act now|suspended)", text):
            signals.append("urgency language")
        if re.search(r"http[s]?://", text):
            signals.append("embedded links")
        if re.search(r"(password|pin|otp|ssn|cvv)", text):
            signals.append("credential request cues")

        if not signals:
            signals.append("low concentration of common phishing indicators")

        return (
            f"Score {score:.2f} based on detected signals: "
            + ", ".join(signals[:4])
            + ". Replace this heuristic output with trained RNN/LSTM/GRU/BiRNN inference for production use."
        )

    def _preview(self, text: str, max_chars: int = 120) -> str:
        if len(text) <= max_chars:
            return text
        return text[: max_chars - 3] + "..."

