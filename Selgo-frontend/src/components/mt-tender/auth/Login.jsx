"use client";
import { useState } from "react";
import Link from "next/link";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-[#dbeeee] px-4">
      {/* Form Container */}
      <div className="w-full max-w-md space-y-6">
        {/* Email Input */}
        <div className="relative">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="peer w-full border-2 border-[#5b4c83] rounded-md px-4 pt-6 pb-2 text-gray-800 placeholder-transparent focus:outline-none focus:border-teal-600"
            placeholder="Enter Email"
          />
          <label className="absolute left-4 top-2 text-sm text-[#5b4c83] peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 transition-all duration-200">
            Enter Email
          </label>
        </div>

        {/* Password Input */}
        <div className="relative">
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="peer w-full border-2 border-[#5b4c83] rounded-md px-4 pt-6 pb-2 text-gray-800 placeholder-transparent focus:outline-none focus:border-teal-600"
            placeholder="Enter Password"
          />
          <label className="absolute left-4 top-2 text-sm text-[#5b4c83] peer-placeholder-shown:top-4 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 transition-all duration-200">
            Enter Password
          </label>
        </div>

        {/* Button */}
        <button className="w-full bg-teal-600 text-white py-2 rounded-md hover:bg-teal-700 transition">
          Next
        </button>

        {/* Divider */}
        <div className="border-t border-gray-300 my-4" />

        {/* Bottom Links */}
        <div className="flex flex-col items-center space-y-2 text-teal-700 text-sm">
          <Link href="#">Forget</Link>
          <Link href="#">Register a new business</Link>
          <Link href="#">Post a job</Link>
        </div>
      </div>
    </div>
  );
}
