const AUTH_BASE = `${import.meta.env.VITE_API_URL}/api/auth`

export function getToken() {
  return localStorage.getItem('token')
}

export function setToken(token) {
  localStorage.setItem('token', token)
}

export function clearToken() {
  localStorage.removeItem('token')
}

export function authHeaders() {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    const detail = body.detail
    const message =
      typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((e) => e.msg).join(', ')
          : `Request failed (${res.status})`
    throw new Error(message)
  }
  return res.json()
}

export async function login(username, password) {
  const res = await fetch(`${AUTH_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username, password }),
  })
  const data = await handleResponse(res)
  setToken(data.access_token)
  return data
}

export async function getMe() {
  const res = await fetch(`${AUTH_BASE}/me`, {
    headers: authHeaders(),
  })
  return handleResponse(res)
}
