import React from 'react'

function Skeleton() {
  return (
    <div className="skeleton">
      <div className="s-row"></div>
      <div className="s-row short"></div>
    </div>
  )
}

export default function ResultsPanel({ results, loading, error }) {
  const handleCardClick = (url) => {
    if (url) {
      window.open(url, '_blank')
    }
  }

  return (
    <div>
      {error && <div className="error">{error}</div>}

      {loading && (
        <div className="loading active">
          <div className="spinner"></div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '1.125rem' }}>Finding your perfect match...</p>
        </div>
      )}

      {!loading && (
        <section className={`results-section ${results ? 'active' : ''}`}>
          <div className="results-header">
            <h2 className="results-title">Your Personalized Matches</h2>
            <p className="results-subtitle" id="resultsCount">
              {results && results.length > 0 
                ? `${results.length} perfect ${results.length === 1 ? 'match' : 'matches'} found for you`
                : 'AI-curated recommendations based on your preferences'}
            </p>
          </div>

          {results && results.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">🏠</div>
              <p>No matches found. Try adjusting your preferences.</p>
            </div>
          ) : (
            <div className="results-grid">
              {results && results.map((house, index) => {
                const score = house.final_score || house.score || 0
                // final_score is 0-1, so multiply by 100 and clamp to 0-100
                const scorePercent = Math.min(100, Math.max(0, score * 100))
                const beds = house.beds || house.bedrooms || 2
                const sqft = house.sqft || house.area_sqft || 850
                const price = house.price || 0
                const imageUrl = house.image || null

                return (
                  <div
                    key={house.external_id || house.house_id || index}
                    className="result-card"
                    onClick={() => handleCardClick(imageUrl ? house.url : null)}
                    style={{ cursor: house.url ? 'pointer' : 'default' }}
                  >
                    <div className="result-image">
                      {imageUrl ? (
                        <img src={imageUrl} alt={house.address} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                      ) : (
                        <span>🏡</span>
                      )}
                    </div>
                    <div className="result-content">
                      {index === 0 && <span className="result-badge">Best Match</span>}
                      <div className="result-price">₹{house.price_display ? house.price_display.replace('Rs. ', '').replace('/month', '') : price.toLocaleString('en-IN')}<span style={{ fontSize: '1rem', color: 'var(--text-muted)', fontFamily: "'DM Sans', sans-serif" }}>/month</span></div>
                      
                      <div className="result-details">
                        <div className="detail-item">
                          <span className="detail-icon">🛏️</span>
                          <span>{beds} BHK</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-icon">📐</span>
                          <span>{sqft} sqft</span>
                        </div>
                        <div className="detail-item">
                          <span className="detail-icon">📍</span>
                          <span>{house.city}, {house.state}</span>
                        </div>
                      </div>

                      <div className="result-score">
                        <div className="score-bar">
                          <div className="score-fill" style={{ width: `${scorePercent}%` }}></div>
                        </div>
                        <div className="score-value">{scorePercent.toFixed(0)}%</div>
                      </div>

                      <p className="result-explanation">{house.explanation || `${house.address}, ${house.city}, ${house.state}`}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </section>
      )}
    </div>
  )
}
