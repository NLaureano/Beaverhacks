import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Auth endpoints
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
}

// Tickets endpoints
export const ticketsAPI = {
  getAll: () => api.get('/tickets'),
  getById: (id) => api.get(`/tickets/${id}`),
  create: (ticket) => api.post('/tickets', ticket),
  update: (id, ticket) => api.put(`/tickets/${id}`, ticket),
  complete: (id) => api.patch(`/tickets/${id}/complete`),
}

// Codebase endpoints (separate from tickets)
export const codebaseAPI = {
  getFiles: (ticketId) => api.get(`/codebases/${ticketId}/files`),
  updateFile: (ticketId, fileName, content) =>
    api.put(`/codebases/${ticketId}/files/${fileName}`, { content }),
}

// Terminal/Code execution endpoints
export const executionAPI = {
  executePython: (code) =>
    api.post('/execute/python', { code }),
  executeTerminalCommand: (command) =>
    api.post('/execute/terminal', { command }),
  runTests: (ticketId, files) =>
    api.post(`/execute/tests/${ticketId}`, { files }),
}

// User endpoints
export const userAPI = {
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data),
  getStats: () => api.get('/user/stats'),
}

export default api
