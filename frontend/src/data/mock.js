// API service for "What If" scenarios
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Generate session ID for user tracking (stored in localStorage)
const getSessionId = () => {
  let sessionId = localStorage.getItem('whatif_session_id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('whatif_session_id', sessionId);
  }
  return sessionId;
};

export const generateScenario = async (question) => {
  try {
    const sessionId = getSessionId();
    
    const response = await axios.post(`${API}/scenarios/generate`, {
      question: question.trim(),
      session_id: sessionId
    });
    
    return response.data;
  } catch (error) {
    console.error('Error generating scenario:', error);
    
    // Provide user-friendly error message
    let errorMessage = 'Failed to generate scenario. Please try again.';
    if (error.response?.data?.detail) {
      errorMessage = error.response.data.detail;
    } else if (error.code === 'NETWORK_ERROR' || !error.response) {
      errorMessage = 'Network error. Please check your connection and try again.';
    }
    
    throw new Error(errorMessage);
  }
};

export const getScenarioHistory = async (limit = 10) => {
  try {
    const sessionId = getSessionId();
    
    const response = await axios.get(`${API}/scenarios/history`, {
      params: {
        session_id: sessionId,
        limit
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Error fetching scenario history:', error);
    throw new Error('Failed to fetch scenario history');
  }
};

// Keep mock scenarios for development/fallback purposes
export const mockScenarios = [
  {
    id: 1,
    question: "What if gravity stopped for 5 minutes?",
    scenario: "First, everyone would float like astronauts. Your coffee would become a flying liquid bomb. Birds would finally laugh at us. Then, after 5 minutes, BOOM—you'd crash back down and regret your curiosity forever.",
    timestamp: new Date().toISOString(),
    mood: "chaotic"
  }
];