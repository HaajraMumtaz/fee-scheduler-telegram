import { createContext, useContext, useState, useEffect } from 'react'
import { api } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/auth/me')
      .then(d => setUser(d))
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  const login = async (email, password) => {
    await api.post('/auth/login', { email, password })
    const me = await api.get('/auth/me')
    setUser(me)
  }

  const logout = async () => {
    await api.post('/auth/logout', {})
    setUser(null)
  }

  const register = async (email, username, password) => {
    return api.post('/auth/register', { email, username, password })
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, register }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
