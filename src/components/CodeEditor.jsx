import { useState, useEffect, useRef } from 'react'

export default function CodeEditor({ selectedFile, files, onFileChange }) {
  const [openTabs, setOpenTabs] = useState([])
  const [activeTab, setActiveTab] = useState(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    if (selectedFile && !openTabs.find((t) => t.id === selectedFile.id)) {
      setOpenTabs((prev) => [...prev, selectedFile])
      setActiveTab(selectedFile.id)
    } else if (selectedFile) {
      setActiveTab(selectedFile.id)
    }
  }, [selectedFile])

  const closeTab = (fileId) => {
    setOpenTabs((prev) => prev.filter((t) => t.id !== fileId))
    if (activeTab === fileId) {
      setActiveTab(openTabs[0]?.id || null)
    }
  }

  const handleTabKey = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault()
      const textarea = textareaRef.current
      const start = textarea.selectionStart
      const end = textarea.selectionEnd
      const content = textarea.value

      // Insert 2 spaces for indentation
      const newContent = content.substring(0, start) + '  ' + content.substring(end)
      
      // Update file
      onFileChange(activeFile.id, newContent)
      setOpenTabs((prev) =>
        prev.map((t) =>
          t.id === activeFile.id ? { ...t, content: newContent } : t
        )
      )

      // Move cursor after inserted spaces
      setTimeout(() => {
        textarea.selectionStart = textarea.selectionEnd = start + 2
      }, 0)
    }
  }

  const activeFile = openTabs.find((t) => t.id === activeTab)

  return (
    <div className="flex-1 flex flex-col bg-gray-900">
      {/* Tab Bar */}
      {openTabs.length > 0 && (
        <div className="flex bg-gray-800 border-b border-gray-700 overflow-x-auto">
          {openTabs.map((file) => (
            <div
              key={file.id}
              onClick={() => setActiveTab(file.id)}
              className={`flex items-center px-3 py-2 text-xs border-r border-gray-700 cursor-pointer transition ${
                activeTab === file.id
                  ? 'bg-os-panel text-white'
                  : 'bg-gray-800 text-gray-400 hover:text-white'
              }`}
            >
              <span className="mr-2">
                {file.name.includes('.py') ? '🐍' : '📝'}
              </span>
              <span>{file.name}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  closeTab(file.id)
                }}
                className="ml-2 hover:text-red-400 text-xs"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Editor Area */}
      {activeFile ? (
        <div className="flex-1 flex flex-col p-3">
          <div className="text-xs text-gray-400 mb-2">
            {activeFile.name}
          </div>
          <textarea
            ref={textareaRef}
            value={activeFile.content}
            onChange={(e) => {
              onFileChange(activeFile.id, e.target.value)
              setOpenTabs((prev) =>
                prev.map((t) =>
                  t.id === activeFile.id ? { ...t, content: e.target.value } : t
                )
              )
            }}
            onKeyDown={handleTabKey}
            className="flex-1 bg-terminal-bg text-terminal-text font-mono text-sm p-3 border border-gray-700 rounded resize-none focus:outline-none focus:border-os-accent"
            spellCheck="false"
          />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-gray-500">
          Select a file to edit
        </div>
      )}
    </div>
  )
}
