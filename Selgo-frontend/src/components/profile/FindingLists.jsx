"use client";
import { useState } from "react";
import SearchBar from "../root/SearchBar";
import CardGenericFindingsList from "./CardGenericFindingsList";
export default function FindingsList({ findings = [] }) {
  const [search, setSearch] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [listName, setListName] = useState("");

  const filteredFindings = findings.filter((finding) =>
    finding.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="bg-white py-6 relative">
      {/* Search Bar */}
      <div className="mb-4">
        <SearchBar value={search} onChange={setSearch} placeholder="Search" />
      </div>

      {/* Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600 transition"
        >
          Create a List
        </button>
        <button className="bg-gray-500 text-white px-5 py-2 rounded-md hover:bg-gray-600 transition">
          Customize notification
        </button>
      </div>

      {/* Findings List (Now using GenericFindingsList) */}
      <CardGenericFindingsList findings={filteredFindings} />

      {/* Modal Popup (No Background Change) */}
      {isModalOpen && (
        <div
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-lg shadow-lg w-96 border"
          onClick={(e) => e.stopPropagation()} // Prevent closing when clicking inside
        >
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-800">New List</h2>
            <button
              onClick={() => setIsModalOpen(false)}
              className="text-gray-500 hover:text-black"
            >
              ✕
            </button>
          </div>
          <label className="block text-sm font-medium text-gray-700">Create new list</label>
          <input
            type="text"
            value={listName}
            onChange={(e) => setListName(e.target.value)}
            placeholder="Name"
            className="mt-2 block w-full text-gray-600 p-3 border rounded-md bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            onClick={() => setIsModalOpen(false)}
            className="mt-4 w-full bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600 transition"
          >
            Save
          </button>
        </div>
      )}
    </div>
  );
}