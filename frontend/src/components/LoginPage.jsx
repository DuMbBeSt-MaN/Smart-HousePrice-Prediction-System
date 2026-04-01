import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { GoogleLogin } from '@react-oauth/google'
import { useAuth } from '../context/AuthContext'
import DynamicBackground from './DynamicBackground'
import './LoginPage.css'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } }
}

const buttonVariants = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.6 } }
}

export default function LoginPage() {
  const navigate = useNavigate()
  const { loginWithGoogle, loginWithEmail } = useAuth()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [isEmailPending, setIsEmailPending] = useState(false)

  const handleGoogleSuccess = (credentialResponse) => {
    try {
      // Decode JWT token to get user info
      const base64Url = credentialResponse.credential.split('.')[1]
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
      const jsonPayload = decodeURIComponent(atob(base64).split('').map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''))
      const userData = JSON.parse(jsonPayload)
      loginWithGoogle(userData)
      navigate('/home')
    } catch (error) {
      console.error('Google login error:', error)
    }
  }

  const handleEmailLogin = async (e) => {
    e.preventDefault()
    if (email && password) {
      setIsEmailPending(true)
      // Simulate API call
      setTimeout(() => {
        loginWithEmail(email, password)
        navigate('/home')
        setIsEmailPending(false)
      }, 1000)
    }
  }

  return (
    <div className="login-page">
      <DynamicBackground />
      
      <motion.div className="login-container" variants={containerVariants} initial="hidden" animate="visible">
        {/* Logo */}
        <motion.div className="login-logo" variants={itemVariants}>
          <h1>
            <span className="gradient-text">HomeFinder</span>
          </h1>
          <p>Discover Your Dream Home</p>
        </motion.div>

        {/* Login Card */}
        <motion.div className="login-card" variants={itemVariants} whileHover={{ scale: 1.02 }} transition={{ duration: 0.3 }}>
          <h2>Welcome Back</h2>
          <p className="login-subtitle">Sign in to your account or create a new one</p>

          {/* Google Login */}
          <motion.div className="auth-option" variants={itemVariants}>
            <div className="google-login-wrapper">
              <GoogleLogin
                onSuccess={handleGoogleSuccess}
                onError={() => console.log('Login Failed')}
                theme="dark"
                width="340"
              />
            </div>
          </motion.div>

          {/* Divider */}
          <motion.div className="divider" variants={itemVariants}>
            <span>or</span>
          </motion.div>

          {/* Email Login Form */}
          <motion.form onSubmit={handleEmailLogin} variants={itemVariants}>
            <div className="form-group">
              <label htmlFor="email">Email Address</label>
              <input
                type="email"
                id="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Password</label>
              <div className="password-input-wrapper">
                <input
                  type={showPassword ? 'text' : 'password'}
                  id="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? '👁️' : '👁️‍🗨️'}
                </button>
              </div>
            </div>

            <motion.button
              type="submit"
              className="login-button"
              disabled={isEmailPending}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {isEmailPending ? 'Logging in...' : 'Sign In'}
            </motion.button>
          </motion.form>

          <p className="signup-text">
            Don't have an account? <span>Create one</span>
          </p>
        </motion.div>

        {/* Features */}
        <motion.div className="features" variants={containerVariants}>
          {[
            { icon: '🏠', title: 'Find Perfect Home', desc: 'Browse thousands of properties' },
            { icon: '💰', title: 'Best Prices', desc: 'Get the best deals in market' },
            { icon: '📍', title: 'Multiple Locations', desc: 'Search across all major cities' }
          ].map((feature, idx) => (
            <motion.div key={idx} className="feature-item" variants={itemVariants} whileHover={{ y: -5 }}>
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </motion.div>
    </div>
  )
}
