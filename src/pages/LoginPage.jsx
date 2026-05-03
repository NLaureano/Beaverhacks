import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useStore } from '../store/authStore'

export default function LoginPage() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const login = useStore((state) => state.login)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!username || !password) {
      setError('Username and password required')
      return
    }

    try {
      // TODO: Replace with actual API call
      // const res = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ username, password })
      // })
      // if (!res.ok) throw new Error('Invalid credentials')

      login(username, password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black flex items-center justify-center">
      <div className="window w-96">
        <div className="window-title">
          <span>BeaverHacks Dev OS - Login</span>
          <span className="text-lg">_</span>
        </div>
        <div className="window-content">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold mb-2">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded text-white focus:outline-none focus:border-os-accent"
                placeholder="dev_user"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded text-white focus:outline-none focus:border-os-accent"
                placeholder="••••••••"
              />
            </div>

            {error && <div className="text-red-400 text-sm">{error}</div>}

            <button
              type="submit"
              className="w-full py-2 bg-os-accent hover:bg-blue-700 text-white font-semibold rounded transition"
            >
              Enter Dev OS
            </button>
          </form>

          <p className="text-gray-400 text-xs mt-6 text-center">
            Demo: Use any username/password to enter
          </p>
        </div>
      </div>
    </div>
  )
}
