/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'os-bg': '#1a1a1a',
        'os-panel': '#2d2d2d',
        'os-accent': '#0066cc',
        'terminal-bg': '#0c0c0c',
        'terminal-text': '#00ff00',
      }
    },
  },
  plugins: [],
}
