// File: selgo-frontend/src/components/AuthGuard.jsx

"use client";
import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import useAuthStore from "@/store/store";
import protectedRoutes from "@/config/protectedRoutes";
import authService from "@/services/authService";

const AuthGuard = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { user, fetchUser } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  // Fix hydration mismatch by only running client-side
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (!mounted) return; // Don't run until mounted

    const checkAuth = async () => {
      // Check if current route needs protection
      const isProtectedRoute = protectedRoutes.some(route => {
        if (typeof route === 'string') {
          if (pathname === route) {
            return true;
          }
          // Handle pattern routes like '/routes/create-ad/*'
          if (route.endsWith('*')) {
            const basePath = route.slice(0, -1);
            return pathname.startsWith(basePath);
          }
        }
        return false;
      });

      if (isProtectedRoute) {
        console.log(`🔒 Protected route detected: ${pathname}`);
        
        // Check authentication first
        const isAuth = authService.isAuthenticated();
        console.log(`🔍 Authentication check: ${isAuth}`);

        if (!isAuth) {
          console.log(`❌ User not authenticated, redirecting to login`);
          // FIXED: Use router.replace() instead of router.push()
          router.replace(`/routes/auth/signin?redirect=${encodeURIComponent(pathname)}`);
          return;
        }

        // If authenticated but no user in store, fetch user data
        if (!user) {
          console.log(`👤 Fetching user data...`);
          try {
            await fetchUser();
          } catch (error) {
            console.error("Failed to fetch user:", error);
            // FIXED: Use router.replace() instead of router.push()
            router.replace(`/routes/auth/signin?redirect=${encodeURIComponent(pathname)}`);
            return;
          }
        }

        console.log(`✅ Access granted to: ${pathname}`);
      } else {
        console.log(`🌐 Public route: ${pathname}`);
      }
      
      setLoading(false);
    };

    checkAuth();
  }, [mounted, pathname, user, fetchUser, router]);

  // Don't render anything until mounted (prevents hydration mismatch)
  if (!mounted) {
    return null;
  }

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