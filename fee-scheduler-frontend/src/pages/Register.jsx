import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Alert, Input, Btn } from '../components/UI'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const set = k => e => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async () => {
    setError(''); setLoading(true)
    try {
      await register(form.email, form.username, form.password)
      navigate('/login')
    } catch (e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div style={{ minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center', background:'var(--bg-base)' }}>
      <div className="fade-up" style={{ background:'var(--bg-surface)', border:'1px solid var(--border-bright)', borderRadius:16, padding:'40px 44px', width:'100%', maxWidth:400 }}>
        <div style={{ marginBottom:28, textAlign:'center' }}>
          <div style={{ fontFamily:'var(--font-display)', fontSize:26, color:'var(--gold-text)', marginBottom:4 }}>Create Account</div>
          <div style={{ color:'var(--text-muted)', fontSize:13 }}>FeeScheduler Admin</div>
        </div>
        <Alert msg={error} />
        <div style={{ display:'flex', flexDirection:'column', gap:14, marginBottom:22 }}>
          <Input label="Email" type="email" value={form.email} onChange={set('email')} />
          <Input label="Username" value={form.username} onChange={set('username')} />
          <Input label="Password" type="password" value={form.password} onChange={set('password')} />
        </div>
        <Btn onClick={handleSubmit} loading={loading} style={{ width:'100%', justifyContent:'center', padding:11 }}>Register</Btn>
        <div style={{ textAlign:'center', marginTop:18, color:'var(--text-muted)', fontSize:13 }}>
          Have an account? <Link to="/login" style={{ color:'var(--gold-text)' }}>Sign in</Link>
        </div>
      </div>
    </div>
  )
}
