// File: C:\Users\Amjad Khalil\OneDrive\Desktop\Selggo\selgo-frontend\app\routes\create-ad\boat\[subcategory]\page.jsx

"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import BoatAdForm from "@/components/boat/BoatAdForm";
import authService from "@/services/authService";

export default function CreateBoatAdPage() {
  const params = useParams();
  const router = useRouter();
  const { subcategory } = params;
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check auth immediately when page loads
    if (!authService.isAuthenticated()) {
      console.log("User not authenticated, redirecting to login");
      router.push(`/routes/auth/signin?redirect=${encodeURIComponent(`/routes/create-ad/boat/${subcategory}`)}`);
      return;
    }
    
    setLoading(false);
  }, [router, subcategory]);

  // Show a nicer loading indicator
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <BoatAdForm subcategory={subcategory} />
    </div>
  );
}