// File: C:\Users\Amjad Khalil\OneDrive\Desktop\Selggo\selgo-frontend\components\AuthGuard.jsx

"use client";
import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import useAuthStore from "@/store/store";
import protectedRoutes from "@/config/protectedRoutes";
import authService from "@/services/authService";

const AuthGuard = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { fetchUser } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if current route needs protection
    const isProtectedRoute = protectedRoutes.some(route => {
      if (typeof route === 'string') {
        return pathname === route;
      }
      // Handle pattern routes like '/routes/create-ad/*'
      if (route.endsWith('*')) {
        const basePath = route.slice(0, -1);
        return pathname.startsWith(basePath);
      }
      return false;
    });

    if (isProtectedRoute) {
      console.log(`Protected route detected: ${pathname}`);
      
      // Check if user is authenticated
      if (!authService.isAuthenticated()) {
        console.log(`User not authenticated, redirecting to login`);
        
        // Redirect to login immediately
        router.push(`/routes/auth/signin?redirect=${encodeURIComponent(pathname)}`);
        return; // Skip the rest of this effect
      } else {
        // User is authenticated, fetch user data
        fetchUser().finally(() => setLoading(false));
      }
    } else {
      // Not a protected route, no need to check auth
      setLoading(false);
    }
  }, [pathname, fetchUser, router]);

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  return <>{children}</>;
};

export default AuthGuard;