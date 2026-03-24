import React, { useState } from 'react';

const PostInput = ({ onAnalyze, isLoading }) => {
  const [emailText, setEmailText] = useState('');
  const [sender, setSender] = useState('');
  const [subject, setSubject] = useState('');

  const templates = [
    {
      label: 'Phishing-like',
      subject: 'URGENT: Verify your account',
      sender: 'security-alerts@paypa1-verify.com',
      body: 'Your account will be suspended in 24 hours. Verify now: http://bit.ly/verify-now and submit your login details.',
    },
    {
      label: 'Benign-like',
      subject: 'Q4 Report Draft',
      sender: 'alex@company.com',
      body: 'Hi team, attached is the updated Q4 report. Please share comments before Friday.',
    },
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (emailText.trim()) {
      onAnalyze({ emailText, sender, subject });
    }
  };

  const applyTemplate = (template) => {
    setSubject(template.subject);
    setSender(template.sender);
    setEmailText(template.body);
  };

  const clearForm = () => {
    setSubject('');
    setSender('');
    setEmailText('');
  };

  return (
    <div className="card input-card">
      <h2>Submit Email for Analysis</h2>
      <div className="template-row">
        {templates.map((template) => (
          <button
            key={template.label}
            type="button"
            className="btn btn-subtle"
            onClick={() => applyTemplate(template)}
            disabled={isLoading}
          >
            Use {template.label}
          </button>
        ))}
        <button
          type="button"
          className="btn btn-ghost"
          onClick={clearForm}
          disabled={isLoading}
        >
          Clear
        </button>
      </div>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="email-text">Email Body</label>
          <textarea
            id="email-text"
            className="input-textarea"
            rows="6"
            placeholder="Paste suspicious email content here..."
            value={emailText}
            onChange={(e) => setEmailText(e.target.value)}
          />
        </div>

        <div className="form-group">
          <label htmlFor="sender-input">Sender (optional)</label>
          <input
            id="sender-input"
            type="text"
            className="input-text"
            placeholder="e.g., support-security@alerts-mail.com"
            value={sender}
            onChange={(e) => setSender(e.target.value)}
          />
          <p className="input-hint">
            Sender metadata can improve risk scoring signals.
          </p>
        </div>

        <div className="form-group">
          <label htmlFor="subject-input">Subject (optional)</label>
          <input
            id="subject-input"
            type="text"
            className="input-text"
            placeholder="e.g., Action required: verify your mailbox"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
          />
          <p className="input-hint">
            Subject line helps capture urgency/social-engineering cues.
          </p>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !emailText.trim()}
        >
          {isLoading ? 'Analyzing...' : 'Analyze Email'}
        </button>
      </form>
    </div>
  );
};

export default PostInput;

