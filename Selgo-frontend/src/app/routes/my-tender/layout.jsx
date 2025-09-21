"use client";
import Header from "@/components/mt-tender/layout/Header";
import Footer from "@/components/mt-tender/layout/Footer";

export default function MyTenderLayout({ children }) {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <Header />
      <main className="flex-1">{children}</main>
      <Footer />
    </div>
  );
}