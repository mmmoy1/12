import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Derive base path for GitHub Pages if building in Actions
const repository = process.env.GITHUB_REPOSITORY
const repoName = repository ? repository.split('/')[1] : ''
const base = repoName ? `/${repoName}/` : '/'

export default defineConfig({
  plugins: [react()],
  base,
})
