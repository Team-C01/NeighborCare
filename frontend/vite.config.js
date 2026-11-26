import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    strictPort: true,
  },
  test: {
    environment: 'jsdom',
    include: ['tests/**/*.test.{js,jsx}', 'tests/**/*.spec.{js,jsx}'],
    reporters: ['default', 'junit'],
    outputFile: {
      junit: 'test-results/junit.xml',
    },
  },
});
