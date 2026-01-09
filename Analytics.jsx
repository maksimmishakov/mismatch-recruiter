import React, { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useApi } from '../hooks/useApi';

export default function Analytics() {
  const [metrics, setMetrics] = useState(null);
  const [funnel, setFunnel] = useState(null);
  const [quality, setQuality] = useState(null);
  const [timeline, setTimeline] = useState(null);
  const [loading, setLoading] = useState(true);
  const api = useApi();

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const [metricsRes, funnelRes, qualityRes, timelineRes] = await Promise.all([
          api.get('/api/analytics/dashboard?days=30'),
          api.get('/api/analytics/funnel?days=30'),
          api.get('/api/analytics/match-quality?days=30'),
          api.get('/api/analytics/timeline?days=30&interval=day'),
        ]);

        setMetrics(metricsRes.data.metrics);
        setFunnel(funnelRes.data.funnel);
        setQuality(qualityRes.data.quality);
        setTimeline(timelineRes.data.timeline);
      } catch (error) {
        console.error('Error fetching analytics:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) return <div>Loading...</div>;

  const COLORS = ['#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="analytics-dashboard">
      <h1>Analytics Dashboard</h1>

      {/* Key Metrics */}
      <div className="metrics-grid">
        <MetricCard label="Total Users" value={metrics?.total_users} />
        <MetricCard label="Total Candidates" value={metrics?.total_candidates} />
        <MetricCard label="Total Vacancies" value={metrics?.total_vacancies} />
        <MetricCard label="Application Rate" value={`${metrics?.application_rate?.toFixed(1)}%`} />
      </div>

      {/* Funnel Chart */}
      <div className="chart-container">
        <h2>User Funnel</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={[funnel]}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis />
            <YAxis />
            <Tooltip />
            <Bar dataKey="registered" fill="#8884d8" />
            <Bar dataKey="profile_completed" fill="#82ca9d" />
            <Bar dataKey="applied" fill="#ffc658" />
            <Bar dataKey="hired" fill="#ff7c7c" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Match Quality Distribution */}
      <div className="chart-container">
        <h2>Match Quality Distribution</h2>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={[
                { name: 'High Quality (80+)', value: quality?.high_quality_matches },
                { name: 'Medium Quality (50-80)', value: quality?.medium_quality_matches },
                { name: 'Low Quality (<50)', value: quality?.low_quality_matches },
              ]}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({name, value}) => `${name}: ${value}`}
              outerRadius={80}
            >
              {COLORS.map((color, index) => (
                <Cell key={`cell-${index}`} fill={color} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Conversion Rates */}
      <div className="conversion-rates">
        <h2>Key Conversion Rates (30 days)</h2>
        <div className="rates-grid">
          <RateCard label="Profile Completion" rate={funnel?.profile_completion_rate} />
          <RateCard label="Application Rate" rate={funnel?.application_rate} />
          <RateCard label="Hiring Rate" rate={funnel?.hiring_rate} />
          <RateCard label="Match Acceptance" rate={quality?.match_to_hire_rate} />
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value }) {
  return (
    <div className="metric-card">
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
    </div>
  );
}

function RateCard({ label, rate }) {
  return (
    <div className="rate-card">
      <div className="rate-label">{label}</div>
      <div className="rate-value">{rate?.toFixed(1)}%</div>
      <div className="rate-bar">
        <div
          className="rate-bar-fill"
          style={{ width: `${Math.min(rate || 0, 100)}%` }}
        ></div>
      </div>
    </div>
  );
}