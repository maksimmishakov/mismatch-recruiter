import React, { useState, useEffect } from 'react';
import { analyticsApi } from '../services/api';

export default function AnalyticsPage() {
  const [stats, setStats] = useState<any>(null);
  const [trends, setTrends] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      const [statsData, trendsData] = await Promise.all([
        analyticsApi.getDashboardStats(),
        analyticsApi.getMarketTrends()
      ]);
      setStats(statsData);
      setTrends(trendsData);
    } catch (error) {
      console.error('Failed to load analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center py-8">Loading analytics...</div>;

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Analytics & Insights</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-gray-600 text-sm">Total Jobs</p>
          <p className="text-3xl font-bold text-blue-600">{stats?.total_jobs}</p>
        </div>
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <p className="text-gray-600 text-sm">Active Jobs</p>
          <p className="text-3xl font-bold text-green-600">{stats?.active_jobs}</p>
        </div>
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <p className="text-gray-600 text-sm">Total Matches</p>
          <p className="text-3xl font-bold text-purple-600">{stats?.total_matches}</p>
        </div>
        <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <p className="text-gray-600 text-sm">Avg Match Score</p>
          <p className="text-3xl font-bold text-orange-600">{stats?.average_match_score?.toFixed(1)}%</p>
        </div>
      </div>

      <div className="bg-white border rounded-lg p-6">
        <h2 className="text-xl font-bold mb-4">Market Trends</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-3">Top Locations</h3>
            <ul className="space-y-2">
              {trends?.top_locations?.map((loc: any, i: number) => (
                <li key={i} className="flex justify-between">
                  <span>{loc[0]}</span>
                  <span className="font-bold">{loc[1]} jobs</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-3">Seniority Distribution</h3>
            <ul className="space-y-2">
              {Object.entries(trends?.seniority_dist || {}).map(([level, count]: [string, any]) => (
                <li key={level} className="flex justify-between">
                  <span>{level}</span>
                  <span className="font-bold">{count}%</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
