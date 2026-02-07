import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle 401 responses globally
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (email, password) =>
    apiClient.post('/auth/login', { email, password }),
  
  register: (userData) =>
    apiClient.post('/auth/register', userData),
  
  logout: () =>
    apiClient.post('/auth/logout'),
  
  getCurrentUser: () =>
    apiClient.get('/auth/me'),
};

// Analytics API
export const analyticsAPI = {
  getDashboard: () =>
    apiClient.get('/analytics/dashboard'),
  
  getRecruitmentMetrics: () =>
    apiClient.get('/analytics/metrics'),
  
  getCandidateStats: () =>
    apiClient.get('/analytics/candidates'),
};

// Jobs API
export const jobsAPI = {
  getAll: (params = {}) =>
    apiClient.get('/jobs', { params }),
  
  getById: (id) =>
    apiClient.get(`/jobs/${id}`),
  
  create: (jobData) =>
    apiClient.post('/jobs', jobData),
  
  update: (id, jobData) =>
    apiClient.put(`/jobs/${id}`, jobData),
  
  delete: (id) =>
    apiClient.delete(`/jobs/${id}`),
};

// Candidates API
export const candidatesAPI = {
  getAll: (params = {}) =>
    apiClient.get('/candidates', { params }),
  
  getById: (id) =>
    apiClient.get(`/candidates/${id}`),
  
  create: (candidateData) =>
    apiClient.post('/candidates', candidateData),
  
  update: (id, candidateData) =>
    apiClient.put(`/candidates/${id}`, candidateData),
};

export default apiClient;
