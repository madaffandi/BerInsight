/** @type {import('next').NextConfig} */
const isDev = process.env.NODE_ENV === 'development'
const isGitHubPages = process.env.GITHUB_PAGES === 'true'

const nextConfig = {
  // Only use static export for GitHub Pages build
  ...(isGitHubPages ? { output: 'export' } : {}),
  trailingSlash: true,
  // basePath only for GitHub Pages deployment
  ...(isGitHubPages ? { basePath: '/BerInsight' } : {}),
  images: {
    unoptimized: true
  },
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
  }
}

module.exports = nextConfig
