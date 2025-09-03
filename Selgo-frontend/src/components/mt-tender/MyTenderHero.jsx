"use client";
import Image from "next/image";
import React from "react";

export default function MyTenderHero() {
  return (
    <section className="w-full max-w-7xl mx-auto px-4 md:px-6">
      <div className="flex flex-col lg:flex-row items-center">
        {/* Left Image */}
        <div className="w-full lg:w-1/2 flex justify-center items-center p-4">
          <img
            src="/assets/my-tender/30.svg"
            alt="My Tender Hero"
            className="w-full h-auto max-h-[500px] object-contain rounded-lg shadow-lg"
          />
        </div>

        {/* Right Content */}
        <div className="w-full lg:w-1/2 p-6 lg:p-10 space-y-5">
          <span className="inline-block bg-yellow-100 text-yellow-800 text-xs font-medium px-2 py-1 rounded">
            New
          </span>

          <h2 className="text-2xl md:text-3xl font-semibold text-gray-900">
            My tender{" "}
            <span className="relative inline-block font-bold text-gray-900">
              XL
              <Image
                src="/assets/my-tender/29.svg"
                alt="Underline XL"
                width={40}
                height={12}
                className="absolute left-0 bottom-0 transform translate-y-0"
              />
            </span>
            <br />
            For big projects!
          </h2>

          <ul className="text-sm text-gray-700 space-y-1 list-none">
            <li>· We match your project with 3 qualified companies</li>
            <li>· Get a personal project supervisor throughout the entire project</li>
            <li>· The service is completely free and non-binding</li>
          </ul>

          <button className="mt-3 inline-block bg-teal-600 text-white px-5 py-2 rounded hover:bg-teal-700 transition">
            Get started
          </button>
        </div>
      </div>
    </section>
  );
}
