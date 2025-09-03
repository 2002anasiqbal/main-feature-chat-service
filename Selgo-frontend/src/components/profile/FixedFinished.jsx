"use client";
import { useState } from "react";
import SearchBar from "../root/SearchBar";

export default function FixedFinished() {
  const [activeTab, setActiveTab] = useState("sell"); // "sell" or "purchase"

  // Mock data for listings
  const mySellings = [
    { id: 1, title: "Gaming Laptop", status: "Sold" },
    { id: 2, title: "Smartphone", status: "Available" },
  ];

  const myPurchases = [
    { id: 1, title: "Office Chair", status: "Delivered" },
    { id: 2, title: "Headphones", status: "Pending" },
  ];

  const activeList = activeTab === "sell" ? mySellings : myPurchases;

  return (
    <div className="bg-white py-6">
      {/* Full-width Search Bar */}
      <div className="mb-6">
        <SearchBar placeholder="Search" className="w-full" />
      </div>

      {/* Title */}
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Fixed Finished</h2>

      {/* Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab("sell")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "sell"
              ? "bg-teal-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          Things I sell
        </button>
        <button
          onClick={() => setActiveTab("purchase")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "purchase"
              ? "bg-teal-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          My Purchase
        </button>
      </div>

      {/* Dynamic Content */}
      <div>
        {activeList.length > 0 ? (
          <ul className="space-y-4">
            {activeList.map((item) => (
              <li
                key={item.id}
                className="p-4 border rounded-lg shadow-sm flex justify-between"
              >
                <span className="font-semibold text-gray-800">{item.title}</span>
                <span className="text-sm text-gray-600">{item.status}</span>
              </li>
            ))}
          </ul>
        ) : (
          <div className="text-center text-gray-500">
            None of your ads have received any requests yet
          </div>
        )}
      </div>
    </div>
  );
}