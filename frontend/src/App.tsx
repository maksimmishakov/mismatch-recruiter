import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Dashboard } from './pages/Dashboard';
import { ResumesPage } from './pages/Resumes';

import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="navbar bg-blue-600 text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold flex items-center gap-2">
              🎯 MisMatch
            </Link>
            <div className="flex gap-4">
              <Link 
                to="/" 
                className="px-4 py-2 rounded-lg hover:bg-blue-700 transition font-semibold"
              >
                Dashboard
              </Link>
              <Link 
                to="/resumes" 
                className="px-4 py-2 rounded-lg hover:bg-blue-700 transition font-semibold"
              >
                Resumes
              </Link>
            </div>
          </div>
        </nav>

        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/resumes" element={<ResumesPage />} />
          </Routes>
        </main>

        <footer className="bg-gray-800 text-gray-300 py-6 text-center text-sm">
          <p>© 2026 MisMatch Recruitment Platform | Days 16-17 Implementation</p>
        </footer>
      </div>
    </BrowserRouter>
  );
}

export default App;
