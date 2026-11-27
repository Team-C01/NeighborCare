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
    coverage: {
      provider: 'v8',
      include: ['src/**/*.{js,jsx}'],
      exclude: ['**/*.test.*', '**/*.spec.*', '**/__tests__/**'],
      reporter: ['text', 'lcov'],
      reportsDirectory: 'coverage',
    },
    reporters: ['default', 'junit'],
    outputFile: {
      junit: 'test-results/junit.xml',
    },
  },
});
