"use client";
import React, { useState } from "react";

export default function RegionTabs() {
  // Tab configuration: each tab has a label and an array of locations.
  const tabs = [
    {
      label: "Northern-Norway",
      locations: [
        "Alstahaug",
        "Alta",
        "Balsfjord",
        "Bardu",
        "Bodø",
        "Fauske",
        "Hammerfest",
        "Harstad",
        "Mo i Rana",
        "Narvik",
        "Sortland",
        "Sørreisa",
        "Tromsø",
        "Vadsø"
      ]
    },
    {
      label: "South",
      locations: [
        "Kristiansand",
        "Arendal",
        "Tønsberg",
        "Sandefjord",
        "Larvik",
        "Halden"
      ]
    },
    {
      label: "Trøndelag",
      locations: [
        "Trondheim",
        "Steinkjer",
        "Levanger",
        "Stjørdal"
      ]
    },
    {
      label: "Westland",
      locations: [
        "Bergen",
        "Stavanger",
        "Haugesund",
        "Egersund"
      ]
    },
    {
      label: "Eastern-Norway",
      locations: [
        "Oslo",
        "Drammen",
        "Fredrikstad",
        "Hamar",
        "Lillehammer",
        "Gjøvik"
      ]
    }
  ];

  // State for the current active tab
  const [activeTab, setActiveTab] = useState(tabs[0].label);

  // Find the locations array for the active tab
  const currentTab = tabs.find((tab) => tab.label === activeTab);

  return (
    <div className="w-full py-8">
      {/* Heading */}
      <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-6">
        Find businesses near you
      </h2>

      {/* Tabs */}
      <div className="flex space-x-6 border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.label}
            onClick={() => setActiveTab(tab.label)}
            className={`relative pb-2 text-sm font-medium ${
              activeTab === tab.label
                ? "text-gray-900 border-b-2 border-teal-600"
                : "text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Active Tab Content: Locations in a responsive grid */}
      <div className="mt-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-x-4 gap-y-2">
        {currentTab.locations.map((loc) => (
          <a
            key={loc}
            href="#"
            className="text-gray-700 hover:underline whitespace-nowrap"
          >
            Plumber in {loc}
          </a>
        ))}
      </div>
    </div>
  );
}
