import { useRef, useState, useEffect } from 'react'

export default function DraggableWindow({
  id,
  title,
  children,
  onClose,
  initialX = 0,
  initialY = 0,
  initialWidth = 500,
  initialHeight = 400,
}) {
  const [position, setPosition] = useState({ x: initialX, y: initialY })
  const [size, setSize] = useState({ width: initialWidth, height: initialHeight })
  const [isDragging, setIsDragging] = useState(false)
  const [isResizing, setIsResizing] = useState(null)
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 })
  const [resizeStart, setResizeStart] = useState({ x: 0, y: 0, width: 0, height: 0 })
  const windowRef = useRef(null)

  // Global mouse move listener for dragging and resizing
  useEffect(() => {
    const handleGlobalMouseMove = (e) => {
      if (isDragging) {
        setPosition({
          x: e.clientX - dragOffset.x,
          y: e.clientY - dragOffset.y,
        })
      }

      if (isResizing === 'se') {
        // Only resize from bottom-right corner - simple and predictable
        const deltaX = e.clientX - resizeStart.x
        const deltaY = e.clientY - resizeStart.y

        const newWidth = Math.max(300, resizeStart.width + deltaX)
        const newHeight = Math.max(200, resizeStart.height + deltaY)

        setSize({ width: newWidth, height: newHeight })
      }
    }

    const handleGlobalMouseUp = () => {
      setIsDragging(false)
      setIsResizing(null)
    }

    if (isDragging || isResizing) {
      document.addEventListener('mousemove', handleGlobalMouseMove)
      document.addEventListener('mouseup', handleGlobalMouseUp)

      return () => {
        document.removeEventListener('mousemove', handleGlobalMouseMove)
        document.removeEventListener('mouseup', handleGlobalMouseUp)
      }
    }
  }, [isDragging, isResizing, dragOffset, resizeStart])

  const handleMouseDown = (e) => {
    if (e.target.closest('.window-title')) {
      setIsDragging(true)
      setDragOffset({
        x: e.clientX - position.x,
        y: e.clientY - position.y,
      })
    }
  }

  const startResize = (direction, e) => {
    e.stopPropagation()
    setIsResizing(direction)
    setResizeStart({
      x: e.clientX,
      y: e.clientY,
      width: size.width,
      height: size.height,
    })
  }

  return (
    <div
      ref={windowRef}
      className="absolute window z-20"
      style={{
        left: `${position.x}px`,
        top: `${position.y}px`,
        width: `${size.width}px`,
        height: `${size.height}px`,
        cursor: isDragging ? 'grabbing' : 'default',
      }}
      onMouseDown={handleMouseDown}
    >
      <div className="window-title flex justify-between items-center cursor-grab active:cursor-grabbing">
        <span>{title}</span>
        <button
          onClick={onClose}
          className="hover:bg-red-600 px-2 py-0 rounded"
        >
          ✕
        </button>
      </div>

      <div className="window-content overflow-auto" style={{ height: `calc(100% - 28px)` }}>
        {children}
      </div>

      {/* Resize Handle - Bottom Right Corner Only */}
      <div
        onMouseDown={(e) => startResize('se', e)}
        className="absolute bottom-0 right-0 w-4 h-4 hover:bg-os-accent"
        style={{ cursor: 'nwse-resize', backgroundColor: 'transparent' }}
        title="Drag to resize"
      />
    </div>
  )
}
