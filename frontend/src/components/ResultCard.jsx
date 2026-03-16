import React from 'react';

const ResultCard = ({ result }) => {
  if (!result) return null;

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
          <span className="result-label">Analyzed URL:</span>
          <span className="result-value url-value">{result.url}</span>
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
          <span className="result-value">
            {(result.confidence * 100).toFixed(1)}%
          </span>
        </div>

        <div className="result-explanation">
          <h3>Explainability</h3>
          <p>{result.explanation}</p>
          <p className="placeholder-notice">
            ⚠️ This is a placeholder result. Real ML model integration pending.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;

