import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import { Spinner } from './components/UI'

import Login     from './pages/Login'
import Register  from './pages/Register'
import Dashboard from './pages/Dashboard'
import Students  from './pages/Students'
import Teachers  from './pages/Teachers'
import Fees      from './pages/Fees'
import Payroll   from './pages/Payroll'
import Reminders from './pages/Reminders'
import Reports   from './pages/Reports'

function Protected({ children }) {
  const { user, loading } = useAuth()
  if (loading) return (
    <div style={{ minHeight:'100vh', display:'flex', alignItems:'center', justifyContent:'center' }}>
      <Spinner size={32} />
    </div>
  )
  return user ? <Layout>{children}</Layout> : <Navigate to="/login" replace />
}

function Public({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  return user ? <Navigate to="/dashboard" replace /> : children
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<Public><Login /></Public>} />
          <Route path="/register" element={<Public><Register /></Public>} />
          <Route path="/dashboard"  element={<Protected><Dashboard /></Protected>} />
          <Route path="/students"   element={<Protected><Students /></Protected>} />
          <Route path="/teachers"   element={<Protected><Teachers /></Protected>} />
          <Route path="/fees"       element={<Protected><Fees /></Protected>} />
          <Route path="/payroll"    element={<Protected><Payroll /></Protected>} />
          <Route path="/reminders"  element={<Protected><Reminders /></Protected>} />
          <Route path="/reports"    element={<Protected><Reports /></Protected>} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
