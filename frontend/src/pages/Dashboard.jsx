import { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    const token = localStorage.getItem('token');
    
    if (!token) {
      window.location.href = '/login';
      return;
    }

    try {
      setLoading(true);
      
      // Fetch analytics stats
      const statsResponse = await axios.get('/api/v1/analytics/dashboard', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(statsResponse.data);

      // Fetch recent jobs
      const jobsResponse = await axios.get('/api/v1/jobs?limit=10', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setJobs(jobsResponse.data.jobs || []);
      
      setLoading(false);
    } catch (err) {
      console.error('Dashboard data fetch error:', err);
      setError(err.response?.data?.message || 'Failed to load dashboard');
      setLoading(false);
      
      if (err.response?.status === 401) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <h2>Error</h2>
        <p>{error}</p>
        <button onClick={fetchDashboardData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>MisMatch Recruiter Dashboard</h1>
        <button onClick={handleLogout} className="btn-logout">Logout</button>
      </header>

      {/* Analytics Stats Grid */}
      <div className="stats-grid">
        {stats && (
          <>
            <div className="stat-card stat-primary">
              <div className="stat-icon">👥</div>
              <div className="stat-content">
                <h3>Total Candidates</h3>
                <p className="stat-value">{stats.total_candidates || 0}</p>
                <span className="stat-trend">+{stats.candidates_this_week || 0} this week</span>
              </div>
            </div>

            <div className="stat-card stat-success">
              <div className="stat-icon">💼</div>
              <div className="stat-content">
                <h3>Active Jobs</h3>
                <p className="stat-value">{stats.active_jobs || 0}</p>
                <span className="stat-trend">{stats.pending_jobs || 0} pending</span>
              </div>
            </div>

            <div className="stat-card stat-info">
              <div className="stat-icon">🎯</div>
              <div className="stat-content">
                <h3>Matches Today</h3>
                <p className="stat-value">{stats.matches_today || 0}</p>
                <span className="stat-trend">{stats.matches_this_week || 0} this week</span>
              </div>
            </div>

            <div className="stat-card stat-warning">
              <div className="stat-icon">📊</div>
              <div className="stat-content">
                <h3>Success Rate</h3>
                <p className="stat-value">{stats.success_rate || 0}%</p>
                <span className="stat-trend">Last 30 days</span>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Recent Jobs Section */}
      <div className="jobs-section">
        <div className="section-header">
          <h2>Recent Jobs</h2>
          <button className="btn-primary">+ New Job</button>
        </div>

        <div className="jobs-list">
          {jobs.length > 0 ? (
            jobs.map(job => (
              <div key={job.id} className="job-card">
                <div className="job-header">
                  <h3>{job.title}</h3>
                  <span className={`job-status status-${job.status}`}>
                    {job.status}
                  </span>
                </div>
                <p className="job-description">{job.description}</p>
                <div className="job-footer">
                  <span className="job-location">📍 {job.location || 'Remote'}</span>
                  <span className="job-salary">💰 {job.salary || 'Negotiable'}</span>
                  <span className="job-candidates">👥 {job.candidates_count || 0} candidates</span>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-state">
              <p>No jobs posted yet</p>
              <button className="btn-primary">Post Your First Job</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
