"use client";
import { useState } from "react";
import Link from "next/link";

export default function FindFlight({ searchRoute = "/" }) {
  const [tripType, setTripType] = useState("Return Trip");

  return (
    <div className="w-full mx-auto bg-transparent text-white">
      {/* Tabs Section */}
      <div className="bg-white px-4 rounded-t-lg flex flex-wrap justify-center">
        {["Return Trip", "One way", "More cities"].map((type) => (
          <button
            key={type}
            className={`
              py-2 text-sm font-medium transition-all 
              px-4 sm:px-8 md:px-12 
              rounded-t-md 
              ${tripType === type ? "bg-teal-700 text-white" : "text-gray-600 hover:text-gray-800"}
            `}
            onClick={() => setTripType(type)}
          >
            {type}
          </button>
        ))}
      </div>

      {/* Flight Search Form */}
      <div className="bg-teal-700 p-4 sm:p-6 rounded-b-lg shadow-md">
        {/* 
          Use a responsive grid:
          1 column on small screens,
          2 columns on sm,
          5 columns on md 
        */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-4">
          <div>
            <label className="text-white text-sm">Fly from</label>
            <input
              type="text"
              placeholder="Airport"
              className="w-full p-2 border border-gray-300 text-gray-700 bg-white placeholder-gray-400"
            />
          </div>
          <div>
            <label className="text-white text-sm">Fly to</label>
            <input
              type="text"
              placeholder="Airport"
              className="w-full p-2 border border-gray-300 text-gray-700 bg-white placeholder-gray-400"
            />
          </div>
          <div>
            <label className="text-white text-sm">Departure</label>
            <input
              type="date"
              className="w-full p-2 border border-gray-300 text-gray-700 bg-white"
            />
          </div>
          <div>
            <label className="text-white text-sm">Home journey</label>
            <input
              type="date"
              className="w-full p-2 border border-gray-300 text-gray-700 bg-white"
            />
          </div>
          <div>
            <label className="text-white text-sm">Traveler</label>
            <select className="w-full p-2 border border-gray-300 text-gray-700 bg-white">
              <option>1 adult, Economy</option>
              <option>2 adults, Business</option>
              <option>3 adults, First Class</option>
            </select>
          </div>
        </div>

        {/* Checkboxes & Search Button */}
        <div className="mt-4 space-y-2">
          <label className="flex items-center text-white">
            <input type="checkbox" className="mr-2" />
            Search for hotels
          </label>
          <Link href={searchRoute || "/"}>
            <button className="w-full sm:w-auto px-4 py-2 bg-white text-teal-700 rounded-md font-semibold hover:bg-gray-100">
              Search
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}
