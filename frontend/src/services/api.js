// API service for communicating with the backend

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze a social media post for phishing/malware links
 * @param {Object} data - The post data
 * @param {string} data.postText - The social media post content
 * @param {string} data.url - The URL to analyze
 * @returns {Promise<Object>} Analysis result
 */
export const analyzePost = async (data) => {
  try {
    const response = await fetch(`${API_BASE_URL}/detect`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        post_text: data.postText,
        url: data.url,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('API Error:', error);
    // Return mock data if backend is not available (for development)
    return getMockResponse(data);
  }
};

/**
 * Mock response for development/testing when backend is unavailable
 * TODO: Remove this once real backend is connected
 */
const getMockResponse = (data) => {
  const mockResponses = [
    {
      risk_level: 'High',
      prediction: 'Potential Phishing',
      confidence: 0.92,
      explanation: 'Model identified suspicious URL patterns including domain mimicry and unusual TLD.',
    },
    {
      risk_level: 'Medium',
      prediction: 'Suspicious',
      confidence: 0.67,
      explanation: 'URL contains redirects and shortened link patterns commonly used in phishing.',
    },
    {
      risk_level: 'Low',
      prediction: 'Safe',
      confidence: 0.95,
      explanation: 'URL appears legitimate with proper HTTPS and known trusted domain.',
    },
  ];

  // Return random mock response
  return mockResponses[Math.floor(Math.random() * mockResponses.length)];
};

