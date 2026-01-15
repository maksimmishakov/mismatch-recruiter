import React, { useState } from 'react';
import './CandidateForm.css';

function CandidateForm({ onCalculate }) {
  const [formData, setFormData] = useState({
    candidateId: '',
    jobId: '',
    candidateName: '',
    candidateEmail: '',
    jobTitle: '',
    companyName: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (!formData.candidateId || !formData.jobId) {
        throw new Error('Please select both candidate and job');
      }

      await onCalculate(parseInt(formData.candidateId), parseInt(formData.jobId));
      // Reset form
      setFormData({
        candidateId: '',
        jobId: '',
        candidateName: '',
        candidateEmail: '',
        jobTitle: '',
        companyName: ''
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="candidate-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="candidateId">👤 Candidate ID:</label>
          <input
            id="candidateId"
            type="number"
            name="candidateId"
            value={formData.candidateId}
            onChange={handleInputChange}
            placeholder="e.g., 123"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="candidateName">Name:</label>
          <input
            id="candidateName"
            type="text"
            name="candidateName"
            value={formData.candidateName}
            onChange={handleInputChange}
            placeholder="Candidate name (optional)"
            disabled
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="jobId">💼 Job ID:</label>
          <input
            id="jobId"
            type="number"
            name="jobId"
            value={formData.jobId}
            onChange={handleInputChange}
            placeholder="e.g., 456"
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="jobTitle">Job Title:</label>
          <input
            id="jobTitle"
            type="text"
            name="jobTitle"
            value={formData.jobTitle}
            onChange={handleInputChange}
            placeholder="Job title (optional)"
            disabled
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label htmlFor="candidateEmail">Email:</label>
          <input
            id="candidateEmail"
            type="email"
            name="candidateEmail"
            value={formData.candidateEmail}
            onChange={handleInputChange}
            placeholder="candidate@example.com"
          />
        </div>
        <div className="form-group">
          <label htmlFor="companyName">Company:</label>
          <input
            id="companyName"
            type="text"
            name="companyName"
            value={formData.companyName}
            onChange={handleInputChange}
            placeholder="Company name (optional)"
            disabled
          />
        </div>
      </div>

      {error && (
        <div className="error-message">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !formData.candidateId || !formData.jobId}
        >
          {loading ? 'Calculating Match...' : '📊 Calculate Match'}
        </button>
        <button
          type="reset"
          className="btn btn-secondary"
          onClick={() =>
            setFormData({
              candidateId: '',
              jobId: '',
              candidateName: '',
              candidateEmail: '',
              jobTitle: '',
              companyName: ''
            })
          }
        >
          🗑️ Clear
        </button>
      </div>

      <div className="form-info">
        <p>💡 <strong>How to use:</strong></p>
        <ul>
          <li>Enter a Candidate ID from your database</li>
          <li>Enter a Job ID from your postings</li>
          <li>Click "Calculate Match" to see the AI-generated match score</li>
          <li>The system will analyze skills, experience, location, and salary</li>
        </ul>
      </div>
    </form>
  );
}

export default CandidateForm;
