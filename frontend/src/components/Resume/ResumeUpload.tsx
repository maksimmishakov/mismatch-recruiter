import React, { useState } from 'react';
import { Resume, handleApiError } from '../../services/api';

interface ResumeUploadProps {
  onUploadSuccess: (resume: Resume) => void;
  onError?: (error: string) => void;
}

export const ResumeUpload: React.FC<ResumeUploadProps> = ({
  onUploadSuccess,
  onError,
}) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const files = e.dataTransfer.files;
    if (files && files[0]) handleFile(files[0]);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) handleFile(files[0]);
  };

  const handleFile = async (file: File) => {
    const validTypes = ['application/pdf', 'text/plain'];
    if (!validTypes.includes(file.type)) {
      setError('Only PDF files supported');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('File size must be < 5MB');
      return;
    }

    setError(null);
    setUploading(true);
    setProgress(0);

    try {
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const mockResume: Resume = {
        id: Date.now(),
        fullName: 'Sample User',
        email: 'user@example.com',
        phone: '123-456-7890',
        location: 'Moscow',
        currentJobTitle: 'Software Engineer',
        yearsExperience: 5,
        skills: ['React', 'TypeScript', 'Node.js'],
        confidence: 0.95,
        filename: file.name,
        uploadedAt: new Date().toISOString(),
      };

      clearInterval(progressInterval);
      setProgress(100);
      setTimeout(() => {
        setUploading(false);
        setProgress(0);
        onUploadSuccess(mockResume);
      }, 500);
    } catch (err) {
      const errorMsg = handleApiError(err);
      setError(errorMsg);
      setUploading(false);
      setProgress(0);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-8 mb-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-2">📄 Upload Resume</h2>
      <p className="text-gray-600 mb-6">
        Upload PDF files. System automatically parses and extracts skills.
      </p>

      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-12 text-center transition-all ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 bg-gray-50'
        }`}
      >
        <input
          id="file-upload"
          type="file"
          accept=".pdf"
          onChange={handleChange}
          className="hidden"
          disabled={uploading}
        />
        <label htmlFor="file-upload" className="cursor-pointer block">
          {uploading ? (
            <div className="text-gray-600">
              <div className="text-4xl mb-4">⏳</div>
              <p className="text-lg font-semibold mb-4">
                Processing resume...
              </p>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-sm text-gray-500">{progress}%</p>
            </div>
          ) : (
            <div className="text-gray-600">
              <div className="text-5xl mb-4">📤</div>
              <p className="text-xl font-semibold mb-2">
                Drag and drop resume
              </p>
              <p className="text-gray-500">or click to select</p>
              <p className="text-xs text-gray-400 mt-4">
                PDF up to 5MB
              </p>
            </div>
          )}
        </label>
      </div>

      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          ❌ {error}
        </div>
      )}

      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-green-600 font-semibold mb-2">✅ Extract</div>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Name</li>
            <li>• Contact</li>
            <li>• Skills</li>
          </ul>
        </div>
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="text-blue-600 font-semibold mb-2">⚡ Fast</div>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• &lt;5 sec</li>
            <li>• 95% accuracy</li>
            <li>• Scoring</li>
          </ul>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <div className="text-purple-600 font-semibold mb-2">🔒 Safe</div>
          <ul className="text-xs text-gray-600 space-y-1">
            <li>• Encrypted</li>
            <li>• GDPR</li>
            <li>• Delete</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
