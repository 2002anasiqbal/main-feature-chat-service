"use client";

import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Image from "next/image";
import { FaGoogle, FaTwitter, FaChevronLeft } from "react-icons/fa";
import useAuthStore from "@/store/store";
import { mockLogin, mockFetchUser } from "@/utils/mockAuth";
import Cookies from "js-cookie"; // For simulated JWT storage
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

  // Handle Mock Login
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await mockLogin({ email, password });

      // Store the token in cookies (for simulation)
      Cookies.set("auth_token", response.token, { expires: 1 });

      setUser(response.user); // Update Zustand Store
      router.push(redirectUrl); // Redirect to the original URL or dashboard
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  // Fetch User if Cookie Exists (Optional for Refresh Handling)
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  // Handle custom back behavior
  const handleBack = () => {
    // If we have a redirect URL that's not the home page, 
    // we should navigate directly to a safe page instead of going back
    if (redirectUrl !== "/" && redirectUrl !== "") {
      router.push("/"); // Go to a safe public page like home
    } else {
      router.back(); // Use regular back behavior for normal cases
    }
  };

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
          Don't have an account?{" "}
          <Link href="/routes/auth/signup" className="text-blue-600 hover:underline">
            Sign up
          </Link>
        </div>

        <div className="max-w-sm w-full px-8">
          <h2 className="text-2xl font-semibold mb-6 text-gray-800">Sign in</h2>

          {/* Social Logins */}
          <button
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 mb-3 hover:bg-gray-100 transition"
            onClick={() => console.log("Redirecting to Google OAuth...")}
          >
            <FaGoogle className="text-red-500" size={20} />
            Continue with Google
          </button>
          <button
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 hover:bg-gray-100 transition"
            onClick={() => console.log("Redirecting to Twitter OAuth...")}
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