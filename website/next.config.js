/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'jcsnotfunny.com',
      },
      {
        protocol: 'https', 
        hostname: 'cdn.jcsnotfunny.com',
      },
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
      },
    ],
    formats: ['image/webp', 'image/avif'],
    minimumCacheTTL: 60 * 60 * 24 * 30,
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
        ],
      },
      {
        source: '/audio/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
          {
            key: 'Content-Type',
            value: 'audio/mpeg',
          },
        ],
      },
      {
        source: '/images/(.*)',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
          {
            key: 'Cache-Tag',
            value: 'images',
          },
        ],
      },
    ];
  },
  async redirects() {
    return [
      {
        source: '/episode/:slug',
        destination: '/episodes/:slug',
        permanent: true,
      },
      {
        source: '/podcast',
        destination: '/episodes',
        permanent: true,
      },
    ];
  },
  compress: true,
  poweredByHeader: false,
  generateEtags: true,
  turbopack: {},
};

module.exports = nextConfig;