"use client";
import React from "react";
import Image from "next/image";
import Link from "next/link";

const HeroOnlineCar = () => {
  return (
    <div className="w-full bg-teal-700 text-white py-12">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center">
        {/* Left Content */}
        <div className="md:w-1/2 text-center md:text-left space-y-4">
          <p className="text-sm font-semibold">Are you from Selgo?</p>
          <h1 className="text-3xl sm:text-4xl font-bold leading-tight">
            You are at the right place. <br /> We sell the <span className="text-gray-200">cars.</span>
          </h1>
          <p className="text-gray-200">
            We at Nettbil sell your car quickly, safely, and easily. We have 2,260 dealers ready to bid on your car.
          </p>
          {/* Input Field */}
          <div className="flex flex-col items-center gap-2 sm:gap-4 mt-4">
            <input
              type="text"
              placeholder="Registration No."
              className="w-full sm:w-auto bg-white px-4 py-2 rounded-full border-none text-gray-800 focus:ring-2 focus:ring-teal-500"
            />
            <Link href="/routes/online-car/online-car-process">
              <button className="px-10 py-2 bg-teal-500 text-white font-semibold rounded-md hover:bg-teal-800 transition">
                Get Started
              </button>
            </Link>
          </div>
        </div>

        {/* Right Image */}
        <div className="md:w-1/2 mt-8 md:mt-0 flex justify-center">
          <Image
            src="/assets/online-car/car.svg"
            alt="Online Car"
            width={500}
            height={300}
            className="w-full max-w-md md:max-w-lg object-contain"
          />
        </div>
      </div>
    </div>
  );
};

export default HeroOnlineCar;