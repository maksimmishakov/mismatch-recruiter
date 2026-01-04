/**
 * API Service - Frontend to Backend Communication
 * Backend running on: http://localhost:5000
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

class ApiService {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    const token = localStorage.getItem('auth_token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    return headers;
  }

  private async request<T>(
    method: string,
    endpoint: string,
    data?: any
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;

    try {
      const options: RequestInit = {
        method,
        headers: this.getHeaders(),
      };

      if (data) {
        options.body = JSON.stringify(data);
      }

      const response = await fetch(url, options);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const responseData = await response.json();
      return {
        success: true,
        data: responseData,
      };
    } catch (error: any) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error.message || 'Unknown error occurred',
      };
    }
  }

  // Candidates Endpoints
  async getCandidates(page = 1, pageSize = 20) {
    return this.request('/api/candidates', 'GET');
  }

  async getCandidate(id: number) {
    return this.request(`/api/candidates/${id}`, 'GET');
  }

  async createCandidate(data: any) {
    return this.request('/api/candidates', 'POST', data);
  }

  async updateCandidate(id: number, data: any) {
    return this.request(`/api/candidates/${id}`, 'PUT', data);
  }

  async deleteCandidate(id: number) {
    return this.request(`/api/candidates/${id}`, 'DELETE');
  }

  // Jobs Endpoints
  async getJobs(page = 1, pageSize = 20) {
    return this.request('/api/jobs', 'GET');
  }

  async getJob(id: number) {
    return this.request(`/api/jobs/${id}`, 'GET');
  }

  async createJob(data: any) {
    return this.request('/api/jobs', 'POST', data);
  }

  async updateJob(id: number, data: any) {
    return this.request(`/api/jobs/${id}`, 'PUT', data);
  }

  async deleteJob(id: number) {
    return this.request(`/api/jobs/${id}`, 'DELETE');
  }

  // Matches Endpoints
  async getMatches(jobId: number) {
    return this.request(`/api/matches?job_id=${jobId}`, 'GET');
  }

  async getCandidateMatches(candidateId: number) {
    return this.request(`/api/matches?candidate_id=${candidateId}`, 'GET');
  }

  async getMatch(id: number) {
    return this.request(`/api/matches/${id}`, 'GET');
  }

  async createMatch(data: any) {
    return this.request('/api/matches', 'POST', data);
  }

  // Auth Endpoints
  async login(email: string, password: string) {
    const response = await this.request('/api/auth/login', 'POST', {
      email,
      password,
    });

    if (response.success && response.data?.token) {
      localStorage.setItem('auth_token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }

    return response;
  }

  async logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
    return {
      success: true,
    };
  }

  async register(userData: any) {
    return this.request('/api/auth/register', 'POST', userData);
  }

  // Analytics Endpoints
  async getAnalytics(startDate?: string, endDate?: string) {
    let endpoint = '/api/analytics';
    if (startDate && endDate) {
      endpoint += `?start_date=${startDate}&end_date=${endDate}`;
    }
    return this.request(endpoint, 'GET');
  }

  // Utility Methods
  getToken(): string | null {
    return localStorage.getItem('auth_token');
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  getUser(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}

// Export singleton instance
export const api = new ApiService();
export default api;
