import React, { useState } from 'react'

export default function SearchPanel({ stateValue, cityValue, profile, maxPrice, states, cities, setState, setCity, setProfile, setMaxPrice, promptInput, setPromptInput, uiMode, setUiMode, onSearch, loading }) {
  const handlePreferenceChange = (value) => {
    setProfile(value)
  }

  return (
    <div>
      <section className="hero">
        <h1 className="hero-title">
          Find Your Perfect <span className="gradient-text">Nest</span>
        </h1>
        <p className="hero-subtitle">
          AI-powered rental recommendations tailored to your preferences, budget, and lifestyle. Discover homes that truly fit.
        </p>
      </section>

      <div className="form-container">
        {/* Mode Toggle */}
        <div className="mode-toggle">
          <button
            type="button"
            className={`mode-btn ${uiMode === 'form' ? 'active' : ''}`}
            onClick={() => setUiMode('form')}
          >
            💼 Form Search
          </button>
          <button
            type="button"
            className={`mode-btn ${uiMode === 'prompt' ? 'active' : ''}`}
            onClick={() => setUiMode('prompt')}
          >
            💬 Ask AI
          </button>
        </div>

        {uiMode === 'prompt' ? (
          <form className="form-grid" onSubmit={(e) => { e.preventDefault(); onSearch() }}>
            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
              <label className="form-label" htmlFor="promptSearch">Describe your ideal home</label>
              <textarea
                id="promptSearch"
                className="natural-search-input"
                placeholder="E.g., 'I'm looking for an affordable 2-bedroom apartment near parks in Austin, Texas under $1500/month' or 'Safe neighborhood in New York with good schools'"
                value={promptInput}
                onChange={(e) => setPromptInput(e.target.value)}
                rows="4"
              />
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ gridColumn: '1 / -1' }}>
              <span>{loading ? 'Finding homes...' : 'Search'}</span>
            </button>
          </form>
        ) : (
          <form className="form-grid" onSubmit={(e) => { e.preventDefault(); onSearch() }}>
            <div className="form-group">
              <label className="form-label" htmlFor="state">State</label>
              <div className="input-wrapper">
                <select id="state" value={stateValue} onChange={(e) => { setState(e.target.value); setCity('') }} required>
                  <option value="">Select your state</option>
                  {states.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="city">City</label>
              <div className="input-wrapper">
                <select id="city" value={cityValue} onChange={(e) => setCity(e.target.value)} disabled={!stateValue} required>
                  <option value="">Select your city</option>
                  {stateValue && cities[stateValue].map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Your Preference</label>
              <div className="preference-selector">
                <label className={`preference-card ${profile === 'cheap_but_safe' ? 'selected' : ''}`}>
                  <input type="radio" name="profile" value="cheap_but_safe" checked={profile === 'cheap_but_safe'} onChange={(e) => handlePreferenceChange(e.target.value)} required />
                  <div className="preference-content">
                    <div className="preference-title">💰 Budget Smart</div>
                    <div className="preference-desc">Affordable options without compromising safety</div>
                  </div>
                  <div className="check-indicator"></div>
                </label>

                <label className={`preference-card ${profile === 'balanced' ? 'selected' : ''}`}>
                  <input type="radio" name="profile" value="balanced" checked={profile === 'balanced'} onChange={(e) => handlePreferenceChange(e.target.value)} required />
                  <div className="preference-content">
                    <div className="preference-title">⚖️ Balanced</div>
                    <div className="preference-desc">Best mix of price, location, and amenities</div>
                  </div>
                  <div className="check-indicator"></div>
                </label>

                <label className={`preference-card ${profile === 'premium' ? 'selected' : ''}`}>
                  <input type="radio" name="profile" value="premium" checked={profile === 'premium'} onChange={(e) => handlePreferenceChange(e.target.value)} required />
                  <div className="preference-content">
                    <div className="preference-title">✨ Premium</div>
                    <div className="preference-desc">Top-tier locations and luxury amenities</div>
                  </div>
                  <div className="check-indicator"></div>
                </label>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="maxPrice">Maximum Budget ($/month)</label>
              <div className="input-wrapper">
                <input type="number" id="maxPrice" value={maxPrice} onChange={(e) => setMaxPrice(Number(e.target.value))} placeholder="e.g., 1500" min="100" step="100" required />
              </div>
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ gridColumn: '1 / -1' }}>
              <span>{loading ? 'Finding your perfect match...' : 'Discover Your Perfect Home'}</span>
            </button>
          </form>
        )}
      </div>
    </div>
  )
}
