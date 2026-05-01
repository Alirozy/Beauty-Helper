const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

function extractErrorMessage(payload) {
  if (!payload) return 'Request failed. Please try again later.'
  if (typeof payload === 'string') return payload
  if (payload.detail) return payload.detail
  if (payload.message) return payload.message

  const firstValue = Object.values(payload)[0]
  if (Array.isArray(firstValue) && firstValue.length) {
    return String(firstValue[0])
  }
  if (typeof firstValue === 'string') {
    return firstValue
  }

  return 'Request failed. Please try again later.'
}

function getTokens() {
  const access = localStorage.getItem('accessToken')
  const refresh = localStorage.getItem('refreshToken')
  return { access, refresh }
}

export async function refreshAccessToken() {
  const { refresh } = getTokens()
  if (!refresh) return null

  const response = await fetch(`${API_BASE_URL}/api/users/token/refresh/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  })

  if (!response.ok) {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')
    return null
  }

  const data = await response.json()
  localStorage.setItem('accessToken', data.access)
  if (data.refresh) {
    localStorage.setItem('refreshToken', data.refresh)
  }
  return data.access
}

export async function apiFetch(path, options = {}, retry = true) {
  const token = localStorage.getItem('accessToken')
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  })

  if (response.status === 401 && retry) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      return apiFetch(path, options, false)
    }
  }

  let payload
  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok) {
    const message = extractErrorMessage(payload)
    throw new Error(message)
  }

  return payload
}

export { API_BASE_URL }
