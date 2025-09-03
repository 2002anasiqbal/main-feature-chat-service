"use client";
import React from "react";
import { FaInfoCircle } from "react-icons/fa";

const tools = [
  {
    title: "Car Guide",
    description: "Here you find tips and tricks about car guide",
    buttonText: "Show More",
  },
  {
    title: "Loan calculator",
    description: "Use loan calculator to see about car loans.",
    buttonText: "Show More",
  },
  {
    title: "Car worth",
    description: "Know the worth of your car",
    buttonText: "Show More",
  },
];

export default function UsefulTools() {
  return (
    <div className="py-10">
      {/* Section Title */}
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Useful Tools</h2>

      {/* Cards Section */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {tools.map((tool, index) => (
          <div key={index} className="border rounded-lg p-6 text-center shadow-sm bg-white">
            {/* Icon */}
            <FaInfoCircle className="text-teal-500 text-2xl mx-auto mb-3" />

            {/* Title */}
            <h3 className="text-lg font-semibold text-gray-900">{tool.title}</h3>

            {/* Description */}
            <p className="text-sm text-gray-600 mt-2">{tool.description}</p>

            {/* Button */}
            <button className="mt-4 px-4 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-100 transition">
              {tool.buttonText}
            </button>
          </div>
        ))}
      </div>

      {/* Insure Car Button */}
      <div className="mt-8 text-center">
        <button className="px-6 py-3 bg-teal-500 text-white font-semibold rounded-md hover:bg-teal-600 transition">
          Insure your Car
        </button>
      </div>
    </div>
  );
}