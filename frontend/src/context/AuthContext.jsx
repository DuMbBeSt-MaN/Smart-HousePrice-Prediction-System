import { createContext, useContext, useState } from 'react'

const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  const loginWithGoogle = (googleUser) => {
    const userData = {
      id: googleUser.sub,
      name: googleUser.name,
      email: googleUser.email,
      picture: googleUser.picture,
      provider: 'google'
    }
    setUser(userData)
    setIsAuthenticated(true)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const loginWithEmail = (email, password) => {
    // In a real app, this would call an API
    const userData = {
      id: Date.now().toString(),
      email,
      provider: 'email'
    }
    setUser(userData)
    setIsAuthenticated(true)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    setIsAuthenticated(false)
    localStorage.removeItem('user')
  }

  const initializeAuth = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      const userData = JSON.parse(storedUser)
      setUser(userData)
      setIsAuthenticated(true)
    }
  }

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, loginWithGoogle, loginWithEmail, logout, initializeAuth }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
