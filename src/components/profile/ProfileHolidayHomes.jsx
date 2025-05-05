"use client";
import { useState } from "react";
import SearchBar from "../root/SearchBar";

export default function ProfileHolidayHomes() {
  const [activeTab, setActiveTab] = useState("rental"); // Default to "rental"

  return (
    <div className="bg-white py-6">
      {/* Search Bar */}
      <div className="mb-6">
        <SearchBar placeholder="Search" className="w-full" />
      </div>

      {/* Title */}
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">
        Holiday homes and cabins in Norway
      </h2>

      {/* Toggle Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab("rent")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "rent"
              ? "bg-gray-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          Rent
        </button>
        <button
          onClick={() => setActiveTab("rental")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "rental"
              ? "bg-teal-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          Rental
        </button>
      </div>

      {/* Message for Empty Listings */}
      <div className="text-center text-gray-500">
        None of your ads have received any requests yet
      </div>
    </div>
  );
}