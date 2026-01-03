import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Suspense, lazy } from 'react'
import './App.css'

// Lazy load kompomenty
const Dashboard = lazy(() => import('./components/Dashboard'))
const AdminPanel = lazy(() => import('./components/AdminPanel'))
const JobsList = lazy(() => import('./components/JobsList'))
const CandidateProfile = lazy(() => import('./components/CandidateProfile'))
const MatchingEngine = lazy(() => import('./components/MatchingEngine'))
const InterviewScheduler = lazy(() => import('./components/InterviewScheduler'))
const NotFound = lazy(() => import('./components/NotFound'))

// Fallback Loading Component
const LoadingFallback = () => (
  <div style={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: 'sans-serif'
  }}>
    <div style={{ textAlign: 'center', color: 'white' }}>
      <h1>Loading...</h1>
      <p>MisMatch Recruiter Platform</p>
    </div>
  </div>
)

// Error Boundary Component
import React from 'react'
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          padding: '20px',
          textAlign: 'center',
          background: '#f8d7da',
          color: '#721c24'
        }}>
          <h1>Something went wrong</h1>
          <p>Please refresh the page</p>
        </div>
      )
    }

    return this.props.children
  }
}

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Suspense fallback={<LoadingFallback />}>
          <Routes>
            {/* CRITICAL: Root route */}
            <Route path="/" element={<Dashboard />} />
           
            {/* Main application routes */}
            <Route path="/jobs" element={<JobsList />} />
            <Route path="/candidates" element={<CandidateProfile />} />
            <Route path="/matching" element={<MatchingEngine />} />
            <Route path="/interviews" element={<InterviewScheduler />} />
           
            {/* Admin routes */}
            <Route path="/admin-dashboard" element={<AdminPanel />} />
            
            {/* 404 Fallback */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </Router>
    </ErrorBoundary>
  )
}

export default App