import React, { useState } from 'react';
import Header from '../components/Header';
import PostInput from '../components/PostInput';
import ResultCard from '../components/ResultCard';
import Footer from '../components/Footer';
import { analyzePost } from '../services/api';

const Home = () => {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (data) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await analyzePost(data);
      setResult({
        ...response,
        url: data.url || 'No URL provided'
      });
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content">
        <div className="container">
          <PostInput onAnalyze={handleAnalyze} isLoading={isLoading} />
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <ResultCard result={result} />
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;

