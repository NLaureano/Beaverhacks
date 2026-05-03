export default function Desktop() {
  return (
    <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-blue-900 to-black opacity-60 pointer-events-none">
      {/* Grid pattern background */}
      <div
        className="absolute inset-0"
        style={{
          backgroundImage: 'linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px)',
          backgroundSize: '40px 40px',
        }}
      />
    </div>
  )
}
