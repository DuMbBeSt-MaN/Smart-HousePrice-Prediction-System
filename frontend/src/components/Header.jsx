import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './header.css'

export default function Header() {
  const navigate = useNavigate()
  const { logout } = useAuth()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  return (
    <header>
      <div className="container">
        <div className="header-wrapper">
          <Link to="/search" className="logo">
            HomeFinder
          </Link>
          <div className="header-actions">
            <Link to="/home" className="nav-link">
              Home
            </Link>
            <button className="logout-btn-small" onClick={handleLogout}>
              Logout
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}
