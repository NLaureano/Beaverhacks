export default function FileExplorer({ files, selectedFile, onSelectFile }) {
  return (
    <div className="w-64 bg-os-panel border-r border-gray-600 flex flex-col">
      <h2 className="text-sm font-bold p-3 border-b border-gray-600">📁 Files</h2>
      <div className="flex-1 overflow-y-auto">
        {files.map((file) => (
          <div
            key={file.id}
            onClick={() => onSelectFile(file)}
            className={`px-3 py-2 text-sm cursor-pointer border-l-2 transition ${
              selectedFile?.id === file.id
                ? 'bg-os-accent border-l-os-accent text-white'
                : 'border-l-transparent hover:bg-gray-700'
            }`}
          >
            <span className="mr-2">
              {file.name.includes('.py') ? '🐍' : file.name.includes('.json') ? '📄' : '📝'}
            </span>
            {file.name}
          </div>
        ))}
      </div>
    </div>
  )
}
