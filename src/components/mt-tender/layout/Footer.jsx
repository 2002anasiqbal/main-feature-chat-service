"use client";
import Image from "next/image";
import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 px-4 py-8">
      <div className="max-w-7xl mx-auto w-full flex flex-col md:flex-row justify-between gap-8">
        {/* Left Logo + Info */}
        <div className="md:w-1/4">
          <Image
            src="/assets/my-tender/logo.svg"
            alt="Mittanbud"
            width={160}
            height={80}
            className="mb-2"
          />
          <p className="text-sm text-gray-600">Schibsted Norge</p>
          <p className="text-sm text-gray-600">SMB © 2024</p>
        </div>

        {/* Footer Links - take remaining space evenly */}
        <div className="flex-1 grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {/* About */}
          <div>
            <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">About</h4>
            {["Press", "Carrier", "Contact", "Privacy", "Site map"].map((item, i) => (
              <Link key={i} href="/" className="block text-sm text-gray-700 hover:underline">
                {item}
              </Link>
            ))}
          </div>

          {/* Private Person */}
          <div>
            <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Private Person</h4>
            {["Current affair", "Inspiraton", "Help center", "Reference", "Start guide"].map((item, i) => (
              <Link key={i} href="/" className="block text-sm text-gray-700 hover:underline">
                {item}
              </Link>
            ))}
          </div>

          {/* Prof */}
          <div>
            <h4 className="text-sm font-semibold text-gray-500 uppercase mb-2">Prof</h4>
            {["Current affair", "Reference", "Register your company", "Start guide", "Tool box"].map((item, i) => (
              <Link key={i} href="/" className="block text-sm text-gray-700 hover:underline">
                {item}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
