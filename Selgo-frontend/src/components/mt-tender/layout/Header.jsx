"use client";
import Image from "next/image";
import Link from "next/link";
import { FaBars } from "react-icons/fa";

export default function Header() {
  return (
    <header className="w-full bg-white shadow-sm py-2 px-4">
      {/* Mobile Top Row: Burger & Logo */}
      <div className="flex items-center justify-between md:hidden">
        <button className="text-gray-700 text-xl">
          <FaBars />
        </button>

        <Link href="/">
          <Image
            src="/assets/my-tender/logo.svg"
            alt="Mittanbud Logo"
            width={140}
            height={40}
            className="h-auto w-auto"
          />
        </Link>
      </div>

      {/* Mobile Bottom Row: Log in, Register, Post Job */}
      <div className="mt-3 flex justify-between md:hidden text-sm text-gray-800 items-center">
        <Link href="/routes/my-tender/login" className="hover:underline">
          Log in
        </Link>
        <Link href="/routes/my-tender/register" className="hover:underline">
          Register
        </Link>
        <Link href="/routes/my-tender/category">
          <button className="bg-teal-700 hover:bg-teal-800 text-white font-semibold px-4 py-2 rounded-md cursor-pointer">
            Post a Job
          </button>
        </Link>
      </div>

      {/* Desktop Layout */}
      <div className="hidden md:flex items-center justify-between">
        {/* Left Side: Hamburger + Logo + Menu */}
        <div className="flex items-center space-x-4">
          <button className="text-gray-700 text-xl">
            <FaBars />
          </button>
          <Link href="/">
            <Image
              src="/assets/my-tender/logo.svg"
              alt="Mittanbud Logo"
              width={160}
              height={40}
              className="h-auto w-auto"
            />
          </Link>
          <div className="text-sm text-gray-700 ml-2 cursor-pointer flex items-center">
            Menu
          </div>
        </div>

        {/* Right Side */}
        <div className="flex items-center space-x-4">
          <Link href="/routes/my-tender/login" className="text-sm text-gray-800 hover:underline">
            Log in
          </Link>
          <Link href="/routes/my-tender/registration" className="text-sm text-gray-800 hover:underline">
            Register
          </Link>
          <Link href="/routes/my-tender/category">
            <button className="bg-teal-700 hover:bg-teal-800 text-white text-sm px-4 py-2 rounded-md cursor-pointer">
              Post a Job
            </button>
          </Link>
        </div>
      </div>
    </header>
  );
}
