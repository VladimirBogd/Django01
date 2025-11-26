import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': {
        target: "http://localhost:8000"
      },
      '/admin': {
        target: "http://localhost:8000"
      },
      '/static': {
        target: "http://localhost:8000"
      },
      '/media': {
        target: "http://localhost:8000"
      },
    },
    // Add headers for proper MIME types
    headers: {
      'Content-Type': 'text/css'
    }
  },
  // Ensure proper build configuration
  build: {
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          let extType = assetInfo.name.split('.')[1]
          if (/png|jpe?g|svg|gif|tiff|bmp|ico/i.test(extType)) {
            extType = 'img'
          } else if (/css/i.test(extType)) {
            extType = 'css'
          }
          return `assets/${extType}/[name]-[hash][extname]`
        }
      }
    }
  }
})
