import React, { useState, useEffect } from 'react';
import './App.css';
import MatchList from './components/MatchList';
import CandidateForm from './components/CandidateForm';

function App() {
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    minScore: 50,
    status: 'all',
    sortBy: 'score_desc'
  });

  // Fetch matches from API
  const fetchMatches = async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append('min_score', filters.minScore);
      if (filters.status !== 'all') params.append('status', filters.status);
      params.append('sort_by', filters.sortBy);

      const response = await fetch(`/api/matches?${params}`);
      if (!response.ok) throw new Error('Failed to fetch matches');
      const data = await response.json();
      setMatches(data.matches);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch matches on mount and when filters change
  useEffect(() => {
    fetchMatches();
  }, [filters]);

  // Calculate new match
  const handleCalculateMatch = async (candidateId, jobId) => {
    setLoading(true);
    try {
      const response = await fetch('/api/matches/calculate-score', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ candidate_id: candidateId, job_id: jobId })
      });
      if (!response.ok) throw new Error('Failed to calculate match');
      const result = await response.json();
      // Add new match to list
      setMatches([result.match, ...matches]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Update match status
  const handleUpdateStatus = async (matchId, newStatus) => {
    try {
      const response = await fetch(`/api/matches/${matchId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      if (!response.ok) throw new Error('Failed to update status');
      const updated = await response.json();
      setMatches(matches.map(m => m.id === matchId ? updated.match : m));
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 MisMatch Recruiter - Smart Job Matching</h1>
        <p>AI-powered candidate-job matching platform</p>
      </header>

      <main className="App-main">
        {error && (
          <div className="alert alert-error">
            {error}
            <button onClick={() => setError(null)}>×</button>
          </div>
        )}

        <section className="candidate-section">
          <h2>New Match Calculation</h2>
          <CandidateForm onCalculate={handleCalculateMatch} />
        </section>

        <section className="filters-section">
          <h2>Filters & Sorting</h2>
          <div className="filters-container">
            <div className="filter-group">
              <label htmlFor="minScore">Min Score:</label>
              <input
                id="minScore"
                type="range"
                min="0"
                max="100"
                value={filters.minScore}
                onChange={(e) => setFilters({...filters, minScore: parseInt(e.target.value)})}
              />
              <span>{filters.minScore}%</span>
            </div>

            <div className="filter-group">
              <label htmlFor="status">Status:</label>
              <select
                id="status"
                value={filters.status}
                onChange={(e) => setFilters({...filters, status: e.target.value})}
              >
                <option value="all">All</option>
                <option value="pending">Pending</option>
                <option value="viewed">Viewed</option>
                <option value="applied">Applied</option>
                <option value="rejected">Rejected</option>
                <option value="hired">Hired</option>
              </select>
            </div>

            <div className="filter-group">
              <label htmlFor="sortBy">Sort By:</label>
              <select
                id="sortBy"
                value={filters.sortBy}
                onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
              >
                <option value="score_desc">Score (High to Low)</option>
                <option value="score_asc">Score (Low to High)</option>
                <option value="recent">Most Recent</option>
                <option value="oldest">Oldest</option>
              </select>
            </div>
          </div>
        </section>

        <section className="matches-section">
          <h2>Matches ({matches.length})</h2>
          {loading ? (
            <div className="loading">Loading matches...</div>
          ) : matches.length > 0 ? (
            <MatchList
              matches={matches}
              onStatusChange={handleUpdateStatus}
              onRefresh={fetchMatches}
            />
          ) : (
            <div className="no-matches">No matches found. Try adjusting your filters.</div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
