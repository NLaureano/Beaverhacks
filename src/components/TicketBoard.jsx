import { useState, useEffect } from 'react'
import { ticketsAPI } from '../utils/api'
const MOCK_TICKETS = [
  {
    id: 1,
    title: 'Fix login validation',
    description: 'Add email validation to login form',
    difficulty: 'Easy',
    xp: 50,
    status: 'open',
    priority: 'High'
  },
  {
    id: 2,
    title: 'Create dashboard layout',
    description: 'Build OS-like dashboard with windows',
    difficulty: 'Medium',
    xp: 150,
    status: 'open',
    priority: 'High'
  },
  {
    id: 3,
    title: 'Implement terminal API',
    description: 'Connect terminal to backend for command execution',
    difficulty: 'Hard',
    xp: 300,
    status: 'open',
    priority: 'Medium'
  },
  {
    id: 4,
    title: 'Python code execution',
    description: 'Add Python sandbox execution endpoint',
    difficulty: 'Hard',
    xp: 250,
    status: 'open',
    priority: 'High'
  },
]

export default function TicketBoard() {
  const [tickets, setTickets] = useState(MOCK_TICKETS)
  const [selectedTicket, setSelectedTicket] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadTickets = async () => {
    setLoading(true)
    setError('')

    try{
      const response = await ticketsAPI.getAll()
      setTickets(response.data)
    } catch (error) {
      console.error('failed to fetch tickets:', error)
      setError('Could not load tickets from the backend.')
      setTickets(MOCK_TICKETS)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTickets()
  }, [])

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-400'
      case 'Medium': return 'text-yellow-400'
      case 'Hard': return 'text-red-400'
      default: return 'text-gray-400'
    }
  }

  const getPriorityBg = (priority) => {
    switch (priority) {
      case 'High': return 'bg-red-900'
      case 'Medium': return 'bg-yellow-900'
      case 'Low': return 'bg-green-900'
      default: return 'bg-gray-900'
    }
  }

  const completeTicket = (id) => {
    setTickets((prev) => prev.map((t) => t.id === id ? { ...t, status: 'completed' } : t))
    setSelectedTicket(null)
  }

  return (
    <div className="h-full flex gap-4">
      {/* Ticket List */}
      <div className="flex-1 overflow-y-auto">
        <h2 className="text-lg font-bold mb-3 sticky top-0 bg-os-panel py-2">🎯 Available Tickets</h2>
        {loading && <p className="text-sm text-gray-400 mb-3">Loading tickets...</p>}
        {error && <p className="text-sm text-red-400 mb-3">{error}</p>}
        <div className="space-y-2">
          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => setSelectedTicket(ticket)}
              className={`p-3 rounded cursor-pointer transition ${
                selectedTicket?.id === ticket.id
                  ? 'bg-os-accent'
                  : 'bg-gray-800 hover:bg-gray-700'
              } ${ticket.status === 'completed' ? 'opacity-50 line-through' : ''}`}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold text-sm">{ticket.title}</h3>
                  <p className={`text-xs ${getDifficultyColor(ticket.difficulty)}`}>
                    {ticket.difficulty}
                  </p>
                </div>
                <span className="text-lg font-bold text-yellow-400">+{ticket.xp} XP</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Ticket Details */}
      {selectedTicket && (
        <div className="w-80 bg-gray-800 p-4 rounded border border-gray-600">
          <h2 className="text-lg font-bold mb-3">{selectedTicket.title}</h2>

          <div className="space-y-2 mb-4 text-sm">
            <div>
              <span className="font-semibold">Status:</span> {selectedTicket.status}
            </div>
            <div>
              <span className="font-semibold">Difficulty:</span>{' '}
              <span className={getDifficultyColor(selectedTicket.difficulty)}>
                {selectedTicket.difficulty}
              </span>
            </div>
            <div>
              <span className={`inline-block px-2 py-1 rounded text-xs font-semibold ${getPriorityBg(selectedTicket.priority)}`}>
                {selectedTicket.priority} Priority
              </span>
            </div>
            <div>
              <span className="font-semibold">Reward:</span>{' '}
              <span className="text-yellow-400">+{selectedTicket.xp} XP</span>
            </div>
          </div>

          <p className="text-sm text-gray-300 mb-4">{selectedTicket.description}</p>

          {selectedTicket.status === 'open' && (
            <button
              onClick={() => completeTicket(selectedTicket.id)}
              className="w-full py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded font-semibold"
            >
              ✓ Mark Complete
            </button>
          )}

          {selectedTicket.status === 'completed' && (
            <div className="text-center py-2 bg-green-900 rounded text-green-300 text-sm font-semibold">
              ✓ Completed!
            </div>
          )}
        </div>
      )}
    </div>
  )
}
