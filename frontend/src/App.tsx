import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import MainLayout from '@components/layout/MainLayout'
import DashboardPage from '@pages/DashboardPage'
import NotFoundPage from '@pages/NotFoundPage'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<DashboardPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
