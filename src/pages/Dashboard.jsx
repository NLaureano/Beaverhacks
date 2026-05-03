import { useState } from 'react'
import { useStore } from '../store/authStore'
import Taskbar from '../components/Taskbar'
import TicketWorkspace from '../components/TicketWorkspace'
import Desktop from '../components/Desktop'
import DraggableWindow from '../components/DraggableWindow'

export default function Dashboard() {
  const { user, logout } = useStore()
  const [openWindows, setOpenWindows] = useState({
    workspace: true,
  })
  const [windowPositions, setWindowPositions] = useState({
    workspace: { x: 32, y: 32 },
  })

  const toggleWindow = (key) => {
    setOpenWindows((prev) => ({
      ...prev,
      [key]: !prev[key],
    }))
  }

  const closeWindow = (key) => {
    setOpenWindows((prev) => ({
      ...prev,
      [key]: false,
    }))
  }

  return (
    <div className="h-screen bg-os-bg flex flex-col overflow-hidden">
      {/* Desktop Area */}
      <div className="flex-1 overflow-auto">
        <Desktop />

        {/* Windows */}
        <div className="relative w-full h-full">
          {/* Ticket Workspace - main window */}
          {openWindows.workspace && (
            <DraggableWindow
              id="workspace"
              title="💻 Dev Workspace"
              initialX={windowPositions.workspace.x}
              initialY={windowPositions.workspace.y}
              initialWidth={1200}
              initialHeight={700}
              onClose={() => closeWindow('workspace')}
            >
              <TicketWorkspace />
            </DraggableWindow>
          )}
        </div>
      </div>

      {/* Taskbar */}
      <Taskbar
        openWindows={openWindows}
        toggleWindow={toggleWindow}
        user={user}
        onLogout={logout}
      />
    </div>
  )
}
