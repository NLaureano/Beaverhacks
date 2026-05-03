import { create } from 'zustand'

export const useStore = create((set) => ({
  isAuthenticated: false,
  user: null,
  login: (username, password) => {
    // TODO: Call backend API to authenticate
    // For now, mock login
    set({
      isAuthenticated: true,
      user: { username, id: '1' }
    })
  },
  logout: () => {
    set({
      isAuthenticated: false,
      user: null
    })
  },
}))
