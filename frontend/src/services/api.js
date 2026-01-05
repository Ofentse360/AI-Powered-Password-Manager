import axios from 'axios';

// Create a base client
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000', 
  headers: {
    'Content-Type': 'application/json',
  },
});

// Helper to login
export const loginUser = async (username, password) => {
  // OAuth2 expects form-data, not JSON
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await api.post('/api/auth/token', formData);
  return response.data; // Returns { access_token, token_type }
};




// Helper to register
export const registerUser = async (email, password) => {
  // The backend expects JSON for registration: { email: "...", password: "..." }
  const response = await api.post('/api/auth/register', {
    email: email,
    password: password
  });
  return response.data;
};



export const getPasswords = async () => {
  const token = localStorage.getItem("token"); // Retrieve token
  
  const response = await api.get('/api/passwords/', {
    headers: { Authorization: `Bearer ${token}` } // Send it to backend
  });
  return response.data;
};

//  Add a new password
export const createPassword = async (passwordData) => {
  const token = localStorage.getItem("token");
  
  const response = await api.post('/api/passwords/', passwordData, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return response.data;
};

export default api;