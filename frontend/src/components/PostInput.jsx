import React, { useState } from 'react';

const PostInput = ({ onAnalyze, isLoading }) => {
  const [postText, setPostText] = useState('');
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (postText.trim() || url.trim()) {
      onAnalyze({ postText, url });
    }
  };

  return (
    <div className="card input-card">
      <h2>Submit Post for Analysis</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="post-text">Social Media Post Content</label>
          <textarea
            id="post-text"
            className="input-textarea"
            rows="6"
            placeholder="Paste the social media post content here..."
            value={postText}
            onChange={(e) => setPostText(e.target.value)}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="url-input">URL(s) to Analyze</label>
          <input
            id="url-input"
            type="text"
            className="input-text"
            placeholder="Enter URL (e.g., https://example.com)"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
          <p className="input-hint">
            Enter the suspicious URL found in the post
          </p>
        </div>

        <button 
          type="submit" 
          className="btn btn-primary"
          disabled={isLoading || (!postText.trim() && !url.trim())}
        >
          {isLoading ? 'Analyzing...' : 'Analyze Post'}
        </button>
      </form>
    </div>
  );
};

export default PostInput;

