export default function TestResults({ results, loading }) {
  if (!results) {
    return (
      <div className="p-4 bg-gray-800 text-gray-400 text-sm">
        Run tests to see results
      </div>
    )
  }

  if (loading) {
    return (
      <div className="p-4 bg-gray-800 text-gray-400 text-sm">
        Running tests... ⏳
      </div>
    )
  }

  const { passed, failed, tests, error, output } = results

  return (
    <div className="p-4 space-y-4 max-h-96 overflow-y-auto">
      {/* Summary */}
      <div className="flex gap-4">
        <div
          className={`px-3 py-2 rounded text-sm font-semibold ${
            passed ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'
          }`}
        >
          {passed ? '✓ All Tests Passed!' : '✗ Tests Failed'}
        </div>
        {tests && (
          <div className="text-xs text-gray-400">
            {tests.passed} / {tests.total} tests passing
          </div>
        )}
      </div>

      {/* Error Messages */}
      {error && (
        <div className="bg-red-900 border border-red-700 rounded p-3 text-red-200 text-xs font-mono whitespace-pre-wrap break-words">
          {error}
        </div>
      )}

      {/* Test Output */}
      {output && (
        <div className="bg-terminal-bg border border-gray-700 rounded p-3 text-terminal-text text-xs font-mono whitespace-pre-wrap break-words">
          {output}
        </div>
      )}

      {/* Individual Test Results */}
      {tests && tests.list && (
        <div className="space-y-2">
          <h3 className="text-sm font-bold text-gray-300">Test Details</h3>
          {tests.list.map((test, i) => (
            <div
              key={i}
              className={`text-xs p-2 rounded border-l-2 ${
                test.passed
                  ? 'bg-green-900 bg-opacity-20 border-l-green-500 text-green-300'
                  : 'bg-red-900 bg-opacity-20 border-l-red-500 text-red-300'
              }`}
            >
              <div className="font-mono">
                {test.passed ? '✓' : '✗'} {test.name}
              </div>
              {test.message && (
                <div className="text-xs mt-1 opacity-80">{test.message}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
