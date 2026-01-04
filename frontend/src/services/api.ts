const API_BASE = process.env.VITE_API_URL || 'http://localhost:8000/api';

interface JobData {
  title: string;
  company_name: string;
  description: string;
  salary_min: number;
  salary_max: number;
  seniority_level: string;
  location: string;
  work_mode: string;
  required_skills: string[];
}

export const jobsApi = {
  async createJob(data: JobData) {
    const res = await fetch(`${API_BASE}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },

  async getJob(jobId: number) {
    const res = await fetch(`${API_BASE}/jobs/${jobId}`);
    return res.json();
  },

  async listJobs() {
    const res = await fetch(`${API_BASE}/jobs`);
    return res.json();
  },

  async updateJob(jobId: number, data: Partial<JobData>) {
    const res = await fetch(`${API_BASE}/jobs/${jobId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },

  async closeJob(jobId: number) {
    const res = await fetch(`${API_BASE}/jobs/${jobId}/close`, {
      method: 'POST'
    });
    return res.json();
  }
};

export const salaryApi = {
  async getSalaryRange(title: string, seniority: string, location = 'USA') {
    const params = new URLSearchParams({ title, seniority, location });
    const res = await fetch(`${API_BASE}/salary/range?${params}`);
    return res.json();
  },

  async calculateSalaryMatch(jobMin: number, jobMax: number, candMin: number, candMax: number) {
    const res = await fetch(`${API_BASE}/salary/match`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_min: jobMin, job_max: jobMax, candidate_min: candMin, candidate_max: candMax })
    });
    return res.json();
  }
};

export const analyticsApi = {
  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/analytics/dashboard`);
    return res.json();
  },

  async getJobPerformance(jobId: number) {
    const res = await fetch(`${API_BASE}/analytics/job/${jobId}`);
    return res.json();
  },

  async getMarketTrends(location = 'USA') {
    const res = await fetch(`${API_BASE}/analytics/trends?location=${location}`);
    return res.json();
  }
};
