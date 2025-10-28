/** @type {import('next').NextConfig} */
const nextConfig = {
  // Remove 'output: export' for Railway (use SSR)
  // Use 'output: export' only for GitHub Pages
  ...(process.env.RAILWAY_ENVIRONMENT ? {} : { output: 'export' }),
  trailingSlash: true,
  // basePath only for GitHub Pages
  ...(process.env.RAILWAY_ENVIRONMENT ? {} : { basePath: '/BerInsight' }),
  images: {
    unoptimized: true
  },
  env: {
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'
  }
}

module.exports = nextConfig
