/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ['maps.googleapis.com', 'images.unsplash.com'],
    remotePatterns: [
      {
        protocol: "https",
        hostname: "picsum.photos",
        
      },
    ],
  },
};

export default nextConfig;
