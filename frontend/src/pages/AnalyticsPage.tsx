import React, { useState, useEffect } from 'react';
import { BarChart, TrendingUp, Users, Zap } from 'lucide-react';

const AnalyticsPage: React.FC = () => {
  const [stats, setStats] = useState({
    total_candidates: 0,
    successful_matches: 0,
    avg_match_score: 0,
    active_jobs: 0,
  });
  const [loading, setLoading] = useState(true);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await fetch(`${API_URL}/api/analytics`, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` },
      });
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  const metrics = [
    { label: 'Total Candidates', value: stats.total_candidates, icon: Users, color: 'bg-blue-500' },
    { label: 'Successful Matches', value: stats.successful_matches, icon: Zap, color: 'bg-green-500' },
    { label: 'Average Match Score', value: `${stats.avg_match_score.toFixed(1)}%`, icon: TrendingUp, color: 'bg-purple-500' },
    { label: 'Active Jobs', value: stats.active_jobs, icon: BarChart, color: 'bg-orange-500' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900">Analytics Dashboard</h1>
          <p className="mt-2 text-gray-600">Track your recruitment performance and metrics</p>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            <p className="mt-4 text-gray-600">Loading analytics...</p>
          </div>
        ) : (
          <>
            {/* Metrics Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {metrics.map((metric, idx) => {
                const Icon = metric.icon;
                return (
                  <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-600">{metric.label}</p>
                        <p className="text-3xl font-bold text-gray-900 mt-2">{metric.value}</p>
                      </div>
                      <div className={`${metric.color} p-3 rounded-lg`}>
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Match Score Distribution */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Match Score Distribution</h2>
                <div className="space-y-3">
                  {[{ label: '90-100%', percentage: 35 }, { label: '80-89%', percentage: 40 }, { label: '70-79%', percentage: 20 }, { label: '<70%', percentage: 5 }].map((item, idx) => (
                    <div key={idx}>
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-700 font-medium">{item.label}</span>
                        <span className="text-gray-600">{item.percentage}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${item.percentage}%` }}></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top Skills */}
              <div className="bg-white rounded-lg shadow-lg p-6">
                <h2 className="text-lg font-bold text-gray-900 mb-4">Top Skills Demanded</h2>
                <div className="space-y-3">
                  {['Python', 'JavaScript', 'React', 'AWS', 'Docker', 'Kubernetes'].map((skill, idx) => (
                    <div key={idx} className="flex items-center justify-between">
                      <span className="text-gray-700">{skill}</span>
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                        {Math.floor(Math.random() * 100) + 50} jobs
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default AnalyticsPage;
