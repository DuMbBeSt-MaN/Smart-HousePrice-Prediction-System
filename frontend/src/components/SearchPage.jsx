import { useState } from 'react'
import Header from './Header'
import SearchPanel from './SearchPanel'
import ResultsPanel from './ResultsPanel'
import { recommendHouses, searchFromText } from '../api'
import './SearchPage.css'

const STATES = ['Andhra Pradesh', 'Delhi', 'Gujarat', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'West Bengal']

const CITIES = {
  'Andhra Pradesh': ['Visakhapatnam', 'Vijayawada', 'Guntur', 'Tirupati'],
  'Delhi': ['New Delhi', 'Dwarka', 'Rohini', 'Saket', 'Lajpat Nagar'],
  'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot'],
  'Karnataka': ['Bengaluru', 'Mysuru', 'Hubli', 'Mangaluru'],
  'Kerala': ['Kochi', 'Thiruvananthapuram', 'Kozhikode', 'Thrissur'],
  'Madhya Pradesh': ['Bhopal', 'Indore', 'Jabalpur', 'Gwalior'],
  'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik', 'Thane', 'Navi Mumbai'],
  'Punjab': ['Chandigarh', 'Ludhiana', 'Amritsar', 'Jalandhar'],
  'Rajasthan': ['Jaipur', 'Jodhpur', 'Udaipur', 'Kota'],
  'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Salem', 'Tiruchirappalli'],
  'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad', 'Karimnagar'],
  'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Noida', 'Ghaziabad'],
  'West Bengal': ['Kolkata', 'Howrah', 'Durgapur', 'Siliguri']
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

        // Map profile to features
        const profileFeatures = {
          'cheap_but_safe': ['affordable', 'safe', 'near schools'],
          'balanced': ['near parks', 'near schools', 'near hospitals'],
          'premium': ['near parks', 'near schools', 'near hospitals', 'premium']
        }

        // Use /parse to geocode the city+state via Google Maps
        const parseResponse = await fetch("http://127.0.0.1:8000/parse", {
          method: "POST",
          mode: "cors",
          credentials: "omit",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text: `${profileFeatures[profile].join(', ')} in ${city}, ${state}` })
        })

        if (!parseResponse.ok) throw new Error(`Parse failed: ${parseResponse.status}`)
        payload = await parseResponse.json()
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
