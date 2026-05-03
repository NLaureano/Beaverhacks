export default function Taskbar({ openWindows, toggleWindow, user, onLogout }) {
  return (
    <div className="taskbar">
      <div className="flex gap-2 flex-1">
        <button
          onClick={() => toggleWindow('workspace')}
          className={`taskbar-btn ${openWindows.workspace ? 'bg-blue-700' : ''}`}
        >
          💻 Dev Workspace
        </button>
      </div>

      <div className="flex gap-3 items-center ml-auto">
        <span className="text-xs text-gray-300">👤 {user?.username}</span>
        <button
          onClick={onLogout}
          className="taskbar-btn bg-red-600 hover:bg-red-700"
        >
          Logout
        </button>
      </div>
    </div>
  )
}
