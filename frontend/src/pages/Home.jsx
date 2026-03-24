import React, { useState } from 'react';
import Header from '../components/Header';
import PostInput from '../components/PostInput';
import ResultCard from '../components/ResultCard';
import Footer from '../components/Footer';
import { analyzePost } from '../services/api';
import ShapeBlur from '../components/ShapeBlur';
import FadeContent from '../components/FadeContent';

const Home = () => {
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (data) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await analyzePost(data);
      setResult(response);
    } catch (err) {
      setError(err.message || 'Analysis failed. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="reactbits-bg-layer" aria-hidden="true">
        <ShapeBlur
          variation={2}
          pixelRatioProp={1.5}
          shapeSize={0.9}
          roundness={0.65}
          borderSize={0.03}
          circleSize={0.24}
          circleEdge={0.6}
        />
      </div>
      <Header />
      
      <main className="main-content">
        <div className="container">
          <FadeContent blur duration={700} delay={100}>
            <section className="intro-panel card">
              <p>
                Paste an email and run ensemble inference across trained deep models and TF-IDF baselines.
                Use sender and subject fields for richer context.
              </p>
            </section>
          </FadeContent>

          <FadeContent blur duration={750} delay={150}>
            <PostInput onAnalyze={handleAnalyze} isLoading={isLoading} />
          </FadeContent>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <FadeContent blur duration={600}>
            <ResultCard result={result} />
          </FadeContent>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Home;

