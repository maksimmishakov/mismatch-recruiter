import React, { useState, useEffect } from 'react';
import { ResumeUpload } from '../components/Resume/ResumeUpload';
import { ParsedResume } from '../components/Resume/ParsedResume';
import { Resume, handleApiError } from '../services/api';

export const ResumesPage = () => {
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResumes();
  }, []);

  const loadResumes = async () => {
    try {
      setLoading(true);
      // TODO: Call API to fetch resumes
      const data: Resume[] = [];
      setResumes(data);
      setError(null);
    } catch (err) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (newResume: Resume) => {
    setResumes([newResume, ...resumes]);
    setError(null);
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure?')) return;
    try {
      // TODO: Call API to delete resume
      setResumes(resumes.filter((r) => r.id !== id));
    } catch (err) {
      setError(handleApiError(err));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">📋 Manage Resumes</h1>
          <p className="text-gray-600 mt-2">
            Upload and manage candidate resumes. System automatically extracts
            skills and experience.
          </p>
        </div>

        <ResumeUpload
          onUploadSuccess={handleUploadSuccess}
          onError={(err) => setError(err)}
        />

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            ❌ {error}
          </div>
        )}

        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Uploaded Resumes ({resumes.length})
          </h2>

          {loading ? (
            <div className="text-center py-8 text-gray-500">
              Loading resumes...
            </div>
          ) : resumes.length === 0 ? (
            <div className="text-center py-8 text-gray-500 bg-gray-50 rounded-lg">
              No resumes yet. Upload your first resume above!
            </div>
          ) : (
            <div className="space-y-4">
              {resumes.map((resume) => (
                <ParsedResume
                  key={resume.id}
                  resume={resume}
                  onDelete={() => handleDelete(resume.id)}
                />
              ))}
            </div>
          )}
        </div>

        {resumes.length > 0 && (
          <div className="grid grid-cols-4 gap-4 bg-white rounded-lg shadow p-6">
            <div>
              <div className="text-sm text-gray-600">Total Resumes</div>
              <div className="text-2xl font-bold text-gray-900 mt-1">
                {resumes.length}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Avg Experience</div>
              <div className="text-2xl font-bold text-blue-600 mt-1">
                {Math.round(
                  resumes.reduce((sum, r) => sum + r.yearsExperience, 0) /
                    resumes.length
                )}
                y
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Avg Confidence</div>
              <div className="text-2xl font-bold text-green-600 mt-1">
                {Math.round(
                  (resumes.reduce((sum, r) => sum + r.confidence, 0) /
                    resumes.length) *
                    100
                )}
                %
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Unique Skills</div>
              <div className="text-2xl font-bold text-purple-600 mt-1">
                {new Set(resumes.flatMap((r) => r.skills)).size}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
