import React, {useState, useEffect} from 'react';
import {useAuth} from '../../context/AuthContext';
import {useNavigate} from 'react-router-dom';
import {matchesAPI, candidatesAPI, jobsAPI} from '../../services/api';

export default function Dashboard() {
  const {user, logout} = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState({candidates: 0, jobs: 0, matches: 0});
  const [topMatches, setTopMatches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [candidatesRes, jobsRes, matchesRes] = await Promise.all([
        candidatesAPI.getAll(),
        jobsAPI.getAll(),
        matchesAPI.getAll(1, 5)
      ]);
      setStats({
        candidates: candidatesRes.data.total || 0,
        jobs: jobsRes.data.total || 0,
        matches: matchesRes.data.total || 0
      });
      setTopMatches(matchesRes.data.matches || []);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) return <div className="flex justify-center items-center h-screen">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">MisMatch Recruiter</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">{user?.username}</span>
              <button onClick={handleLogout} className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto py-12 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-8">Welcome, {user?.username}!</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <dt className="text-sm font-medium text-gray-500 truncate">Total Candidates</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.candidates}</dd>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <dt className="text-sm font-medium text-gray-500 truncate">Total Jobs</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.jobs}</dd>
            </div>
          </div>
          <div className="bg-white overflow-hidden shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <dt className="text-sm font-medium text-gray-500 truncate">Matches</dt>
              <dd className="mt-1 text-3xl font-semibold text-gray-900">{stats.matches}</dd>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-12">
          <button onClick={() => navigate('/candidates')} className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 font-medium">
            View Candidates
          </button>
          <button onClick={() => navigate('/jobs')} className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium">
            View Jobs
          </button>
          <button onClick={() => navigate('/matches')} className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 font-medium">
            View Matches
          </button>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Top Matches</h3>
            {topMatches.length > 0 ? (
              <div className="space-y-4">
                {topMatches.map(match => (
                  <div key={match.id} className="flex justify-between items-center p-4 border border-gray-200 rounded">
                    <div>
                      <p className="font-medium text-gray-900">Candidate {match.candidate_id} → Job {match.job_posting_id}</p>
                      <p className="text-sm text-gray-500">Status: {match.status}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-teal-600">{(match.match_score * 100).toFixed(0)}%</p>
                      <p className="text-xs text-gray-500">Match Score</p>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500">No matches yet</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
