// API service for communicating with the backend

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analyze an email for phishing indicators.
 * @param {Object} data - Email payload
 * @param {string} data.emailText - Email body content
 * @param {string} [data.sender] - Optional sender
 * @param {string} [data.subject] - Optional subject
 * @returns {Promise<Object>} Analysis result
 */
export const analyzePost = async (data) => {
  const response = await fetch(`${API_BASE_URL}/detect`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email_text: data.emailText,
      sender: data.sender || null,
      subject: data.subject || null,
    }),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(
      `Backend error (${response.status}). ${text || 'Is the API running on ' + API_BASE_URL + '?'}`
    );
  }

  return response.json();
};
