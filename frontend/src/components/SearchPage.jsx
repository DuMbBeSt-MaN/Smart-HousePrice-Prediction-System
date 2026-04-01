import { useState } from 'react'
import Header from './Header'
import SearchPanel from './SearchPanel'
import ResultsPanel from './ResultsPanel'
import { recommendHouses, searchFromText } from '../api'
import './SearchPage.css'

const STATES = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina', 'Michigan', 'Virginia', 'Washington', 'Massachusetts', 'Tennessee', 'Arizona', 'Colorado', 'Minnesota', 'Missouri', 'Wisconsin', 'Maryland']

const CITIES = {
  'California': ['Los Angeles', 'San Francisco', 'San Diego', 'San Jose', 'Sacramento', 'Fresno', 'Long Beach'],
  'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio', 'Fort Worth', 'El Paso'],
  'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville', 'Fort Lauderdale'],
  'New York': ['New York City', 'Buffalo', 'Rochester', 'Yonkers'],
  'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown'],
  'Illinois': ['Chicago', 'Aurora', 'Rockford'],
  'Ohio': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo'],
  'Georgia': ['Atlanta', 'Savannah', 'Augusta'],
  'North Carolina': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'],
  'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor'],
  'Virginia': ['Richmond', 'Arlington', 'Alexandria'],
  'Washington': ['Seattle', 'Tacoma', 'Vancouver'],
  'Massachusetts': ['Boston', 'Cambridge', 'Worcester'],
  'Tennessee': ['Memphis', 'Nashville', 'Knoxville'],
  'Arizona': ['Phoenix', 'Tucson', 'Mesa'],
  'Colorado': ['Denver', 'Colorado Springs', 'Aurora'],
  'Minnesota': ['Minneapolis', 'St. Paul', 'Bloomington'],
  'Missouri': ['Kansas City', 'St. Louis', 'Springfield'],
  'Wisconsin': ['Milwaukee', 'Madison', 'Green Bay'],
  'Maryland': ['Baltimore', 'Annapolis', 'Silver Spring']
}

export default function SearchPage() {
  const [state, setState] = useState('')
  const [city, setCity] = useState('')
  const [profile, setProfile] = useState('balanced')
  const [maxPrice, setMaxPrice] = useState(2000)
  const [promptInput, setPromptInput] = useState('')
  const [uiMode, setUiMode] = useState('form') // 'form' or 'prompt'
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    setLoading(true)
    setError(null)

    try {
      let payload

      if (uiMode === 'prompt') {
        // Prompt mode: use Groq to parse free-form input
        if (!promptInput.trim()) {
          setError('Please enter a search query')
          setLoading(false)
          return
        }

        // Parse user query using Groq LLM
        const parseResponse = await fetch("http://127.0.0.1:8000/parse", {
          method: "POST",
          mode: "cors",
          credentials: "omit",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: promptInput })
        })

        if (!parseResponse.ok) {
          throw new Error(`Parse failed: ${parseResponse.status}`)
        }

        payload = await parseResponse.json()
      } else {
        // Form mode: build payload directly from form
        if (!state || !city) {
          setError('Please select state and city')
          setLoading(false)
          return
        }

        if (maxPrice < 500 || maxPrice > 10000) {
          setError('Max price must be between $500 and $10,000')
          setLoading(false)
          return
        }

        // City coordinates
        const cityCoords = {
          'Los Angeles': { lat: 34.0522, lon: -118.2437 },
          'San Francisco': { lat: 37.7749, lon: -122.4194 },
          'Houston': { lat: 29.7604, lon: -95.3698 },
          'Dallas': { lat: 32.7767, lon: -96.7970 },
          'Austin': { lat: 30.2672, lon: -97.7431 },
          'Miami': { lat: 25.7617, lon: -80.1918 },
          'Orlando': { lat: 28.5421, lon: -81.3723 },
          'New York City': { lat: 40.7128, lon: -74.0060 },
          'Philadelphia': { lat: 39.9526, lon: -75.1652 },
          'Chicago': { lat: 41.8781, lon: -87.6298 },
          'Atlanta': { lat: 33.7490, lon: -84.3880 },
          'Seattle': { lat: 47.6062, lon: -122.3321 },
          'Boston': { lat: 42.3601, lon: -71.0589 },
          'Denver': { lat: 39.7392, lon: -104.9903 },
          'Phoenix': { lat: 33.4484, lon: -112.0742 }
        }

        const coords = cityCoords[city] || { lat: 34.0522, lon: -118.2437 }

        // Map profile to features
        const profileFeatures = {
          'cheap_but_safe': ['cheap', 'safe', 'schools'],
          'balanced': ['parks', 'schools', 'hospitals'],
          'premium': ['parks', 'schools', 'hospitals']
        }

        payload = {
          location: coords,
          features: profileFeatures[profile] || ['parks', 'schools']
        }
      }

      // Search using payload
      const searchResponse = await fetch("http://127.0.0.1:8000/search", {
        method: "POST",
        mode: "cors",
        credentials: "omit",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })

      if (!searchResponse.ok) {
        throw new Error(`Search failed: ${searchResponse.status}`)
      }

      const data = await searchResponse.json()
      let resultsArr = []
      if (Array.isArray(data)) resultsArr = data
      else if (Array.isArray(data.results)) resultsArr = data.results
      else if (Array.isArray(data.data)) resultsArr = data.data
      setResults(resultsArr)
    } catch (err) {
      setError(err?.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="search-page">
      <div className="noise"></div>
      <div className="container">
        <Header />
        <SearchPanel
          stateValue={state}
          cityValue={city}
          profile={profile}
          maxPrice={maxPrice}
          states={STATES}
          cities={CITIES}
          setState={setState}
          setCity={setCity}
          setProfile={setProfile}
          setMaxPrice={setMaxPrice}
          promptInput={promptInput}
          setPromptInput={setPromptInput}
          uiMode={uiMode}
          setUiMode={setUiMode}
          onSearch={handleSearch}
          loading={loading}
        />

        <ResultsPanel results={results} loading={loading} error={error} />
      </div>
    </div>
  )
}
