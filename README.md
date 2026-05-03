# BeaverHacks Dev OS - Frontend

A gamified development environment GUI for the BeaverHacks hackathon. Built with React, Vite, Tailwind CSS, and Zustand for state management.

## Features

- 🎮 **Gamified Interface**: Ticket-based task system with XP rewards
- 💻 **Terminal**: Interactive terminal emulator for executing commands
- 🐍 **Python IDE**: Code editor and execution environment
- 🎯 **Ticket Board**: Track and complete development tickets
- 🖥️ **OS-like GUI**: Windows, taskbar, and desktop grid background
- 📱 **Responsive Design**: Modern dark theme inspired by dev environments

## Tech Stack

- **Frontend Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Routing**: React Router
- **HTTP Client**: Axios
- **Package Manager**: npm

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
```

## Project Structure

```
src/
├── main.jsx              # Entry point
├── App.jsx               # Root component with routing
├── index.css             # Global styles + Tailwind
├── pages/
│   ├── LoginPage.jsx     # Authentication page
│   └── Dashboard.jsx     # Main OS dashboard
├── components/
│   ├── Taskbar.jsx       # Bottom taskbar with app switcher
│   ├── Desktop.jsx       # Background with grid pattern
│   ├── Terminal.jsx      # Terminal emulator
│   ├── PythonIDE.jsx     # Python code editor
│   └── TicketBoard.jsx   # Gamified task system
├── store/
│   └── authStore.js      # Zustand auth state
└── utils/
    └── api.js            # Axios API client & endpoints
```

## Backend Integration

The frontend expects a backend API at `/api`. Update the proxy target in `vite.config.js` if your backend runs on a different port.

### API Endpoints to Implement

**Authentication**
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/register` - User registration

**Tickets**
- `GET /api/tickets` - Fetch all tickets
- `GET /api/tickets/:id` - Get ticket by ID
- `POST /api/tickets` - Create new ticket
- `PUT /api/tickets/:id` - Update ticket
- `PATCH /api/tickets/:id/complete` - Mark ticket as complete

**Code Execution**
- `POST /api/execute/python` - Execute Python code
- `POST /api/execute/terminal` - Execute terminal commands

**User**
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `GET /api/user/stats` - Get user stats (XP, level, etc.)

## Development Tips

1. **Hot Module Replacement**: Vite automatically reloads on file changes
2. **Mock Data**: Currently uses mock data. Connect to real API in `store/authStore.js` and components
3. **Terminal Commands**: Add custom commands in `components/Terminal.jsx`
4. **Code Execution**: Uncomment axios calls once backend is ready

## Next Steps

- [ ] Connect login to backend authentication
- [ ] Fetch real tickets from backend
- [ ] Implement Python code execution via backend
- [ ] Add user profile/stats page
- [ ] Create leaderboard
- [ ] Add notifications system
- [ ] Implement file browser
- [ ] Add theme switcher

## Commands

**Install dependencies:**
```bash
npm install
```

**Start dev server:**
```bash
npm run dev
```

**Build for production:**
```bash
npm run build
```

**Lint code:**
```bash
npm run lint
```

## License

Part of BeaverHacks hackathon.