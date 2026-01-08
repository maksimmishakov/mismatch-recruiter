# 🎨 Frontend Development Plan - Полный Гайд

**Дата:** 8 января 2026, 13:35 MSK  
**Время на реализацию:** 4-6 часов  
**Приоритет:** 🔴 HIGH - нужен для demo Lamoda

---

## 📁 Структура проекта

```
frontend/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   │   ├── LoginForm.jsx          (login форма)
│   │   │   ├── RegisterForm.jsx       (регистрация)
│   │   │   └── AuthContext.js         (глобальный auth state)
│   │   ├── Dashboard/
│   │   │   ├── Dashboard.jsx          (главная страница)
│   │   │   ├── Stats.jsx              (статистика)
│   │   │   └── Header.jsx             (шапка)
│   │   ├── Candidates/
│   │   │   ├── CandidateList.jsx      (список кандидатов)
│   │   │   ├── CandidateForm.jsx      (форма добавления)
│   │   │   ├── CandidateDetail.jsx    (деталь кандидата)
│   │   │   └── CandidateCard.jsx      (карточка)
│   │   ├── Jobs/
│   │   │   ├── JobList.jsx            (список вакансий)
│   │   │   ├── JobForm.jsx            (форма вакансии)
│   │   │   ├── JobDetail.jsx          (деталь вакансии)
│   │   │   └── JobCard.jsx            (карточка)
│   │   ├── Matches/
│   │   │   ├── MatchList.jsx          (список матчей)
│   │   │   ├── MatchDetail.jsx        (деталь матча)
│   │   │   └── MatchCard.jsx          (карточка матча)
│   │   └── Common/
│   │       ├── Loading.jsx            (loader)
│   │       ├── Error.jsx              (error display)
│   │       ├── Modal.jsx              (модальное окно)
│   │       └── Button.jsx             (переиспользуемая кнопка)
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── DashboardPage.jsx
│   │   ├── CandidatesPage.jsx
│   │   ├── JobsPage.jsx
│   │   ├── MatchesPage.jsx
│   │   └── NotFoundPage.jsx
│   ├── services/
│   │   ├── api.js                     (все API calls)
│   │   └── auth.js                    (auth логика)
│   ├── hooks/
│   │   ├── useAuth.js                 (auth hook)
│   │   ├── useApi.js                  (API hook)
│   │   └── useForm.js                 (form управление)
│   ├── styles/
│   │   ├── tailwind.css               (tailwind styles)
│   │   └── globals.css                (глобальные стили)
│   ├── utils/
│   │   ├── validation.js              (валидация форм)
│   │   ├── formatters.js              (форматирование данных)
│   │   └── constants.js               (константы)
│   ├── App.jsx                        (главный компонент)
│   ├── main.jsx                       (точка входа)
│   └── .env.example                   (example env файл)
├── public/
│   └── index.html
├── package.json
├── vite.config.js
└── README.md
```

---

## 🔧 Шаг 1.1: Создать API Service

**Файл:** `src/services/api.js`

Этот файл будет централизованной точкой для всех API calls.

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor для добавления JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// AUTH ENDPOINTS
export const authAPI = {
  register: (email, password, username, fullName = '') =>
    api.post('/auth/register', { email, password, username, full_name: fullName }),
  
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  
  getCurrentUser: () =>
    api.get('/auth/me'),
};

// CANDIDATES ENDPOINTS
export const candidatesAPI = {
  list: () =>
    api.get('/candidates'),
  
  get: (id) =>
    api.get(`/candidates/${id}`),
  
  create: (data) =>
    api.post('/candidates', data),
  
  update: (id, data) =>
    api.put(`/candidates/${id}`, data),
  
  delete: (id) =>
    api.delete(`/candidates/${id}`),
};

// JOBS ENDPOINTS
export const jobsAPI = {
  list: () =>
    api.get('/jobs'),
  
  get: (id) =>
    api.get(`/jobs/${id}`),
  
  create: (data) =>
    api.post('/jobs', data),
  
  update: (id, data) =>
    api.put(`/jobs/${id}`, data),
  
  delete: (id) =>
    api.delete(`/jobs/${id}`),
};

// MATCHES ENDPOINTS
export const matchesAPI = {
  list: () =>
    api.get('/matches'),
  
  create: (candidateId, jobId) =>
    api.post('/matches', { candidate_id: candidateId, job_id: jobId }),
  
  getByCandidate: (candidateId) =>
    api.get(`/candidates/${candidateId}/matches`),
  
  getByJob: (jobId) =>
    api.get(`/jobs/${jobId}/matches`),
};

// HEALTH CHECK
export const healthAPI = {
  check: () =>
    api.get('/health'),
};

export default api;
```

---

## 🔑 Шаг 1.2: Создать Auth Context

**Файл:** `src/components/Auth/AuthContext.js`

```javascript
import { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Проверить, есть ли сохраненный токен при загрузке
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      authAPI
        .getCurrentUser()
        .then((response) => setUser(response.data))
        .catch(() => {
          localStorage.removeItem('access_token');
          setUser(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, password) => {
    try {
      setError(null);
      const response = await authAPI.login(email, password);
      localStorage.setItem('access_token', response.data.access_token);
      setUser(response.data.user);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
      throw err;
    }
  };

  const register = async (email, password, username, fullName = '') => {
    try {
      setError(null);
      const response = await authAPI.register(email, password, username, fullName);
      // После регистрации можно автоматически залогинить
      await login(email, password);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
      throw err;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        login,
        register,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};
```

---

## 📝 Шаг 1.3: Создать Login Form

**Файл:** `src/components/Auth/LoginForm.jsx`

```javascript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './AuthContext';

const LoginForm = () => {
  const navigate = useNavigate();
  const { login, error: authError } = useAuth();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError(authError || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">МисМэтч</h1>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="test@lamoda.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Loading...' : 'Sign In'}
            </button>
          </form>

          <p className="mt-4 text-center text-sm text-gray-600">
            Don't have an account?{' '}
            <Link to="/register" className="text-indigo-600 hover:text-indigo-700 font-semibold">
              Register
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
```

---

## 📝 Шаг 1.4: Создать Register Form

**Файл:** `src/components/Auth/RegisterForm.jsx`

```javascript
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from './AuthContext';

const RegisterForm = () => {
  const navigate = useNavigate();
  const { register, error: authError } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: '',
    fullName: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      await register(
        formData.email,
        formData.password,
        formData.username,
        formData.fullName
      );
      navigate('/dashboard');
    } catch (err) {
      setError(authError || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">МисМэтч</h1>
          <h2 className="text-xl text-center text-gray-600 mb-6">Create Account</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Full Name</label>
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Username</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="johndoe"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="john@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="••••••••"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">Confirm Password</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
                placeholder="••••••••"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50"
            >
              {loading ? 'Creating...' : 'Create Account'}
            </button>
          </form>

          <p className="mt-4 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-indigo-600 hover:text-indigo-700 font-semibold">
              Sign In
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterForm;
```

---

## 📊 Шаг 1.5: Создать Dashboard Page

**Файл:** `src/pages/DashboardPage.jsx`

```javascript
import { useEffect, useState } from 'react';
import { useAuth } from '../components/Auth/AuthContext';
import { matchesAPI, candidatesAPI, jobsAPI } from '../services/api';

const DashboardPage = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalMatches: 0,
    totalCandidates: 0,
    totalJobs: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [matches, candidates, jobs] = await Promise.all([
          matchesAPI.list(),
          candidatesAPI.list(),
          jobsAPI.list(),
        ]);

        setStats({
          totalMatches: matches.data.length,
          totalCandidates: candidates.data.length,
          totalJobs: jobs.data.length,
        });
      } catch (err) {
        setError('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Welcome, {user?.username}! 👋</h1>

        {error && <div className="text-red-600 mb-4">{error}</div>}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold uppercase">Total Candidates</h3>
            <p className="text-4xl font-bold text-indigo-600 mt-2">{stats.totalCandidates}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold uppercase">Total Jobs</h3>
            <p className="text-4xl font-bold text-green-600 mt-2">{stats.totalJobs}</p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow">
            <h3 className="text-gray-600 text-sm font-semibold uppercase">Total Matches</h3>
            <p className="text-4xl font-bold text-blue-600 mt-2">{stats.totalMatches}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
```

---

## 📋 Шаг 1.6: Создать основные Pages

### CandidatesPage.jsx

**Файл:** `src/pages/CandidatesPage.jsx`

```javascript
import { useEffect, useState } from 'react';
import { candidatesAPI } from '../services/api';
import CandidateList from '../components/Candidates/CandidateList';
import CandidateForm from '../components/Candidates/CandidateForm';

const CandidatesPage = () => {
  const [candidates, setCandidates] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchCandidates();
  }, []);

  const fetchCandidates = async () => {
    try {
      const response = await candidatesAPI.list();
      setCandidates(response.data);
    } catch (error) {
      console.error('Failed to fetch candidates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCandidate = async (data) => {
    try {
      await candidatesAPI.create(data);
      await fetchCandidates();
      setShowForm(false);
    } catch (error) {
      console.error('Failed to add candidate:', error);
    }
  };

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Candidates</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg"
          >
            {showForm ? 'Cancel' : 'Add Candidate'}
          </button>
        </div>

        {showForm && <CandidateForm onSubmit={handleAddCandidate} />}

        <CandidateList candidates={candidates} onRefresh={fetchCandidates} />
      </div>
    </div>
  );
};

export default CandidatesPage;
```

---

## 🧪 Шаг 1.7: Создать компоненты списков

**Файл:** `src/components/Candidates/CandidateList.jsx`

```javascript
import { useState } from 'react';
import { candidatesAPI } from '../../services/api';
import CandidateCard from './CandidateCard';

const CandidateList = ({ candidates, onRefresh }) => {
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await candidatesAPI.delete(id);
        onRefresh();
      } catch (error) {
        console.error('Failed to delete candidate:', error);
      }
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {candidates.map((candidate) => (
        <CandidateCard
          key={candidate.id}
          candidate={candidate}
          onDelete={() => handleDelete(candidate.id)}
          onSelect={() => setSelectedCandidate(candidate)}
        />
      ))}
    </div>
  );
};

export default CandidateList;
```

**Файл:** `src/components/Candidates/CandidateCard.jsx`

```javascript
const CandidateCard = ({ candidate, onDelete, onSelect }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
      <h3 className="text-xl font-semibold text-gray-900">
        {candidate.first_name} {candidate.last_name}
      </h3>
      <p className="text-gray-600 text-sm">{candidate.email}</p>
      <p className="text-gray-600 text-sm mt-2">
        📍 {candidate.location || 'Not specified'}
      </p>
      <p className="text-gray-600 text-sm">
        💼 {candidate.experience_years || 0} years experience
      </p>

      <div className="mt-4">
        <span className="inline-block bg-indigo-100 text-indigo-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded">
          {candidate.skills?.length || 0} skills
        </span>
      </div>

      <div className="mt-4 flex gap-2">
        <button
          onClick={onSelect}
          className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-4 rounded text-sm"
        >
          View
        </button>
        <button
          onClick={onDelete}
          className="flex-1 bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default CandidateCard;
```

---

## 📝 Шаг 1.8: Создать главный App.jsx

**Файл:** `src/App.jsx`

```javascript
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './components/Auth/AuthContext';
import LoginForm from './components/Auth/LoginForm';
import RegisterForm from './components/Auth/RegisterForm';
import DashboardPage from './pages/DashboardPage';
import CandidatesPage from './pages/CandidatesPage';
import JobsPage from './pages/JobsPage';
import MatchesPage from './pages/MatchesPage';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <div>Loading...</div>;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return children;
};

const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/login" element={<LoginForm />} />
      <Route path="/register" element={<RegisterForm />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/candidates"
        element={
          <ProtectedRoute>
            <CandidatesPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/jobs"
        element={
          <ProtectedRoute>
            <JobsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/matches"
        element={
          <ProtectedRoute>
            <MatchesPage />
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/dashboard" />} />
    </Routes>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </Router>
  );
}

export default App;
```

---

## ✅ Контрольный список для Шага 1

- [ ] API service (`api.js`) создана - ВСЕ endpoints работают
- [ ] Auth Context (`AuthContext.js`) - JWT management
- [ ] Login Form - форма входа работает
- [ ] Register Form - регистрация работает
- [ ] Dashboard - главная страница загружает статистику
- [ ] CandidatesPage - список кандидатов
- [ ] JobsPage - список вакансий  
- [ ] MatchesPage - список матчей
- [ ] Auth interceptor - JWT добавляется в headers
- [ ] Protected routes - работает перенаправление
- [ ] npm install - все зависимости установлены
- [ ] npm run dev - запускается без ошибок
- [ ] Стили Tailwind - применяются корректно

