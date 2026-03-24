import React from 'react';

const Header = () => {
  return (
    <header className="header">
      <div className="header-content">
        <p className="eyebrow">CSE543 • Cybersecurity AI Lab</p>
        <h1 className="title">
          RNN-Based Phishing Email Detection
        </h1>
        <p className="subtitle">
          Ensemble scoring with Simple RNN, LSTM, GRU, BiRNN, and TF-IDF baselines
        </p>
        <div className="header-chips">
          <span className="chip">Realtime /detect API</span>
          <span className="chip">Multi-model Ensemble</span>
          <span className="chip">Explainable Risk Scoring</span>
        </div>
      </div>
    </header>
  );
};

export default Header;

