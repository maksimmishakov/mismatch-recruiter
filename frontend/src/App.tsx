import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MainLayout from '@components/layout/MainLayout'
import DashboardPage from '@pages/DashboardPage'
import CandidatesPage from '@pages/CandidatesPage'
import JobsPage from '@pages/JobsPage'
import MatchesPage from '@pages/MatchesPage'
import NotFoundPage from '@pages/NotFoundPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/candidates" element={<CandidatesPage />} />
          <Route path="/jobs" element={<JobsPage />} />
          <Route path="/matches" element={<MatchesPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
