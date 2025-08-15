"use client";
import { useState } from "react";

export default function MyAds() {
  const [search, setSearch] = useState("");

  return (
    <div className="bg-white py-6">
      {/* Heading */}
      <h1 className="text-2xl font-semibold text-gray-800 mb-4">My ads</h1>

      {/* Search Bar */}
      <div className="mb-4">
        <label className="block text-sm text-gray-600">Search ad content</label>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="mt-1 block w-full p-3 border rounded-md text-gray-600 bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Search..."
        />
      </div>

      {/* Description */}
      <p className="text-gray-700 mb-6">
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
        Lorem Ipsum has been the industry’s standard dummy text ever since the 1500s, 
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
      </p>

      {/* Button */}
      <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600 transition">
        Button
      </button>
    </div>
  );
}
