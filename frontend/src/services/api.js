import axios from 'axios';

// Use the environment variable we set in Docker (or default to localhost)
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
});

// --- AUTH SERVICES ---

export const loginUser = async (email, password) => {
  // 1. Convert to Form Data (Required by FastAPI OAuth2)
  const formData = new URLSearchParams();
  formData.append('username', email); // FastAPI expects 'username', even if it's an email
  formData.append('password', password);

  // 2. Send as x-www-form-urlencoded
  const response = await api.post('/api/auth/token', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return response.data;
};

export const registerUser = async (username, email, master_password) => {
  // Registration expects JSON with username, email, and master_password
  const response = await api.post('/api/auth/register', {
    username,
    email,
    master_password
  });
  return response.data;
};

// --- PASSWORD SERVICES ---

export const getPasswords = async () => {
  const token = localStorage.getItem("token");
  const response = await api.get('/api/passwords/', {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export const createPassword = async (passwordData) => {
  const token = localStorage.getItem("token");
  const response = await api.post('/api/passwords/', passwordData, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export default api;