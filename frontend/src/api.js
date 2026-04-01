// Backend API configuration
const API_BASE = "http://127.0.0.1:8000";

/**
 * Parse free-form user text input into structured JSON
 * @param {string} userText - User's natural language search query
 * @returns {Promise<Object>} - Parsed JSON with location and features
 */
export async function parseUserInput(userText) {
  const response = await fetch(`${API_BASE}/parse`, {
    method: "POST",
    mode: "cors",
    credentials: "omit",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: userText })
  });
  if (!response.ok) throw new Error(`Parse failed: ${response.status}`);
  return response.json();
}

/**
 * Search for houses using a structured payload
 * @param {Object} payload - Payload with location and features
 * @returns {Promise<Object>} - Search results
 */
export async function searchHouses(payload) {
  const response = await fetch(`${API_BASE}/search`, {
    method: "POST",
    mode: "cors",
    credentials: "omit",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!response.ok) throw new Error(`Search failed: ${response.status}`);
  return response.json();
}

/**
 * Combined: parse text input then search for houses
 * @param {string} userText - User's natural language search query
 * @returns {Promise<Object>} - Search results
 */
export async function searchFromText(userText) {
  const parsed = await parseUserInput(userText);
  return searchHouses(parsed);
}

// Legacy: kept for backward compatibility
export async function recommendHouses(payload) {
  return searchHouses(payload);
}

export default { parseUserInput, searchHouses, searchFromText, recommendHouses }
