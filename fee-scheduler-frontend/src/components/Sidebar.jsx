import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const nav = [
  { to: '/dashboard',  label: 'Dashboard',  icon: '▦' },
  { to: '/students',   label: 'Students',   icon: '◎' },
  { to: '/teachers',   label: 'Teachers',   icon: '◈' },
  { to: '/fees',       label: 'Fees',       icon: '◇' },
  { to: '/payroll',    label: 'Payroll',    icon: '◆' },
  { to: '/reminders',  label: 'Reminders',  icon: '◉' },
  { to: '/reports',    label: 'Reports',    icon: '▤' },
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  return (
    <aside style={{
      width: 'var(--sidebar-w)',
      background: 'var(--bg-surface)',
      borderRight: '1px solid var(--border)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'fixed',
      top: 0, left: 0,
      zIndex: 100,
    }}>
      {/* Logo */}
      <div style={{
        padding: '20px 20px 16px',
        borderBottom: '1px solid var(--border)',
      }}>
        <div style={{ fontFamily: 'var(--font-display)', fontSize: 20, color: 'var(--gold-text)', letterSpacing: '-0.02em' }}>
          Fee<span style={{ color: 'var(--text-muted)' }}>Scheduler</span>
        </div>
        <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2, letterSpacing: '0.1em', textTransform: 'uppercase' }}>
          Finance & Payroll
        </div>
      </div>

      {/* Nav */}
      <nav style={{ flex: 1, padding: '12px 10px', overflowY: 'auto' }}>
        {nav.map(({ to, label, icon }) => (
          <NavLink key={to} to={to} style={({ isActive }) => ({
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '9px 10px', borderRadius: 'var(--radius)',
            marginBottom: 2,
            color: isActive ? 'var(--gold-text)' : 'var(--text-secondary)',
            background: isActive ? 'var(--gold-glow)' : 'transparent',
            fontWeight: isActive ? 600 : 400,
            fontSize: 13,
            transition: 'all 0.15s',
            textDecoration: 'none',
          })}
            onMouseEnter={e => { if (!e.currentTarget.classList.contains('active')) e.currentTarget.style.background = 'var(--bg-elevated)' }}
            onMouseLeave={e => { e.currentTarget.style.background = '' }}>
            <span style={{ fontSize: 14, opacity: 0.8 }}>{icon}</span>
            {label}
          </NavLink>
        ))}
      </nav>

      {/* User */}
      <div style={{
        padding: '14px 16px',
        borderTop: '1px solid var(--border)',
      }}>
        <div style={{ fontSize: 12, color: 'var(--text-muted)', marginBottom: 4 }}>Signed in as</div>
        <div style={{ fontSize: 13, color: 'var(--text-primary)', marginBottom: 10, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {user?.email}
        </div>
        <button onClick={handleLogout} style={{
          width: '100%', padding: '7px 0',
          background: 'var(--bg-elevated)',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius)',
          color: 'var(--text-muted)',
          fontSize: 12, fontWeight: 600,
          letterSpacing: '0.04em',
          cursor: 'pointer',
          transition: 'color 0.15s',
        }}
          onMouseEnter={e => e.target.style.color = 'var(--red)'}
          onMouseLeave={e => e.target.style.color = 'var(--text-muted)'}>
          Sign Out
        </button>
      </div>
    </aside>
  )
}
