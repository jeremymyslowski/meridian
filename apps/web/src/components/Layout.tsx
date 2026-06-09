import { Link, Outlet } from 'react-router-dom'
import { Button } from '@meridian/ui-kit'
import { useAuth } from '../context/AuthContext'
import { useFeatureFlags } from '../hooks/useFeatureFlags'
import './Layout.css'

export default function Layout() {
  const { user, logout } = useAuth()
  const { isEnabled } = useFeatureFlags()

  return (
    <div className="layout">
      <header className="layout-header">
        <div className="layout-nav">
          <Link to="/" className="layout-brand">Meridian</Link>
          {isEnabled('analytics_dashboard') && (
            <Link to="/analytics" className="layout-nav-link">Analytics</Link>
          )}
        </div>
        <div className="layout-user">
          <span>{user?.name}</span>
          <Button variant="secondary" onClick={logout}>
            Log out
          </Button>
        </div>
      </header>
      <main className="layout-main">
        <Outlet />
      </main>
    </div>
  )
}