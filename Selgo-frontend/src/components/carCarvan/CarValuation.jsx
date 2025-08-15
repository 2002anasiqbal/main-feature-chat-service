"use client";
import React, { useState } from "react";
import Image from "next/image";

export default function CarValuation() {
  const [formData, setFormData] = useState({
    registration: "",
    mileage: "",
  });

  // Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="flex flex-col md:flex-row items-center justify-between bg-white p-6 mb-20 rounded-lg shadow-md w-full">
      {/* Left Section */}
      <div className="flex flex-col w-full md:w-2/3">
        <h2 className="text-lg font-semibold text-gray-900">Are you going to sell the car?</h2>
        <p className="text-sm text-gray-700">
          Gain insights into car value and find the best way to sell it.
        </p>

        {/* Input Fields */}
        <div className="flex flex-col md:flex-row gap-4 mt-4">
          {/* Registration No. */}
          <div className="flex flex-col w-full">
            <label className="text-sm font-medium text-gray-800">Registration No.</label>
            <input
              type="text"
              name="registration"
              value={formData.registration}
              onChange={handleChange}
              placeholder="11024-K-67"
              className="border border-gray-400 p-2 rounded-md w-full text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          {/* Mileage */}
          <div className="flex flex-col w-full">
            <label className="text-sm font-medium text-gray-800">Mileage</label>
            <input
              type="text"
              name="mileage"
              value={formData.mileage}
              onChange={handleChange}
              placeholder="1000 km"
              className="border border-gray-400 p-2 rounded-md w-full text-gray-900 bg-white focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>
        </div>
      </div>

      {/* Right Section: Car Image & Button */}
      <div className="flex flex-col items-center justify-center mt-6 md:mt-0">
        {/* Car Image */}
        <Image
          src="/assets/carcarvan/car.svg"
          alt="Car Image"
          width={140}
          height={80}
          className="object-contain"
        />

        {/* Check Car Button */}
        <button className="mt-4 px-6 py-2 bg-teal-500 text-white font-semibold rounded-md hover:bg-teal-600">
          Check car
        </button>
      </div>
    </div>
  );
}