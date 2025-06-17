import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    serverActions: {},
  },
  transpilePackages: ["react-pdf"],
};

module.exports = nextConfig;
