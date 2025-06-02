"use client";
import React, { useState, useRef } from "react";

const TravelSidebar = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [expandedSections, setExpandedSections] = useState({
    directOrder: true,
    stopovers: true,
    luggage: true,
    time: true,
    tips: true,
  });

  // Toggle entire sidebar on mobile
  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  // Toggle individual sections
  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  // Prevent clicks *inside* sidebar from closing it
  const stopPropagation = (e) => e.stopPropagation();

  return (
    <>
      {/* 1) Floating button (mobile only) */}
      <button
        onClick={handleOpenSidebar}
        className="fixed top-1/2 left-2 -translate-y-1/2 bg-teal-500 text-white p-2 rounded-full shadow-md z-50 sm:hidden"
      >
        ☰
      </button>

      {/* 
        2) Transparent Overlay 
           - Only visible if isSidebarOpen
           - Covers full screen 
           - Click outside => closes sidebar 
      */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-transparent"
          onClick={handleCloseSidebar}
        />
      )}

      {/* 
        3) Sidebar Container 
           - Clicks inside => e.stopPropagation() so it doesn't close 
           - Slides in on mobile, static on larger screens 
      */}
      <div
        onClick={stopPropagation}
        className={`
          fixed top-0 left-0 h-full w-2/3
          sm:w-full sm:max-w-xs
          bg-white p-4 shadow-lg 
          transform transition-transform duration-300 z-50
          ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
          sm:static sm:translate-x-0
        `}
      >
        {/* Close Button (mobile only) */}
        <button
          onClick={handleCloseSidebar}
          className="absolute top-4 right-4 text-gray-600 sm:hidden"
        >
          ×
        </button>

        {/* Main Sidebar Content */}
        <button className="w-1/2 bg-teal-500 text-white py-2 rounded-md font-semibold">
          Price alerts
        </button>

        {/* Direct Order Section */}
        <div className="mt-4">
          <h3
            className="flex justify-between items-center cursor-pointer font-bold text-gray-600"
            onClick={() => toggleSection("directOrder")}
          >
            Direct order <span>{expandedSections.directOrder ? "▲" : "▼"}</span>
          </h3>
          {expandedSections.directOrder && (
            <div className="mt-2 space-y-2 text-gray-400">
              {["Show all hits", "Book directly with airline"].map((option, index) => (
                <label key={index} className="flex items-center space-x-2 cursor-pointer">
                  <input type="radio" name="directOrder" className="hidden peer" defaultChecked={index === 0} />
                  <div className="w-6 h-6 rounded-full border-2 border-gray-400 flex items-center justify-center peer-checked:border-teal-500">
                    <div className="w-3 h-3 bg-teal-500 rounded-full hidden peer-checked:block" />
                  </div>
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        <hr className="my-3 border-t-2 border-gray-500" />

        {/* Stopovers Section */}
        <div>
          <h3
            className="flex justify-between items-center cursor-pointer font-bold text-gray-600"
            onClick={() => toggleSection("stopovers")}
          >
            Stopovers <span>{expandedSections.stopovers ? "▲" : "▼"}</span>
          </h3>
          {expandedSections.stopovers && (
            <div className="mt-2 space-y-2 text-gray-400">
              {["Direct", "Max 1", "Max 2", "All"].map((option, index) => (
                <label key={index} className="flex items-center space-x-2 cursor-pointer">
                  <input type="radio" name="stopovers" className="hidden peer" defaultChecked={index === 0} />
                  <div className="w-6 h-6 rounded-full border-2 border-gray-400 flex items-center justify-center peer-checked:border-teal-500">
                    <div className="w-3 h-3 bg-teal-500 rounded-full hidden peer-checked:block" />
                  </div>
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        <hr className="my-3 border-t-2 border-gray-500" />

        {/* Luggage Section */}
        <div>
          <h3
            className="flex justify-between items-center cursor-pointer font-bold text-gray-600"
            onClick={() => toggleSection("luggage")}
          >
            Luggage <span>{expandedSections.luggage ? "▲" : "▼"}</span>
          </h3>
          {expandedSections.luggage && (
            <div className="mt-2 space-y-2 text-gray-400">
              {["Direct", "Max 1", "Max 2", "All"].map((option, index) => (
                <label key={index} className="flex items-center space-x-2 cursor-pointer">
                  <input type="radio" name="luggage" className="hidden peer" defaultChecked={index === 0} />
                  <div className="w-6 h-6 rounded-full border-2 border-gray-400 flex items-center justify-center peer-checked:border-teal-500">
                    <div className="w-3 h-3 bg-teal-500 rounded-full hidden peer-checked:block" />
                  </div>
                  <span>{option}</span>
                </label>
              ))}
            </div>
          )}
        </div>

        <hr className="my-3 border-t-2 border-gray-500" />

        {/* Tips Section */}
        <div>
          <h3
            className="flex justify-between items-center cursor-pointer font-bold text-gray-600"
            onClick={() => toggleSection("tips")}
          >
            Tips us <span>{expandedSections.tips ? "▲" : "▼"}</span>
          </h3>
          {expandedSections.tips && (
            <p className="mt-2 text-sm text-gray-400">
              We appreciate your input to improve the service.
            </p>
          )}
        </div>

        <hr className="my-3 border-t-2 border-gray-500" />
      </div>
    </>
  );
};

export default TravelSidebar;