import { useState, useEffect } from 'react'
import { ticketsAPI, codebaseAPI, executionAPI } from '../utils/api'
import FileExplorer from './FileExplorer'
import CodeEditor from './CodeEditor'
import TestResults from './TestResults'

const MOCK_TICKET = {
  id: 1,
  title: 'Fix login validation',
  description: 'Add email validation to login form. Users should not be able to login with invalid emails.',
  difficulty: 'Easy',
  xp: 50,
  status: 'open',
  priority: 'High',
}

const MOCK_CODEBASE_FILES = [
  {
    id: 1,
    name: 'auth.py',
    content: `def validate_email(email):
    # TODO: Add email validation here
    # Should check if email contains @ and .
    if not email:
        return False
    return True

def login(email, password):
    if not validate_email(email):
        return {"error": "Invalid email"}
    return {"success": True, "user": email}
`,
  },
  {
    id: 2,
    name: 'tests.py',
    content: `import unittest
from auth import validate_email

class TestEmailValidation(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(validate_email('user@example.com'))
    
    def test_missing_at_symbol(self):
        self.assertFalse(validate_email('userexample.com'))
    
    def test_empty_email(self):
        self.assertFalse(validate_email(''))
    
    def test_valid_email_with_plus(self):
        self.assertTrue(validate_email('user+tag@example.com'))

if __name__ == '__main__':
    unittest.main()
`,
  },
]

export default function TicketWorkspace({ ticketId = 1 }) {
  const [ticket, setTicket] = useState(MOCK_TICKET)
  const [files, setFiles] = useState(MOCK_CODEBASE_FILES)
  const [selectedFile, setSelectedFile] = useState(MOCK_CODEBASE_FILES[0])
  const [testResults, setTestResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [initialLoading, setInitialLoading] = useState(true)

  useEffect(() => {
    loadTicketAndFiles()
  }, [ticketId])

  const loadTicketAndFiles = async () => {
    setInitialLoading(true)
    try {
      // Fetch ticket metadata
      const ticketRes = await ticketsAPI.getById(ticketId)
      setTicket(ticketRes.data)

      // Fetch codebase files for this ticket
      const filesRes = await codebaseAPI.getFiles(ticketId)
      setFiles(filesRes.data)
      setSelectedFile(filesRes.data[0])
    } catch (error) {
      console.error('Failed to load ticket:', error)
      setTicket(MOCK_TICKET)
      setFiles(MOCK_CODEBASE_FILES)
      setSelectedFile(MOCK_CODEBASE_FILES[0])
    } finally {
      setInitialLoading(false)
    }
  }

  const handleFileChange = (fileId, newContent) => {
    setFiles((prev) =>
      prev.map((f) =>
        f.id === fileId ? { ...f, content: newContent } : f
      )
    )
  }

  const handleRunTests = async () => {
    setLoading(true)
    try {
      const response = await executionAPI.runTests(ticket.id, files)
      setTestResults(response.data)

      // If all tests pass, show success and offer next ticket
      if (response.data.passed) {
        setTimeout(() => {
          alert('🎉 All tests passed! Moving to next ticket...')
          handleNextTicket()
        }, 1500)
      }
    } catch (error) {
      console.error('Test execution failed:', error)
      setTestResults({
        passed: false,
        error: error.response?.data?.error || 'Failed to run tests',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleNextTicket = () => {
    // TODO: Fetch next ticket from backend
    console.log('Loading next ticket...')
  }

  return (
    <div className="h-full flex flex-col bg-os-bg text-white">
      {initialLoading ? (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <p className="text-lg mb-2">⏳ Loading ticket...</p>
            <p className="text-gray-400 text-sm">Fetching codebase from backend</p>
          </div>
        </div>
      ) : (
        <>
          {/* Header with Ticket Info */}
          <div className="bg-os-panel border-b border-gray-600 p-4">
            <div className="flex justify-between items-start">
              <div>
                <h1 className="text-xl font-bold mb-2">{ticket.title}</h1>
                <p className="text-sm text-gray-400 mb-3">{ticket.description}</p>
                <div className="flex gap-4 text-xs">
                  <span
                    className={`px-2 py-1 rounded ${
                      ticket.difficulty === 'Easy'
                        ? 'bg-green-900 text-green-300'
                        : ticket.difficulty === 'Medium'
                        ? 'bg-yellow-900 text-yellow-300'
                        : 'bg-red-900 text-red-300'
                    }`}
                  >
                    {ticket.difficulty}
                  </span>
                  <span className="text-yellow-400">+{ticket.xp} XP</span>
                </div>
              </div>
              <button
                onClick={handleRunTests}
                disabled={loading}
                className="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-gray-700 text-white font-semibold rounded transition"
              >
                {loading ? '⏳ Running tests...' : '▶ Run Tests'}
              </button>
            </div>
          </div>

          {/* Main Workspace */}
          <div className="flex-1 flex overflow-hidden">
            {/* File Explorer */}
            <FileExplorer
              files={files}
              selectedFile={selectedFile}
              onSelectFile={setSelectedFile}
            />

            {/* Code Editor */}
            <CodeEditor
              selectedFile={selectedFile}
              files={files}
              onFileChange={handleFileChange}
            />

            {/* Test Results */}
            <div className="w-80 bg-os-panel border-l border-gray-600 flex flex-col">
              <h2 className="text-sm font-bold p-3 border-b border-gray-600">
                🧪 Test Results
              </h2>
              <div className="flex-1 overflow-y-auto">
                <TestResults results={testResults} loading={loading} />
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  )
}
