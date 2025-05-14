import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  optimizeDeps: {
    include: ['react', 'react-dom', '@mantine/core', 'axios']
  },
  plugins: [react()],
  server: {
    proxy: {
      // Add proxy to bypass CORS issues
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})