import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Alert, Input, Btn } from '../components/UI'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async () => {
    setError('')
    setLoading(true)
    try {
      await login(form.email, form.password)
      navigate('/dashboard')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'var(--bg-base)',
    }}>
      {/* Background grid */}
      <div style={{
        position: 'fixed', inset: 0, zIndex: 0,
        backgroundImage: `
          linear-gradient(var(--border) 1px, transparent 1px),
          linear-gradient(90deg, var(--border) 1px, transparent 1px)
        `,
        backgroundSize: '40px 40px',
        opacity: 0.3,
      }} />

      <div className="fade-up" style={{
        position: 'relative', zIndex: 1,
        background: 'var(--bg-surface)',
        border: '1px solid var(--border-bright)',
        borderRadius: 16,
        padding: '40px 44px',
        width: '100%', maxWidth: 400,
      }}>
        <div style={{ marginBottom: 32, textAlign: 'center' }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 28, color: 'var(--gold-text)', marginBottom: 6 }}>
            FeeScheduler
          </div>
          <div style={{ color: 'var(--text-muted)', fontSize: 13 }}>Sign in to your account</div>
        </div>

        <Alert msg={error} />

        <div style={{ display: 'flex', flexDirection: 'column', gap: 16, marginBottom: 24 }}>
          <Input
            label="Email"
            type="email"
            placeholder="admin@school.com"
            value={form.email}
            onChange={set('email')}
            onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          />
          <Input
            label="Password"
            type="password"
            placeholder="••••••••"
            value={form.password}
            onChange={set('password')}
            onKeyDown={e => e.key === 'Enter' && handleSubmit()}
          />
        </div>

        <Btn
          onClick={handleSubmit}
          loading={loading}
          style={{ width: '100%', justifyContent: 'center', padding: '11px' }}
        >
          Sign In
        </Btn>

        <div style={{ textAlign: 'center', marginTop: 20, color: 'var(--text-muted)', fontSize: 13 }}>
          No account?{' '}
          <Link to="/register" style={{ color: 'var(--gold-text)' }}>Register</Link>
        </div>
      </div>
    </div>
  )
}
