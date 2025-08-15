"use client";
import Image from "next/image";
import React from "react";

export default function AdviceInspiration() {
  return (
    <section className="w-full max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-16">
      {/* Section Heading */}
      <div className="mb-10">
        <h2 className="text-2xl font-semibold text-gray-900">
          Advice and inspiration
        </h2>
        <p className="text-sm text-gray-600 mt-2">
          Here you will get good advice and inspiration for your next building
          and renovation project
        </p>
      </div>

      {/* Top Large Image */}
      
      <div className="mb-8 text-center">
        <img
          src="/assets/my-tender/31.svg"
          alt="Handcraft dictionary"
          className="mx-auto w-full max-w-screen-md rounded-lg"
        />
        <p className="text-xs text-gray-700 mt-2">
          Handcraft dictionary from Ato Z
        </p>
      </div>

      {/* Bottom Three Images */}
      <div className="flex justify-center items-center gap-10 pb-20">
        <div className="text-center">
          <img
            src="/assets/my-tender/32.svg"
            alt="Handcraft dictionary"
            className="w-full max-w-xs rounded-md"
          />
          <p className="text-xs text-gray-700 mt-2">
            Handcraft dictionary from Ato Z
          </p>
        </div>
        <div className="text-center">
          <img
            src="/assets/my-tender/33.svg"
            alt="Handcraft dictionary"
            className="w-full max-w-xs rounded-md"
          />
          <p className="text-xs text-gray-700 mt-2">
            Handcraft dictionary from Ato Z
          </p>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center">
        <Image
          src="/assets/my-tender/34.svg" 
          alt="Mittanbud Proff"
          width={200}
          height={100}
          className="mx-auto mb-4"
        />
        <h3 className="text-xl text-gray-600 font-semibold mb-3">Do you have a business?</h3>
        <button className="bg-teal-600 text-white px-6 py-2 rounded hover:bg-teal-700 transition">
          Send Message
        </button>
      </div>
    </section>
  );
}
