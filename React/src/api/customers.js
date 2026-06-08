import { authHeaders } from './auth'

const API_BASE = `${import.meta.env.VITE_API_URL}/api/customers`

async function handleResponse(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  if (res.status === 204) {
    return null
  }
  return res.json()
}

export function getCustomers() {
  return fetch(API_BASE).then(handleResponse)
}

export function getCustomer(id) {
  return fetch(`${API_BASE}/${id}`).then(handleResponse)
}

export function createCustomer(data) {
  return fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(handleResponse)
}

export function updateCustomer(id, data) {
  return fetch(`${API_BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  }).then(handleResponse)
}

export function deleteCustomer(id) {
  return fetch(`${API_BASE}/${id}`, {
    method: 'DELETE',
    headers: authHeaders(),
  }).then(handleResponse)
}
