import React from 'react';

const ResultCard = ({ result }) => {
  if (!result) return null;
  const confidencePct = Math.max(0, Math.min(100, Number(result.confidence || 0) * 100));
  const modelTokens = String(result.model_used || '')
    .split('-')
    .filter(Boolean)
    .slice(0, 6);

  const getRiskClass = (riskLevel) => {
    switch (riskLevel.toLowerCase()) {
      case 'high':
        return 'risk-high';
      case 'medium':
        return 'risk-medium';
      case 'low':
        return 'risk-low';
      default:
        return '';
    }
  };

  return (
    <div className="card result-card">
      <h2>Detection Result</h2>

      <div className="result-content">
        <div className="result-item">
          <span className="result-label">Model Used:</span>
          <span className="result-value">{result.model_used || 'N/A'}</span>
        </div>

        <div className="result-item">
          <span className="result-label">Risk Level:</span>
          <span className={`result-value risk-badge ${getRiskClass(result.risk_level)}`}>
            {result.risk_level}
          </span>
        </div>

        <div className="result-item">
          <span className="result-label">Prediction:</span>
          <span className="result-value">{result.prediction}</span>
        </div>

        <div className="result-item">
          <span className="result-label">Confidence:</span>
          <span className="result-value">{confidencePct.toFixed(1)}%</span>
        </div>
        <div className="confidence-meter" aria-label="confidence meter">
          <div className="confidence-fill" style={{ width: `${confidencePct}%` }} />
        </div>

        <div className="result-item">
          <span className="result-label">Email Preview:</span>
          <span className="result-value url-value">{result.email_preview || 'N/A'}</span>
        </div>

        {modelTokens.length > 0 && (
          <div className="model-token-row">
            {modelTokens.map((token) => (
              <span className="model-token" key={token}>
                {token}
              </span>
            ))}
          </div>
        )}

        <div className="result-explanation">
          <h3>Explainability</h3>
          <p>{result.explanation}</p>
          {String(result.model_used || '').toLowerCase().includes('heuristic') && (
            <p className="placeholder-notice">
              ⚠️ Backend is using heuristic fallback because trained artifacts are missing/unloadable.
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultCard;

