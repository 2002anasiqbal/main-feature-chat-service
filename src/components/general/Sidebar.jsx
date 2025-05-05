"use client";
import React, { useState, useRef } from "react";
import { MapContainer, TileLayer } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import CategoriesSelector from "./catagory";
import MapControls from "./MapControls";

export default function Sidebar() {
  // Controls the entire sidebar's open/closed state on mobile
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Distance slider state
  const [distance, setDistance] = useState(3);

  // Price range state
  const [price, setPrice] = useState({ from: "", to: "" });

  // Other filters
  const [filters, setFilters] = useState({
    fixFinished: false,
    freeShipping: false,
  });

  // Toggle for "Fix Finished" and "Free Shipping"
  const handleCheckboxChange = (filter) => {
    setFilters((prev) => ({
      ...prev,
      [filter]: !prev[filter],
    }));
  };

  // Price "Search" button (optional logic)
  const handlePriceSearch = () => {
    console.log("Price search:", price);
    // Add real search logic if needed
  };

  // --- Mobile Sidebar Handlers ---
  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  // We'll stop clicks from propagating inside the sidebar,
  // so clicks inside don't close it
  const sidebarRef = useRef(null);
  const stopPropagation = (e) => e.stopPropagation();

  return (
    <div className="overflow-y-auto hide-scrollbar">
      {/* Floating Button (mobile only) */}
      <button
        onClick={handleOpenSidebar}
        className="fixed top-1/2 left-2 -translate-y-1/2 bg-teal-500 text-white px-2 rounded-full shadow-md z-50 sm:hidden"
      >
        ☰
      </button>
      {/* 
        1) Transparent Overlay for closing sidebar when clicked outside.
           It's invisible (no background color), 
           but still intercepts clicks to close the sidebar.
      */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-transparent"
          onClick={handleCloseSidebar}
        />
      )}

      {/* 
        2) Sidebar Container 
           - We use onClick={stopPropagation} inside to prevent closing 
             when user clicks *inside* the sidebar. 
      */}
      <div
        ref={sidebarRef}
        onClick={stopPropagation}
        className={`
          fixed top-0 left-0 h-full w-2/3 
          sm:w-full sm:max-w-xs sm:relative
          bg-white shadow-lg rounded-md
          transform transition-transform duration-300 z-50
          overflow-y-auto
          
          ${isSidebarOpen ? "translate-x-0" : "-translate-x-full"}
          sm:translate-x-0
        `}
      >
        {/* Close Button (mobile only) */}
        <button
          onClick={handleCloseSidebar}
          className="absolute top-4 right-4 text-gray-600 sm:hidden"
        >
          ×
        </button>

        {/* === Actual Sidebar Content Below === */}

        {/* 1) Categories Section */}
        <div>
          <CategoriesSelector />
        </div>

        {/* 2) Fix Finished & Free Shipping Filters */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold mb-2">Fix Finished</h3>
          <div className="space-y-2">
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={filters.fixFinished}
                onChange={() => handleCheckboxChange("fixFinished")}
                className="w-4 h-4"
              />
              <span>Fix finished (70,551)</span>
            </label>
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={filters.freeShipping}
                onChange={() => handleCheckboxChange("freeShipping")}
                className="w-4 h-4 "
              />
              <span>Free shipping (1,702)</span>
            </label>
          </div>
        </div>

        {/* 3) Search Field */}
        <div className="mt-5">
          <input
            type="text"
            placeholder="Search"
            className="w-full p-2  text-gray-800 "
          />
        </div>

        {/* 4) Map Section */}
        <div className="relative w-full h-64 rounded-md overflow-hidden mt-5">
          <MapContainer
            center={[60.472, 8.4689]} // Example center (Norway)
            zoom={5}
            className="w-full h-full"
            zoomControl={false}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MapControls />
          </MapContainer>
        </div>

        {/* 5) Distance Slider */}
        <div className="mt-5">
          <label className="text-gray-700 text-sm">Distance</label>
          <input
            type="range"
            min="1"
            max="50"
            value={distance}
            onChange={(e) => setDistance(e.target.value)}
            className="w-full"
          />
          <div className="text-right text-gray-600 text-sm">{distance} km</div>
        </div>

        {/* 6) Area Checkboxes */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold">Area</h3>
          {[
            "Agder (7,407)", "Akershus (25,286)", "Buskerud (8,491)", "Finnmark (264)",
            "Inland Norway (8,657)", "Møre og Romsdal (3,614)", "Nordland (1,109)",
            "Oslo (23,128)", "Rogaland (13,377)", "Svalbard (1)", "Telemark (4,619)",
            "Troms (1,325)", "Trøndelag (8,335)", "Vestfold (9,908)",
            "Vestland (11,885)", "Østfold (11,898)"
          ].map((area, index) => (
            <label key={index} className="flex items-center space-x-2 text-gray-700 text-sm">
              <input type="checkbox" className="w-4 h-4" />
              <span>{area}</span>
            </label>
          ))}
        </div>

        {/* 7) Type of Advertisement */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold">Type of Advertisement</h3>
          {["For Sale (136,886)", "Giveaway (365)", "Want to buy (2,054)"].map((ad, idx) => (
            <label key={idx} className="flex items-center space-x-2 text-gray-700 text-sm">
              <input type="checkbox" className="w-4 h-4" />
              <span>{ad}</span>
            </label>
          ))}
        </div>

        {/* 8) Price Section */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold">Price</h3>
          <div className="flex items-center space-x-2 mt-1">
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="From"
                value={price.from}
                onChange={(e) => setPrice({ ...price, from: e.target.value })}
                className="w-20 p-1 text-sm"
              />
              <span className="text-xs text-gray-500">From</span>
            </div>
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="To"
                value={price.to}
                onChange={(e) => setPrice({ ...price, to: e.target.value })}
                className="w-20 p-1  text-sm"
              />
              <span className="text-xs text-gray-500">To</span>
            </div>
          </div>
          <button
            onClick={handlePriceSearch}
            className="mt-2 px-4 py-2 hover:bg-gray-100 text-teal-600 text-sm"
          >
            Search
          </button>
        </div>

        {/* 9) Private/Dealer */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold">Private/Dealer</h3>
          {["Retailer (703)", "Private (138,602)"].map((option, idx) => (
            <label key={idx} className="flex items-center space-x-2 text-gray-700 text-sm">
              <input type="checkbox" className="w-4 h-4" />
              <span>{option}</span>
            </label>
          ))}
        </div>

        {/* 10) Published */}
        <div className="mt-5">
          <h3 className="text-gray-700 text-sm font-bold">Published</h3>
          <label className="flex items-center space-x-2 text-gray-700 text-sm">
            <input type="checkbox" className="w-4 h-4" />
            <span>New Today (2,801)</span>
          </label>
        </div>
      </div>
    </div>
  );
}