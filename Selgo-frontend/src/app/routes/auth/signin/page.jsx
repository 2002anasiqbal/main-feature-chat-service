"use client";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import useAuthStore from "@/store/store";
import Login from "@/components/authentication/Login";

export default function SignIn() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user, isAuthenticated } = useAuthStore();
  const [redirectUrl, setRedirectUrl] = useState(null);

  useEffect(() => {
    // Get redirect URL from search params
    const redirect = searchParams.get('redirect');
    setRedirectUrl(redirect);
    
    console.log("🔍 SignIn page debug:");
    console.log("  Redirect from URL:", redirect);
    console.log("  Current URL:", window.location.href);
  }, [searchParams]);

  // Redirect logged-in users away from login page
  useEffect(() => {
    if (isAuthenticated() && user) {
      console.log("✅ User already logged in, redirecting to home");
      router.replace("/");
    }
  }, [user, isAuthenticated, router]);

  // Don't show login form if user is already logged in
  if (isAuthenticated() && user) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Logging in, redirecting...</p>
        </div>
      </div>
    );
  }

  return <Login redirectUrl={redirectUrl} />;
}