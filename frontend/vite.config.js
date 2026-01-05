import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
      watch: {
        usePolling: true, // Fixes hot reload issues on Windows/WSL
      },
      host: true, // Needed for Docker port mapping
      strictPort: true,
      port: 5173, 
    }
})
