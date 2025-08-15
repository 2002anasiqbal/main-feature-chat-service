"use client";
import React from "react";

export default function HeroWithCategories() {
  return (
    <>
      {/* HERO SECTION */}
      <section className="bg-[#E8F1F3]">
        <div className="max-w-7xl mx-auto px-4 py-10 flex flex-col md:flex-row items-center gap-8">
          <div className="md:w-1/2">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Get the job done!</h1>
            <p className="text-gray-700 mb-6 max-w-md">
              Describe the job and receive offers from skilled professionals.
              Free and without obligation.
            </p>
            <div className="relative w-full max-w-md">
              <input
                type="text"
                placeholder="What do you need help with?"
                className="w-full pl-4 pr-12 py-2 text-gray-600 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
              <button className="absolute right-3 top-1/2 -translate-y-1/2">
                <img src="/assets/my-tender/1.svg" alt="Search" className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="md:w-1/2">
            <img src="/assets/my-tender/2.svg" alt="Hero illustration" className="w-full h-auto" />
          </div>
        </div>
      </section>

      {/* CATEGORY ICONS */}
      <section className="relative bg-white mx-4 sm:mx-10 lg:mx-20 -mt-10 rounded-xl shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-8 gap-4">
            {[
              { icon: "3", label: "Craft" },
              { icon: "4", label: "Renovate the bathroom" },
              { icon: "5", label: "Car workshop" },
              { icon: "6", label: "XL large project" },
              { icon: "7", label: "Cleaning" },
              { icon: "8", label: "Housing" },
              { icon: "9", label: "Transport" },
              { icon: "10", label: "Others" },
            ].map(({ icon, label }, index) => (
              <div key={index} className="flex flex-col items-center text-center">
                <img src={`/assets/my-tender/${icon}.svg`} alt={label} className="mb-2 w-10 h-10" />
                <span className="text-sm font-medium text-gray-700">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
