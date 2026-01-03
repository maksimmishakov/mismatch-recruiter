import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Download, Loader } from 'lucide-react';

interface BatchResult {
  total: number;
  successful: number;
  failed: number;
  processing: boolean;
  results: Array<{
    filename: string;
    status: 'success' | 'error';
    message: string;
  }>;
}

const BatchPage: React.FC = () => {
  const [batchFile, setBatchFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [batchResult, setBatchResult] = useState<BatchResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [uploadMode, setUploadMode] = useState<'csv' | 'zip'>('csv');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const validateBatchFile = (f: File): boolean => {
    const validTypes = {
      csv: 'text/csv',
      zip: 'application/zip',
    };

    if (uploadMode === 'csv' && f.type !== validTypes.csv) {
      setError('CSV file required for CSV mode');
      return false;
    }
    if (uploadMode === 'zip' && f.type !== validTypes.zip) {
      setError('ZIP file required for ZIP mode');
      return false;
    }
    return true;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      const selectedFile = files[0];
      if (validateBatchFile(selectedFile)) {
        setBatchFile(selectedFile);
        setError(null);
      }
    }
  };

  const handleBatchUpload = async () => {
    if (!batchFile) {
      setError('Please select a file to upload');
      return;
    }

    setProcessing(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', batchFile);
      formData.append('mode', uploadMode);

      const res = await fetch(`${API_URL}/api/batch-upload`, {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });

      const data = await res.json();

      if (res.ok) {
        setBatchResult(data);
        setBatchFile(null);
      } else {
        setError(data.message || 'Batch upload failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload error occurred');
    } finally {
      setProcessing(false);
    }
  };

  const downloadTemplate = () => {
    if (uploadMode === 'csv') {
      const csv = 'name,email,phone,skills,experience_years\nJohn Doe,john@example.com,+1234567890,Python;JavaScript,5';
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'batch_template.csv';
      a.click();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <FileText className="mx-auto h-12 w-12 text-purple-600 mb-4" />
            <h1 className="text-3xl font-bold text-gray-900">Batch Upload</h1>
            <p className="mt-2 text-gray-600">Upload multiple resumes at once using CSV or ZIP format</p>
          </div>

          {/* Mode Selection */}
          <div className="grid grid-cols-2 gap-4 mb-8">
            <button
              onClick={() => setUploadMode('csv')}
              className={`p-4 rounded-lg border-2 transition ${
                uploadMode === 'csv'
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <FileText className="h-6 w-6 mx-auto mb-2" />
              <p className="font-medium">CSV Upload</p>
              <p className="text-sm text-gray-600">Candidate data in CSV</p>
            </button>
            <button
              onClick={() => setUploadMode('zip')}
              className={`p-4 rounded-lg border-2 transition ${
                uploadMode === 'zip'
                  ? 'border-purple-500 bg-purple-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <Upload className="h-6 w-6 mx-auto mb-2" />
              <p className="font-medium">ZIP Upload</p>
              <p className="text-sm text-gray-600">Multiple resume files</p>
            </button>
          </div>

          {/* Template Download */}
          {uploadMode === 'csv' && (
            <div className="mb-6">
              <button
                onClick={downloadTemplate}
                className="inline-flex items-center gap-2 text-purple-600 hover:text-purple-700 font-medium"
              >
                <Download className="h-4 w-4" />
                Download CSV Template
              </button>
            </div>
          )}

          {/* Upload Zone */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
            <input
              type="file"
              onChange={handleFileChange}
              accept={uploadMode === 'csv' ? '.csv' : '.zip'}
              className="hidden"
              id="batch-file-input"
              disabled={processing}
            />
            <label htmlFor="batch-file-input" className="cursor-pointer">
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg font-medium text-gray-900">
                Drag and drop your {uploadMode.toUpperCase()} file here
              </p>
              <p className="text-sm text-gray-500 mt-1">or click to browse</p>
            </label>
          </div>

          {/* Selected File Info */}
          {batchFile && (
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg mb-6">
              <p className="text-sm text-gray-700">
                <strong>Selected:</strong> {batchFile.name}
              </p>
              <p className="text-sm text-gray-600">
                Size: {(batchFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3 mb-6">
              <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          {/* Results */}
          {batchResult && (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-6">
              <div className="grid grid-cols-3 gap-4 text-center mb-4">
                <div>
                  <p className="text-2xl font-bold text-blue-600">{batchResult.total}</p>
                  <p className="text-sm text-gray-600">Total Files</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-green-600">{batchResult.successful}</p>
                  <p className="text-sm text-gray-600">Successful</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-red-600">{batchResult.failed}</p>
                  <p className="text-sm text-gray-600">Failed</p>
                </div>
              </div>
              {batchResult.results.length > 0 && (
                <div className="mt-4 border-t pt-4">
                  <h3 className="font-medium text-gray-900 mb-2">Details:</h3>
                  <div className="max-h-64 overflow-y-auto space-y-2">
                    {batchResult.results.map((result, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        {result.status === 'success' ? (
                          <CheckCircle className="h-4 w-4 text-green-600 flex-shrink-0 mt-0.5" />
                        ) : (
                          <AlertCircle className="h-4 w-4 text-red-600 flex-shrink-0 mt-0.5" />
                        )}
                        <div>
                          <p className="font-medium text-gray-900">{result.filename}</p>
                          <p className="text-gray-600">{result.message}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Upload Button */}
          <button
            onClick={handleBatchUpload}
            disabled={!batchFile || processing}
            className={`w-full py-3 px-4 rounded-lg font-medium text-white transition flex items-center justify-center gap-2 ${
              batchFile && !processing
                ? 'bg-purple-600 hover:bg-purple-700'
                : 'bg-gray-400 cursor-not-allowed'
            }`}
          >
            {processing ? (
              <>
                <Loader className="h-5 w-5 animate-spin" />
                Processing...
              </>
            ) : (
              'Start Batch Upload'
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default BatchPage;
