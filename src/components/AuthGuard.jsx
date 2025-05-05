"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import useAuthStore from "@/store/store";
import protectedRoutes from "@/config/protectedRoutes";

const AuthGuard = ({ children }) => {
  const router = useRouter();
  const pathname = usePathname();
  const { user, fetchUser, isAuthenticated } = useAuthStore();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if current route is protected
    if (protectedRoutes.includes(pathname)) {
      if (!isAuthenticated()) {
        // Include the original path as a redirect parameter
        router.push(`/routes/auth/signin?redirect=${encodeURIComponent(pathname)}`);
      } else {
        fetchUser().finally(() => setLoading(false));
      }
    } else {
      setLoading(false); // Allow access to non-protected routes
    }
  }, [pathname, isAuthenticated, fetchUser, router]);

  if (loading) {
    return <div className="flex h-screen items-center justify-center text-gray-600">Loading...</div>;
  }

  return <>{children}</>;
};

export default AuthGuard;