import React, { useState } from 'react';
import { Upload, CheckCircle, AlertCircle, Loader } from 'lucide-react';

interface UploadResponse {
  success: boolean;
  message: string;
  resume_id?: string;
  data?: {
    name: string;
    email: string;
    phone: string;
    skills: string[];
    experience_years: number;
  };
}

const UploadPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [response, setResponse] = useState<UploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const validateFile = (f: File): boolean => {
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!validTypes.includes(f.type)) {
      setError('Only PDF and Word documents are supported');
      return false;
    }
    if (f.size > maxSize) {
      setError('File size must be less than 5MB');
      return false;
    }
    return true;
  };

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
    if (files && files.length > 0) {
      const droppedFile = files[0];
      if (validateFile(droppedFile)) {
        setFile(droppedFile);
        setError(null);
      }
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const selectedFile = files[0];
      if (validateFile(selectedFile)) {
        setFile(selectedFile);
        setError(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      const data: UploadResponse = await res.json();

      if (res.ok && data.success) {
        setResponse(data);
        setFile(null);
      } else {
        setError(data.message || 'Upload failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload error occurred');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <Upload className="mx-auto h-12 w-12 text-blue-600 mb-4" />
            <h1 className="text-3xl font-bold text-gray-900">Upload Resume</h1>
            <p className="mt-2 text-gray-600">Upload your resume for intelligent matching with job opportunities</p>
          </div>

          {/* Upload Zone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition ${
              dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
            }`}
          >
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.doc,.docx"
              className="hidden"
              id="file-input"
              disabled={uploading}
            />
            <label htmlFor="file-input" className="cursor-pointer">
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg font-medium text-gray-900">
                Drag and drop your resume here
              </p>
              <p className="text-sm text-gray-500 mt-1">
                or click to browse (PDF, DOC, DOCX - max 5MB)
              </p>
            </label>
          </div>

          {/* Selected File Info */}
          {file && (
            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <p className="text-sm text-gray-700">
                <strong>Selected:</strong> {file.name}
              </p>
              <p className="text-sm text-gray-600">
                Size: {(file.size / 1024).toFixed(2)} KB
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
              <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Success Message */}
          {response && response.success && (
            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-start gap-3">
                <CheckCircle className="h-5 w-5 text-green-600 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium text-green-800">Resume uploaded successfully!</p>
                  {response.data && (
                    <div className="mt-3 text-sm text-green-700">
                      <p><strong>Name:</strong> {response.data.name}</p>
                      <p><strong>Email:</strong> {response.data.email}</p>
                      <p><strong>Experience:</strong> {response.data.experience_years} years</p>
                      <p><strong>Skills:</strong> {response.data.skills.join(', ')}</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Upload Button */}
          <div className="mt-8">
            <button
              onClick={handleUpload}
              disabled={!file || uploading}
              className={`w-full py-3 px-4 rounded-lg font-medium text-white transition flex items-center justify-center gap-2 ${
                file && !uploading
                  ? 'bg-blue-600 hover:bg-blue-700'
                  : 'bg-gray-400 cursor-not-allowed'
              }`}
            >
              {uploading ? (
                <>
                  <Loader className="h-5 w-5 animate-spin" />
                  Uploading...
                </>
              ) : (
                'Upload Resume'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;
