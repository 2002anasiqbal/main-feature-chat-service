"use client";
import React from "react";

export default function HeroAndCategories() {
  return (
    <>
      {/* HERO SECTION */}
      <section className="bg-[#E8F1F3]">
        <div className="max-w-7xl mx-auto px-4 py-10 flex flex-col md:flex-row items-center gap-8">
          {/* Left text & input */}
          <div className="md:w-1/2">
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Get the job done!
            </h1>
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
              {/* Arrow icon */}
              <button className="absolute right-3 top-1/2 -translate-y-1/2">
                <img
                  src="/assets/my-tender/1.svg"
                  alt="Search arrow"
                  className="w-5 h-5"
                />
              </button>
            </div>
          </div>

          {/* Right image */}
          <div className="md:w-1/2">
            <img
              src="/assets/my-tender/2.svg"
              alt="Hero illustration"
              className="w-full h-auto"
            />
          </div>
        </div>
      </section>

      {/* CATEGORY ICONS SECTION */}
      <section className="relative bg-white mx-20 -top-18 rounded-xl shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-8 gap-4">
            {/* Example categories with their SVGs */}
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/3.svg"
                alt="Craft"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">Craft</span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/4.svg"
                alt="Renovate the bathroom"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Renovate the bathroom
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/5.svg"
                alt="Car workshop"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Car workshop
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/6.svg"
                alt="XL large project"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                XL large project
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/7.svg"
                alt="Cleaning"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Cleaning
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/8.svg"
                alt="Housing"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Housing
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/9.svg"
                alt="Transport"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Transport
              </span>
            </div>
            <div className="flex flex-col items-center text-center">
              <img
                src="/assets/my-tender/10.svg"
                alt="Others"
                className="mb-2 w-10 h-10"
              />
              <span className="text-sm font-medium text-gray-700">
                Others
              </span>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
