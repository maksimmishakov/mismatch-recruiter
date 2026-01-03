const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
export class ApiError extends Error {
    constructor(status, data) {
        super(`API Error: ${status}`);
        Object.defineProperty(this, "status", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: status
        });
        Object.defineProperty(this, "data", {
            enumerable: true,
            configurable: true,
            writable: true,
            value: data
        });
    }
}
export async function apiCall(endpoint, options = {}) {
    const { method = 'GET', body, token = localStorage.getItem('token') || '', headers = {}, } = options;
    const url = `${API_URL}${endpoint}`;
    const fetchOptions = {
        method,
        headers: {
            'Content-Type': 'application/json',
            ...headers,
        },
    };
    if (token) {
        fetchOptions.headers = {
            ...fetchOptions.headers,
            'Authorization': `Bearer ${token}`,
        };
    }
    if (body && method !== 'GET') {
        fetchOptions.body = JSON.stringify(body);
    }
    try {
        const res = await fetch(url, fetchOptions);
        const data = await res.json();
        if (!res.ok) {
            throw new ApiError(res.status, data);
        }
        return data;
    }
    catch (err) {
        if (err instanceof ApiError)
            throw err;
        throw new Error(`Failed to call ${endpoint}`);
    }
}
// API endpoints
export const api = {
    // Auth
    auth: {
        login: (email, password) => apiCall('/api/auth/login', { method: 'POST', body: { email, password } }),
        register: (email, password, name) => apiCall('/api/auth/register', { method: 'POST', body: { email, password, name } }),
        me: () => apiCall('/api/auth/me'),
        logout: () => apiCall('/api/auth/logout', { method: 'POST' }),
    },
    // Candidates
    candidates: {
        list: () => apiCall('/api/candidates'),
        get: (id) => apiCall(`/api/candidates/${id}`),
        create: (data) => apiCall('/api/candidates', { method: 'POST', body: data }),
        update: (id, data) => apiCall(`/api/candidates/${id}`, { method: 'PUT', body: data }),
        delete: (id) => apiCall(`/api/candidates/${id}`, { method: 'DELETE' }),
    },
    // Jobs
    jobs: {
        list: () => apiCall('/api/jobs'),
        get: (id) => apiCall(`/api/jobs/${id}`),
        create: (data) => apiCall('/api/jobs', { method: 'POST', body: data }),
    },
    // Matching
    match: {
        resumeToJob: (jobDescription) => apiCall('/api/match-resume-to-job', {
            method: 'POST',
            body: { job_description: jobDescription },
        }),
    },
    // Upload
    upload: {
        single: (file) => {
            const formData = new FormData();
            formData.append('file', file);
            const token = localStorage.getItem('token');
            return fetch(`${API_URL}/api/upload`, {
                method: 'POST',
                body: formData,
                headers: { 'Authorization': `Bearer ${token}` },
            }).then(r => r.json());
        },
        batch: (file, mode) => {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('mode', mode);
            const token = localStorage.getItem('token');
            return fetch(`${API_URL}/api/batch-upload`, {
                method: 'POST',
                body: formData,
                headers: { 'Authorization': `Bearer ${token}` },
            }).then(r => r.json());
        },
    },
    // Analytics
    analytics: {
        stats: () => apiCall('/api/analytics'),
    },
};
