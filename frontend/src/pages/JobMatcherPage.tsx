import React, { useState } from 'react';
import { Zap, Target, TrendingUp, AlertCircle } from 'lucide-react';

interface Match {
  candidate_id: string;
  name: string;
  email: string;
  match_score: number;
  skills_match: string[];
  missing_skills: string[];
}

const JobMatcherPage: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleMatch = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await fetch(`${API_URL}/api/match-resume-to-job`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ job_description: jobDescription }),
      });

      const data = await res.json();
      if (res.ok) {
        setMatches(data.matches || []);
      } else {
        setError(data.message || 'Failed to find matches');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        <div className="text-center mb-8">
          <Zap className="mx-auto h-12 w-12 text-indigo-600 mb-4" />
          <h1 className="text-4xl font-bold text-gray-900">Job Matcher</h1>
          <p className="mt-2 text-gray-600">Find the perfect candidates for your job openings</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left: Job Description Input */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-lg p-6 sticky top-8">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Job Description</h2>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none"
              />
              <button
                onClick={handleMatch}
                disabled={loading}
                className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-lg transition"
              >
                {loading ? 'Matching...' : 'Find Matches'}
              </button>
            </div>
          </div>

          {/* Right: Matches List */}
          <div className="lg:col-span-2">
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            {matches.length > 0 ? (
              <div className="space-y-4">
                {matches.map((match, idx) => (
                  <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex items-start justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-bold text-gray-900">{match.name}</h3>
                        <p className="text-sm text-gray-600">{match.email}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-3xl font-bold text-indigo-600">{Math.round(match.match_score)}%</p>
                        <p className="text-xs text-gray-600">Match Score</p>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm font-medium text-gray-900 mb-2">Skills Match:</p>
                        <div className="flex flex-wrap gap-2">
                          {match.skills_match.map((skill, i) => (
                            <span key={i} className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                              ✓ {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900 mb-2">Missing Skills:</p>
                        <div className="flex flex-wrap gap-2">
                          {match.missing_skills.map((skill, i) => (
                            <span key={i} className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded">
                              ✗ {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <button className="mt-4 w-full bg-indigo-100 hover:bg-indigo-200 text-indigo-700 font-medium py-2 px-4 rounded-lg transition">
                      View Profile
                    </button>
                  </div>
                ))}
              </div>
            ) : !loading && jobDescription && (
              <div className="bg-gray-50 rounded-lg border border-gray-200 p-8 text-center">
                <Target className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <p className="text-gray-600">No matches found. Try refining your job description.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobMatcherPage;
