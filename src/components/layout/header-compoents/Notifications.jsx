"use client";
import { useState } from "react";

export default function Notifications() {
  const [activeTab, setActiveTab] = useState("saved");

  return (
    <div className="w-full min-h-screen bg-white py-8">
      <div className="">
        {/* Header Section */}
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl text-gray-900 font-bold">Notifications</h1>
          <button className="border border-gray-400 text-gray-700 px-3 py-1 rounded-md text-sm hover:bg-gray-100">
            Mark all as read
          </button>
        </div>

        {/* Tabs */}
        <div className="flex space-x-6 border-b border-gray-300 pb-2">
          <button
            onClick={() => setActiveTab("saved")}
            className={`text-gray-800 font-medium ${
              activeTab === "saved" ? "border-b-2 border-black pb-1" : "hover:text-gray-600"
            }`}
          >
            Saved searches
          </button>
          <button
            onClick={() => setActiveTab("check")}
            className={`text-gray-800 font-medium ${
              activeTab === "check" ? "border-b-2 border-black pb-1" : "hover:text-gray-600"
            }`}
          >
            Check this out
          </button>
        </div>

        {/* Content */}
        <div className="flex justify-center items-center h-64 text-gray-500">
          {activeTab === "saved" ? "There is nothing to show" : "There is nothing to show"}
        </div>
      </div>
    </div>
  );
}