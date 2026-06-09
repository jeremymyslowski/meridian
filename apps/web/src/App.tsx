import { Navigate, Route, Routes } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import { useFeatureFlags } from './hooks/useFeatureFlags'
import LoginPage from './pages/LoginPage'
import ProjectsPage from './pages/ProjectsPage'
import TaskBoardPage from './pages/TaskBoardPage'
import TaskListPage from './pages/TaskListPage'
import TaskDetailPage from './pages/TaskDetailPage'
import AnalyticsPage from './pages/AnalyticsPage'
import Layout from './components/Layout'

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return <>{children}</>
}

function AnalyticsRoute() {
  const { isEnabled } = useFeatureFlags()
  if (!isEnabled('analytics_dashboard')) return <Navigate to="/" replace />
  return <AnalyticsPage />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<ProjectsPage />} />
        <Route path="analytics" element={<AnalyticsRoute />} />
        <Route path="projects/:projectId" element={<TaskBoardPage />} />
        <Route path="projects/:projectId/list" element={<TaskListPage />} />
        <Route path="tasks/:taskId" element={<TaskDetailPage />} />
      </Route>
    </Routes>
  )
}