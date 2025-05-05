"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import { FaGoogle, FaTwitter, FaChevronLeft } from "react-icons/fa";
import Link from "next/link";

const Signup = () => {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [acceptEmails, setAcceptEmails] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const router = useRouter();

  // BACKEND INTEGRATION POINT: Handle OAuth signup redirects
  const handleOAuthSignup = (provider) => {
    if (provider === "google") {
      // window.location.href = "YOUR_BACKEND_GOOGLE_AUTH_URL";
    } else if (provider === "twitter") {
      // window.location.href = "YOUR_BACKEND_TWITTER_AUTH_URL";
    }
  };

  // BACKEND INTEGRATION POINT: Handle signup with FastAPI
  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      // Example: Simulate a successful signup.
      alert("Signup successful!"); // REMOVE THIS AFTER BACKEND INTEGRATION
    } catch (err) {
      setError(err.message || "Failed to sign up");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen relative">
      {/* Left Section (Signup Form) */}
      <div className="w-full md:w-3/5 flex items-center justify-center bg-white px-6 relative">
        {/* Back Button (Mobile - Inside Form) */}
        <button
          onClick={() => router.back()}
          className="absolute top-6 left-6 w-10 h-10 flex items-center justify-center bg-white rounded-full shadow-lg hover:bg-gray-100 transition md:hidden"
        >
          <FaChevronLeft className="text-black text-lg" />
        </button>

        <div className="max-w-3xl w-full px-8">
          <h2 className="text-3xl font-semibold mb-2 text-gray-900">
            Welcome to the shopping community
          </h2>
          <p className="text-gray-600 mb-6">
            Already have an account?{" "}
            <Link href="/routes/auth/signin" className="text-blue-600 hover:underline">
              Log in
            </Link>
          </p>

          {/* Social Logins */}
          <button
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 mb-3 hover:bg-gray-100 transition"
            onClick={() => handleOAuthSignup("google")}
          >
            <FaGoogle className="text-red-500" size={20} />
            Continue with Google
          </button>
          <button
            className="w-full flex items-center text-gray-900 justify-center gap-2 border rounded-full py-2 hover:bg-gray-100 transition"
            onClick={() => handleOAuthSignup("twitter")}
          >
            <FaTwitter className="text-blue-500" size={20} />
            Continue with Twitter
          </button>

          <div className="my-5 flex items-center gap-3">
            <hr className="w-full border-gray-300" />
            <span className="text-gray-500 text-sm">OR</span>
            <hr className="w-full border-gray-300" />
          </div>

          {/* Signup Form */}
          <form onSubmit={handleSignup}>
            <div className="mb-4">
              <label className="block text-gray-700">Email</label>
              <input
                type="email"
                className="w-full border border-gray-400 rounded-lg p-2 mt-1 text-gray-900 placeholder-gray-400 outline-none"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your email"
                required
              />
            </div>

            <div className="mb-4">
              <label className="block text-gray-700">Username</label>
              <input
                type="text"
                className="w-full border border-gray-400 rounded-lg p-2 mt-1 text-gray-900 placeholder-gray-400 outline-none"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Choose a username"
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
                placeholder="Create a password"
                required
              />
              <span
                className="absolute right-3 top-10 text-gray-500 cursor-pointer select-none"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "🙈 Hide" : "👁 Show"}
              </span>
            </div>

            {/* Password Requirements */}
            <div className="text-gray-500 text-sm mb-4 w-full">
              <p className="w-full flex flex-col sm:flex-row justify-between sm:gap-x-5 gap-y-1">
                <span className="w-full sm:w-auto">● Use 9 or more characters</span>
                <span className="w-full sm:w-auto">● One uppercase character</span>
                <span className="w-full sm:w-auto">● One lowercase character</span>
              </p>
              <p className="w-full flex flex-col sm:flex-row justify-start sm:gap-x-5 gap-y-1">
                <span className="w-full sm:w-auto">● One special character</span>
                <span className="w-full sm:w-auto">● One number</span>
              </p>
            </div>

            {/* Email Subscription */}
            <div className="flex items-start gap-2 mb-4">
              <input
                type="checkbox"
                id="acceptEmails"
                checked={acceptEmails}
                onChange={() => setAcceptEmails(!acceptEmails)}
                className="mt-1"
              />
              <label htmlFor="acceptEmails" className="text-gray-700 text-sm">
                I want to receive emails about the product, feature updates,
                events, and marketing promotions.
              </label>
            </div>

            {/* Terms & Privacy */}
            <p className="text-sm text-gray-600 mb-4">
              By creating an account, you agree to the{" "}
              <Link href="#" className="text-blue-600 hover:underline">
                Terms of use
              </Link>{" "}
              and{" "}
              <Link href="#" className="text-blue-600 hover:underline">
                Privacy Policy
              </Link>.
            </p>

            {/* Error Message */}
            {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

            {/* Signup Button */}
            <button
              type="submit"
              className="w-1/5 bg-teal-500 text-white py-2 rounded-lg mt-2 hover:bg-teal-600 transition"
              disabled={loading}
            >
              {loading ? "Signing up..." : "Sign up"}
            </button>

            <p className="text-sm text-gray-600 mt-4">
              Already have an account?{" "}
              <Link href="/routes/auth/signin" className="text-blue-600 hover:underline">
                Log in
              </Link>
            </p>
          </form>
        </div>
      </div>

      {/* Right Section (Image) */}
      <div className="hidden md:flex w-2/5 relative">
        <Image
          src="/assets/signin/2-signup.png"
          alt="Signup"
          fill
          style={{ objectFit: "cover" }}
        />

        {/* Back Button (Desktop - Inside Image) */}
        <button
          onClick={() => router.back()}
          className="absolute top-6 left-6 w-10 h-10 flex items-center justify-center bg-white rounded-full shadow-lg hover:bg-gray-100 transition"
        >
          <FaChevronLeft className="text-black text-lg" />
        </button>
      </div>
    </div>
  );
};

export default Signup;