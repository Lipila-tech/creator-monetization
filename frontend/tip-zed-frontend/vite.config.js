import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // Catch any request starting with "/api"
      '/api': {
        target: 'https://tipzed.pythonanywhere.com', // The Live Server URL
        changeOrigin: true, // ⚠️ Crucial: This tricks the backend into thinking the request is local
        secure: false,      // Helpful if the live server has SSL issues
      },
    },
  },
})