import React, { useState, useEffect } from 'react';
import { jobsApi } from '../services/api';

interface Job {
  id: number;
  title: string;
  company_name: string;
  salary_min: number;
  salary_max: number;
  seniority_level: string;
  status: string;
}

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    loadJobs();
  }, []);

  const loadJobs = async () => {
    try {
      const data = await jobsApi.listJobs();
      setJobs(data);
    } catch (error) {
      console.error('Failed to load jobs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Job Postings</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Create Job
        </button>
      </div>

      {loading ? (
        <div className="text-center py-8">Loading jobs...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {jobs.map((job) => (
            <div key={job.id} className="border rounded-lg p-4 hover:shadow-lg transition">
              <h3 className="font-bold text-lg mb-2">{job.title}</h3>
              <p className="text-gray-600 mb-2">{job.company_name}</p>
              <div className="flex justify-between text-sm mb-2">
                <span className="text-green-600 font-semibold">${job.salary_min.toLocaleString()}</span>
                <span className="text-gray-500">{job.seniority_level}</span>
              </div>
              <span className={`inline-block px-2 py-1 text-xs rounded ${job.status === 'open' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                {job.status.toUpperCase()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
