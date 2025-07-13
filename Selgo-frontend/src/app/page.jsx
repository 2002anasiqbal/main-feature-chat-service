"use client"
import { useEffect } from "react";
import Hero from "@/components/home/Hero";
import Page from "@/components/GenerateCard";
import PopularAds from "@/components/home/PopularAds";

export default function Home() {
  useEffect(() => {
    // Prevent back button from homepage
    const preventBack = () => {
      window.history.pushState(null, null, window.location.pathname);
    };

    // Add a state entry so back button stays on homepage
    window.history.pushState(null, null, window.location.pathname);
    
    // Listen for back button and prevent leaving homepage
    window.addEventListener('popstate', preventBack);

    return () => {
      window.removeEventListener('popstate', preventBack);
    };
  }, []);

  return (
    <main className="bg-white">
      <Hero />
      <PopularAds />
      <Page />
    </main>
  );
}