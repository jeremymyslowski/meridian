import { Link, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Layout.css'

export default function Layout() {
  const { user, logout } = useAuth()

  return (
    <div className="layout">
      <header className="layout-header">
        <Link to="/" className="layout-brand">Meridian</Link>
        <div className="layout-user">
          <span>{user?.name}</span>
          <button type="button" onClick={logout} className="btn-secondary">
            Log out
          </button>
        </div>
      </header>
      <main className="layout-main">
        <Outlet />
      </main>
    </div>
  )
}