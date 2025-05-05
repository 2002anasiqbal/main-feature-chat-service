"use client";
import { useState } from "react";
import Page from "../GenerateCard"; // Using your `Page` component

export default function AdvertisementReviews() {
  const [activeTab, setActiveTab] = useState("advertisement"); // Default to "Advertisement"

  return (
    <div className="bg-white p-6 mx-auto">
      {/* Toggle Buttons */}
      <div className="flex gap-4 mb-6">
        <button
          onClick={() => setActiveTab("advertisement")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "advertisement"
              ? "bg-teal-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          Advertisement
        </button>
        <button
          onClick={() => setActiveTab("reviews")}
          className={`px-5 py-2 rounded-md transition ${
            activeTab === "reviews"
              ? "bg-gray-500 text-white"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
        >
          Reviews
        </button>
      </div>

      {/* Advertisement Section */}
      {activeTab === "advertisement" && (
        <div>
          <Page /> {/* Page component will render its own placeholder data */}
        </div>
      )}

      {/* Reviews Section */}
      {activeTab === "reviews" && (
        <div className="text-gray-500 text-center">No reviews available yet</div>
      )}
    </div>
  );
}