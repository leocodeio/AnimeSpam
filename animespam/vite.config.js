import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import vercel from "vite-plugin-vercel";

export default defineConfig({
  plugins: [react(), vercel()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom']
        }
      }
    },
    assetsInlineLimit: 0,
    cssCodeSplit: true
  },
  server: {
    headers: {
      'Cache-Control': 'public, max-age=31536000, immutable'
    }
  }
});
