import React from 'react';
import { Resume } from '../../services/api';

interface ParsedResumeProps {
  resume: Resume;
  onRunMatching?: () => void;
  onDelete?: () => void;
}

export const ParsedResume: React.FC<ParsedResumeProps> = ({
  resume,
  onRunMatching,
  onDelete,
}) => {
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.9) return 'text-green-600 bg-green-50';
    if (confidence >= 0.7) return 'text-yellow-600 bg-yellow-50';
    return 'text-red-600 bg-red-50';
  };

  const getConfidenceBadge = (confidence: number) => {
    if (confidence >= 0.9) return '✅';
    if (confidence >= 0.7) return '⚠️';
    return '❌';
  };

  return (
    <div className="bg-white rounded-lg shadow p-6 mb-4 border-l-4 border-green-500">
      <div className="grid grid-cols-3 gap-6 mb-6">
        <div>
          <h3 className="text-lg font-bold text-gray-900">{resume.fullName}</h3>
          <p className="text-gray-600 mt-1">{resume.currentJobTitle}</p>
          <p className="text-sm text-gray-500 mt-3">📧 {resume.email}</p>
          {resume.phone && (
            <p className="text-sm text-gray-500">📱 {resume.phone}</p>
          )}
          {resume.location && (
            <p className="text-sm text-gray-500">📍 {resume.location}</p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
            <div className="text-xs text-gray-600">Experience</div>
            <div className="text-3xl font-bold text-blue-600 mt-2">
              {resume.yearsExperience}
            </div>
            <div className="text-xs text-gray-500">years</div>
          </div>

          <div className={`rounded-lg p-4 border ${getConfidenceColor(resume.confidence)}`}>
            <div className="text-xs text-gray-600">Parsing</div>
            <div className="text-3xl font-bold mt-2">
              {getConfidenceBadge(resume.confidence)}
            </div>
            <div className="text-xs">
              {Math.round(resume.confidence * 100)}% confident
            </div>
          </div>
        </div>

        <div className="bg-gray-50 rounded-lg p-4">
          <div className="text-xs text-gray-600 mb-2">Uploaded File</div>
          <p className="text-sm font-semibold text-gray-900 truncate">
            {resume.filename}
          </p>
          <p className="text-xs text-gray-500 mt-1">ID: {resume.id}</p>
          {resume.uploadedAt && (
            <p className="text-xs text-gray-500">
              {new Date(resume.uploadedAt).toLocaleDateString()}
            </p>
          )}
        </div>
      </div>

      {resume.skills.length > 0 && (
        <div className="mb-6">
          <h4 className="font-semibold text-gray-900 mb-3">🛠️ Detected Skills</h4>
          <div className="flex flex-wrap gap-2">
            {resume.skills.map((skill) => (
              <span
                key={skill}
                className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="flex gap-3 pt-4 border-t">
        {onRunMatching && (
          <button
            onClick={onRunMatching}
            className="flex-1 bg-green-500 hover:bg-green-600 text-white py-2 rounded-lg font-semibold transition"
          >
            🎯 Run Matching
          </button>
        )}

        <button className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-lg font-semibold transition">
          👁️ View Full Resume
        </button>

        {onDelete && (
          <button
            onClick={onDelete}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold transition"
          >
            🗑️ Delete
          </button>
        )}
      </div>
    </div>
  );
};
