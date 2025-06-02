"use client"
// import Header from "@/components/layout/Header";
// import Footer from "@/components/layout/Footer";
import Hero from "@/components/home/Hero";
import Page from "@/components/GenerateCard";
import PopularAds from "@/components/home/PopularAds";


export default function Home() {
  return (
    <main className="bg-white">
      {/* <Header /> */}
        <Hero />
        <PopularAds />
        <Page />
      {/* <Footer /> */}
    </main>
  );
}