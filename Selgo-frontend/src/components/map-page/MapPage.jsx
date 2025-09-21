"use client";
import React, { useState, useEffect, useRef } from "react";
import { Loader } from "@googlemaps/js-api-loader";
import SearchBar from "../root/SearchBar";

export default function MapPage() {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  
  // Initialize Google Maps
  useEffect(() => {
    // You'll need to replace this with your actual Google Maps API key
    const loader = new Loader({
      apiKey: "YOUR_GOOGLE_MAPS_API_KEY",
      version: "weekly",
      libraries: ["places"]
    });

    loader.load().then(() => {
      const mapInstance = new google.maps.Map(mapRef.current, {
        center: { lat: 39.8283, lng: -98.5795 }, // Center of USA
        zoom: 4,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
        zoomControl: true,
      });
      
      setMap(mapInstance);
    });
  }, []);

  // Function to handle search
  const handleSearch = (results) => {
    console.log("Search results:", results);
    // Implement search functionality with the map
    // e.g., center the map on search results, add markers, etc.
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="h-screen w-full flex overflow-hidden relative">
      {/* Sidebar */}
      <div className={`bg-white shadow-lg transition-all duration-300 flex flex-col ${sidebarOpen ? 'w-64' : 'w-0'}`}>
        {sidebarOpen && (
          <>
            {/* Logo */}
            <div className="p-4 border-b">
              <div className="h-10 w-full bg-teal-600 rounded-md flex items-center justify-center text-white font-bold">
                LOGO
              </div>
            </div>
            
            {/* Navigation Squares */}
            <div className="flex-1 overflow-y-auto p-2">
              <div className="grid grid-cols-2 gap-2">
                <SquareItem icon="map" label="Map" active />
                <SquareItem icon="jobs" label="Jobs" />
                <SquareItem icon="car" label="Car and Industry" />
                <SquareItem icon="property" label="Property" />
                <SquareItem icon="square" label="The Square" />
                <SquareItem icon="mc" label="MC" />
              </div>
            </div>
          </>
        )}
      </div>

      {/* Map Container */}
      <div className="flex-1 flex flex-col relative">
        {/* Top Search Bar */}
        <div className="absolute top-4 left-4 right-4 z-10 flex items-center gap-4">
          <button 
            onClick={toggleSidebar}
            className="bg-white p-2 rounded-md shadow-md text-teal-600 hover:bg-teal-50"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          
          <div className="flex-1">
            <SearchBar 
              icon={() => (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              )}
              placeholder="Search in Canada..." 
              onSearch={handleSearch} 
            />
          </div>
        </div>
        
        {/* Google Map */}
        <div ref={mapRef} className="w-full h-full" />
        
        {/* Map Controls */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-2">
          <button className="bg-white p-2 rounded-full shadow-md text-teal-600 hover:bg-teal-50">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
          </button>
          <button className="bg-white p-2 rounded-full shadow-md text-teal-600 hover:bg-teal-50">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

// SquareItem Component for sidebar
const SquareItem = ({ icon, label, active }) => {
  return (
    <div className={`rounded-md p-2 flex flex-col items-center justify-center cursor-pointer transition-colors
      ${active ? 'bg-teal-100 text-teal-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}>
      <div className="h-8 w-8 flex items-center justify-center mb-1">
        {/* Replace with actual icons */}
        <div className="h-6 w-6 bg-current opacity-50 rounded-md"></div>
      </div>
      <span className="text-xs font-medium text-center">{label}</span>
    </div>
  );
};