import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {'Content-Type': 'application/json'}
});

axiosInstance.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

axiosInstance.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (email, username, password, fullName) =>
    axiosInstance.post('/auth/register', {email, username, password, full_name: fullName}),
  login: (email, password) =>
    axiosInstance.post('/auth/login', {email, password}),
  getCurrentUser: () => axiosInstance.get('/auth/me')
};

export const candidatesAPI = {
  create: (candidateData) => axiosInstance.post('/candidates', candidateData),
  getAll: (page = 1, perPage = 20) =>
    axiosInstance.get('/candidates', {params: {page, per_page: perPage}}),
  getById: (id) => axiosInstance.get(`/candidates/${id}`),
  update: (id, candidateData) => axiosInstance.put(`/candidates/${id}`, candidateData),
  delete: (id) => axiosInstance.delete(`/candidates/${id}`),
  getMatches: (id) => axiosInstance.get(`/candidates/${id}/matches`)
};

export const jobsAPI = {
  create: (jobData) => axiosInstance.post('/jobs', jobData),
  getAll: (page = 1, perPage = 20) =>
    axiosInstance.get('/jobs', {params: {page, per_page: perPage}}),
  getById: (id) => axiosInstance.get(`/jobs/${id}`),
  update: (id, jobData) => axiosInstance.put(`/jobs/${id}`, jobData),
  delete: (id) => axiosInstance.delete(`/jobs/${id}`),
  getMatches: (id) => axiosInstance.get(`/jobs/${id}/matches`)
};

export const matchesAPI = {
  create: (candidateId, jobId) =>
    axiosInstance.post('/matches', {candidate_id: candidateId, job_id: jobId}),
  getAll: (page = 1, perPage = 20, status = null) =>
    axiosInstance.get('/matches', {params: {page, per_page: perPage, ...(status && {status})}}),
  updateStatus: (id, status) => axiosInstance.put(`/matches/${id}`, {status})
};

export default axiosInstance;
