"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Image from "next/image";
import { FaGoogle, FaTwitter, FaChevronLeft } from "react-icons/fa";
import useAuthStore from "@/store/store";
import authService from "@/services/authService"; // Use real auth service
import Link from "next/link";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [redirectUrl, setRedirectUrl] = useState("/");
  
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setUser, fetchUser } = useAuthStore();

  // Get the redirect URL from query parameters if it exists
  useEffect(() => {
    const redirect = searchParams.get("redirect");
    if (redirect) {
      setRedirectUrl(redirect);
    }
  }, [searchParams]);

  // Handle Real Login
 const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await authService.login({
        username: email, // API accepts username, which can be email
        password: password
      });

      // Store tokens and user data
      localStorage.setItem('accessToken', response.access_token);
      localStorage.setItem('refreshToken', response.refresh_token);
      localStorage.setItem('user', JSON.stringify(response.user));

      setUser(response.user); // Update Zustand Store
      
      // Get redirect URL from current page URL
      const currentUrl = new URL(window.location.href);
      const redirectParam = currentUrl.searchParams.get('redirect');
      
      console.log("🔍 Login redirect debug:");
      console.log("  Current full URL:", window.location.href);
      console.log("  Redirect parameter:", redirectParam);
      
      if (redirectParam) {
        const decodedRedirect = decodeURIComponent(redirectParam);
        console.log("✅ Redirecting to:", decodedRedirect);
        
        // NUCLEAR OPTION: Replace entire browser history
        window.history.replaceState(null, null, decodedRedirect);
        window.location.replace(decodedRedirect);
      } else {
        console.log("🏠 No redirect parameter, going to home");
        window.history.replaceState(null, null, '/');
        window.location.replace('/');
      }
    } catch (err) {
      console.error("Login error:", err);
      setError(err.detail || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

   // Handle OAuth Login (Google)
  const handleGoogleLogin = async () => {
    try {
      // For now, show a message that OAuth is not implemented
      alert("Google OAuth is not yet implemented. Please use email/password login.");
    } catch (error) {
      console.error("Google login error:", error);
    }
  };

  // Handle OAuth Login (Twitter)
  const handleTwitterLogin = async () => {
    try {
      // For now, show a message that OAuth is not implemented
      alert("Twitter OAuth is not yet implemented. Please use email/password login.");
    } catch (error) {
      console.error("Twitter login error:", error);
    }
  };

  // Handle custom back behavior
  const handleBack = () => {
    if (redirectUrl !== "/" && redirectUrl !== "") {
      router.push("/");
    } else {
      router.back();
    }
  };

  // Fetch User if Cookie Exists (Optional for Refresh Handling)
  // useEffect(() => {
  //   fetchUser();
  // }, [fetchUser]);



  return (
    <div className="flex h-screen relative">
      {/* Left Section */}
      <div className="hidden md:flex w-1/2 relative">
        <Image
          src="/assets/signin/1-shop-with-us.png"
          alt="Shop with us"
          fill
          style={{ objectFit: "cover" }}
        />

        {/* Back Button (Desktop - Inside Image) */}
        <button
          onClick={handleBack}
          className="absolute top-6 left-6 w-10 h-10 flex items-center justify-center bg-white rounded-full shadow-lg hover:bg-gray-100 transition"
        >
          <FaChevronLeft className="text-black text-lg" />
        </button>
      </div>

      {/* Right Section (Login Form) */}
      <div className="w-full md:w-1/2 flex items-center justify-center bg-white relative">
        {/* Back Button (Mobile - Inside Login Form) */}
        <button
          onClick={handleBack}
          className="absolute top-6 left-6 w-10 h-10 flex items-center justify-center bg-white rounded-full shadow-lg hover:bg-gray-100 transition md:hidden"
        >
          <FaChevronLeft className="text-black text-lg" />
        </button>

           {/* Top-right Signup Link */}
        <div className="absolute top-6 right-6 text-sm text-gray-600">
          Don&apos;t have an account?{" "}
          <Link href="/routes/auth/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </div>

         <div className="max-w-sm w-full px-8">
          <h2 className="text-2xl font-semibold mb-6 text-gray-800">Sign in</h2>

          {/* Social Logins */}
           <button
            type="button"
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 mb-3 hover:bg-gray-100 transition"
            onClick={handleGoogleLogin}
          >
            <FaGoogle className="text-red-500" size={20} />
            Continue with Google
          </button>
          <button
            type="button"
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 hover:bg-gray-100 transition"
            onClick={handleTwitterLogin}
          >
           <FaTwitter className="text-blue-500" size={20} />
            Continue with Twitter
          </button>

           <div className="my-5 flex items-center gap-3">
            <hr className="w-full border-gray-300" />
            <span className="text-gray-500 text-sm">OR</span>
            <hr className="w-full border-gray-300" />
          </div>

          {/* Sign-in Form */}
            <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-gray-700">Email address</label>
              <input
                type="email"
                className="w-full border border-gray-400 rounded-lg p-2 mt-1 text-gray-900 placeholder-gray-400 outline-none"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>

              <div className="mb-4 relative">
              <label className="block text-gray-700">Password</label>
              <input
                type={showPassword ? "text" : "password"}
                className="w-full border border-gray-400 rounded-lg p-2 mt-1 text-gray-900 placeholder-gray-400 outline-none"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
              <span
                className="absolute right-3 top-10 text-gray-500 cursor-pointer select-none"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "🙈 Hide" : "👁 Show"}
              </span>
            </div>

            {/* Error Message */}
             {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

            {/* Forget Password */}
         <div className="flex justify-end items-center">
              <a
                href="#"
                className="text-sm underline text-gray-600 hover:underline"
              >
                Forget your password?
              </a>
            </div>

            <button
              type="submit"
              className="w-1/3 bg-teal-400 text-white py-2 rounded-lg mt-4 hover:bg-teal-500 transition"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;