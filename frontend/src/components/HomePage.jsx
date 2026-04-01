import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import './HomePage.css'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } }
}

const scrollItemVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: 'easeOut' } }
}

const ScrollRevealItem = ({ children }) => {
  const [isVisible, setIsVisible] = useState(false)
  const [ref, setRef] = useState(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
        }
      },
      { threshold: 0.1 }
    )

    if (ref) observer.observe(ref)
    return () => {
      if (ref) observer.unobserve(ref)
    }
  }, [ref])

  return (
    <motion.div
      ref={setRef}
      initial="hidden"
      animate={isVisible ? 'visible' : 'hidden'}
      variants={scrollItemVariants}
    >
      {children}
    </motion.div>
  )
}

export default function HomePage() {
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({
        x: (e.clientX / window.innerWidth) * 10,
        y: (e.clientY / window.innerHeight) * 10
      })
    }

    window.addEventListener('mousemove', handleMouseMove)
    return () => window.removeEventListener('mousemove', handleMouseMove)
  }, [])

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const handleStartSearching = () => {
    navigate('/search')
  }

  return (
    <div className="home-page">
      {/* Animated Background Gradient */}
      <div className="home-bg-gradient" style={{ transform: `translate(${mousePosition.x}px, ${mousePosition.y}px)` }} />

      {/* Header */}
      <motion.header className="home-header" initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="header-content">
          <h1 className="header-logo">
            <span className="gradient-text">HomeFinder</span>
          </h1>
          <div className="header-actions">
            {user && <span className="user-greeting">Welcome, {user.name || user.email}!</span>}
            <motion.button
              className="logout-btn"
              onClick={handleLogout}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Logout
            </motion.button>
          </div>
        </div>
      </motion.header>

      {/* Hero Section */}
      <motion.section className="hero-section" variants={containerVariants} initial="hidden" animate="visible">
        <motion.div className="hero-content" variants={itemVariants}>
          <h2 className="hero-title">
            Find Your <span className="gradient-text">Perfect Home</span>
          </h2>
          <p className="hero-description">
            Discover the best property deals in Chennai, Bangalore, Mumbai, and Delhi. Our AI-powered recommendation engine helps you find homes that match your lifestyle and budget.
          </p>

          <motion.button
            className="cta-button"
            onClick={handleStartSearching}
            whileHover={{ scale: 1.05, boxShadow: '0 20px 40px rgba(212, 175, 55, 0.3)' }}
            whileTap={{ scale: 0.95 }}
            variants={itemVariants}
          >
            Start Searching
          </motion.button>
        </motion.div>

        {/* Floating Cards */}
        <motion.div className="floating-cards" variants={containerVariants}>
          {[
            { icon: '📊', title: 'AI Recommendations', desc: 'Get personalized property suggestions' },
            { icon: '💰', title: 'Best Prices', desc: 'Find great deals within your budget' },
            { icon: '🗺️', title: 'Multiple Cities', desc: 'Search across major Indian cities' }
          ].map((card, idx) => (
            <motion.div
              key={idx}
              className="floating-card"
              variants={itemVariants}
              whileHover={{ y: -10, scale: 1.05 }}
              transition={{ type: 'spring', stiffness: 300, damping: 10 }}
            >
              <div className="card-icon">{card.icon}</div>
              <h3>{card.title}</h3>
              <p>{card.desc}</p>
            </motion.div>
          ))}
        </motion.div>
      </motion.section>

      {/* Features Section */}
      <section className="features-section">
        <ScrollRevealItem>
          <div className="section-header">
            <h2>Why Choose HomeFinder?</h2>
            <p>Everything you need to find your perfect home</p>
          </div>
        </ScrollRevealItem>

        <div className="features-grid">
          {[
            {
              icon: '🤖',
              title: 'Intelligent Matching',
              description: 'Our AI analyzes your preferences to recommend properties that truly fit your needs and lifestyle.'
            },
            {
              icon: '🔍',
              title: 'Comprehensive Search',
              description: 'Browse through thousands of properties with advanced filtering options to narrow down your choices.'
            },
            {
              icon: '💬',
              title: 'Easy Communication',
              description: 'Connect directly with sellers and agents to inquire about properties and schedule viewings.'
            },
            {
              icon: '📱',
              title: 'Mobile Friendly',
              description: 'Search for homes on the go with our responsive mobile app experience.'
            },
            {
              icon: '🛡️',
              title: 'Trusted & Secure',
              description: 'All properties are verified and your data is protected with enterprise-grade security.'
            },
            {
              icon: '📊',
              title: 'Market Insights',
              description: 'Get detailed price analysis, market trends, and neighborhood information for informed decisions.'
            }
          ].map((feature, idx) => (
            <ScrollRevealItem key={idx}>
              <motion.div
                className="feature-card"
                whileHover={{
                  y: -10,
                  boxShadow: '0 20px 40px rgba(212, 175, 55, 0.2)',
                  borderColor: 'var(--accent-gold)'
                }}
                transition={{ duration: 0.3 }}
              >
                <div className="feature-icon">{feature.icon}</div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </motion.div>
            </ScrollRevealItem>
          ))}
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works">
        <ScrollRevealItem>
          <div className="section-header">
            <h2>How It Works</h2>
            <p>Three simple steps to find your dream home</p>
          </div>
        </ScrollRevealItem>

        <div className="steps-container">
          {[
            {
              number: '01',
              title: 'Create Your Profile',
              description: 'Tell us about your preferences, budget, and lifestyle needs.'
            },
            {
              number: '02',
              title: 'Get Recommendations',
              description: 'Our AI analyzes properties and recommends the best matches for you.'
            },
            {
              number: '03',
              title: 'Schedule & Visit',
              description: 'View properties and connect with sellers to schedule site visits.'
            }
          ].map((step, idx) => (
            <ScrollRevealItem key={idx}>
              <motion.div
                className="step-card"
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3 }}
              >
                <div className="step-number">{step.number}</div>
                <h3>{step.title}</h3>
                <p>{step.description}</p>
              </motion.div>
            </ScrollRevealItem>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <ScrollRevealItem>
        <section className="final-cta">
          <motion.div className="cta-content" variants={containerVariants}>
            <motion.h2 variants={itemVariants}>Ready to Find Your Perfect Home?</motion.h2>
            <motion.p variants={itemVariants}>
              Join thousands of happy homeowners who found their dream properties with HomeFinder.
            </motion.p>
            <motion.button
              className="cta-button large"
              onClick={handleStartSearching}
              whileHover={{ scale: 1.08, boxShadow: '0 25px 50px rgba(212, 175, 55, 0.4)' }}
              whileTap={{ scale: 0.95 }}
              variants={itemVariants}
            >
              Start Your Journey Now
            </motion.button>
          </motion.div>
        </section>
      </ScrollRevealItem>

      {/* Footer */}
      <footer className="home-footer">
        <p>&copy; 2024 HomeFinder. All rights reserved.</p>
      </footer>
    </div>
  )
}
