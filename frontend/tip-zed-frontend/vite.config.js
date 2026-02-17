import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
      alias: {
        '@': '/src', // Maps '@' to the '/src' directory
      },
    },
  server: {
    proxy: {
      // Catch any request starting with "/api"
      '/api': {
        target: 'https://lipila.schadmin.cloud', // The Live Server URL
        changeOrigin: true, // ⚠️ Crucial: This tricks the backend into thinking the request is local
        secure: false,      // Helpful if the live server has SSL issues
      },
    },
  },
})