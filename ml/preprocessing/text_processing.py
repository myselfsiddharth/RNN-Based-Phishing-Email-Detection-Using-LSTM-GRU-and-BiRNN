"""Text preprocessing utilities for phishing email detection."""

import re
from dataclasses import dataclass


@dataclass
class CleanConfig:
    keep_urls_token: bool = True
    keep_numbers: bool = False


class TextPreprocessor:
    """Normalizes email text for classical and deep models."""

    URL_RE = re.compile(r"https?://\S+|www\.\S+")
    NON_ALNUM_RE = re.compile(r"[^a-z0-9\s]")
    MULTISPACE_RE = re.compile(r"\s+")

    def __init__(self, config: CleanConfig | None = None):
        self.config = config or CleanConfig()

    def clean_email_text(self, text: str) -> str:
        """Normalize raw email text into a model-ready string."""
        if not text:
            return ""

        normalized = text.lower().strip()
        if self.config.keep_urls_token:
            normalized = self.URL_RE.sub(" urltoken ", normalized)
        else:
            normalized = self.URL_RE.sub(" ", normalized)

        if not self.config.keep_numbers:
            normalized = re.sub(r"\d+", " ", normalized)

        normalized = self.NON_ALNUM_RE.sub(" ", normalized)
        normalized = self.MULTISPACE_RE.sub(" ", normalized).strip()
        return normalized

    def clean_corpus(self, texts: list[str]) -> list[str]:
        """Apply cleaning to a corpus of email strings."""
        return [self.clean_email_text(text) for text in texts]

    def build_email_input(self, subject: str | None, body: str | None) -> str:
        """Combine subject and body into one sequence string."""
        subject_part = (subject or "").strip()
        body_part = (body or "").strip()
        merged = f"{subject_part} {body_part}".strip()
        return self.clean_email_text(merged)

