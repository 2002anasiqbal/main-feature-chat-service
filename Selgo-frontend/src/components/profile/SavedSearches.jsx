"use client";
import React from "react";

export default function SavedSearches({ searches = [] }) {
  return (
    <div className="bg-white py-6 ">
      {/* Title */}
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Saved Searches</h2>

      {/* Saved Searches List */}
      {searches.length > 0 ? (
        <ul className="space-y-4">
          {searches.map((search, index) => (
            <li key={index} className="p-4 border rounded-lg shadow-sm flex justify-between">
              <span className="font-semibold text-gray-800">{search.title}</span>
              <button 
                className="text-teal-500 hover:underline"
                onClick={() => alert(`Opening search: ${search.title}`)}
              >
                View
              </button>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-center text-gray-500">
          None of your ads have received any requests yet
        </div>
      )}
    </div>
  );
}