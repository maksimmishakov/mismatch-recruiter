import React from 'react';
import './MatchList.css';

function MatchList({ matches, onStatusChange, onRefresh }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    if (score >= 40) return 'score-fair';
    return 'score-poor';
  };

  const handleStatusChange = (matchId, newStatus) => {
    if (window.confirm(`Change status to ${newStatus}?`)) {
      onStatusChange(matchId, newStatus);
    }
  };

  return (
    <div className="match-list">
      <div className="match-list-controls">
        <button className="btn btn-refresh" onClick={onRefresh}>
          🔄 Refresh
        </button>
      </div>

      {matches.length === 0 ? (
        <div className="empty-state">
          <p>No matches found</p>
        </div>
      ) : (
        <div className="matches-grid">
          {matches.map((match) => (
            <div key={match.id} className="match-card">
              <div className="match-header">
                <div className="candidate-info">
                  <h3>{match.candidate.name}</h3>
                  <p className="job-title">💼 {match.job.title}</p>
                </div>
                <div className={`score-badge ${getScoreColor(match.overall_score)}`}>
                  {match.overall_score}%
                </div>
              </div>

              <div className="match-details">
                <div className="detail-row">
                  <span className="label">Location:</span>
                  <span className="value">📍 {match.candidate.location} → {match.job.location}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Experience:</span>
                  <span className="value">{match.candidate.experience_years} years</span>
                </div>
                <div className="detail-row">
                  <span className="label">Salary Range:</span>
                  <span className="value">${match.job.salary_min.toLocaleString()} - ${match.job.salary_max.toLocaleString()}</span>
                </div>
              </div>

              <div className="score-breakdown">
                <h4>Score Breakdown</h4>
                <div className="breakdown-bars">
                  <div className="breakdown-item">
                    <span>Skills</span>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${match.score_breakdown.skills}%` }}></div>
                    </div>
                    <span className="percentage">{match.score_breakdown.skills}%</span>
                  </div>
                  <div className="breakdown-item">
                    <span>Experience</span>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${match.score_breakdown.experience}%` }}></div>
                    </div>
                    <span className="percentage">{match.score_breakdown.experience}%</span>
                  </div>
                  <div className="breakdown-item">
                    <span>Location</span>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${match.score_breakdown.location}%` }}></div>
                    </div>
                    <span className="percentage">{match.score_breakdown.location}%</span>
                  </div>
                  <div className="breakdown-item">
                    <span>Salary</span>
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${match.score_breakdown.salary}%` }}></div>
                    </div>
                    <span className="percentage">{match.score_breakdown.salary}%</span>
                  </div>
                </div>
              </div>

              {match.recommendations && match.recommendations.length > 0 && (
                <div className="recommendations">
                  <h4>💡 Recommendations</h4>
                  <ul>
                    {match.recommendations.slice(0, 3).map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="match-status">
                <label>Status:</label>
                <select
                  value={match.status}
                  onChange={(e) => handleStatusChange(match.id, e.target.value)}
                  className="status-select"
                >
                  <option value="pending">Pending</option>
                  <option value="viewed">Viewed</option>
                  <option value="applied">Applied</option>
                  <option value="rejected">Rejected</option>
                  <option value="hired">Hired</option>
                </select>
              </div>

              <div className="match-meta">
                <small>Created: {new Date(match.created_at).toLocaleDateString()}</small>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default MatchList;
