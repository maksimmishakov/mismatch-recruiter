import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
 
  server: {
    port: 3001,
    host: '0.0.0.0',
    strictPort: false,
    middlewareMode: false,
   
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
        rewrite: (path) => path,
      }
    },
  },
 
  preview: {
    port: 3001,
    host: '0.0.0.0',
    strictPort: false,
  },
 
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['react', 'react-dom', 'react-router-dom'],
        }
      }
    }
  }
})