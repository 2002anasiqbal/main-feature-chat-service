"use client";
import React, { useState, useRef, useEffect } from "react";
import { MapContainer, TileLayer, useMap, Marker, Popup } from "react-leaflet";
import L from 'leaflet';
import "leaflet/dist/leaflet.css";
import CategoriesSelector from "./catagory";
import MapControls from "./MapControls";
import boatService from "@/services/boatService";

// Default icon fix for Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// For map marker functionality
const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function Sidebar({ onFilterChange }) {
  // Controls the entire sidebar's open/closed state on mobile
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
  // Features state 
  const [features, setFeatures] = useState([]);
  const [selectedFeatures, setSelectedFeatures] = useState([]);

  // Distance slider state
  const [distance, setDistance] = useState(50);

  // Price range state
  const [price, setPrice] = useState({ from: "", to: "" });

  // Year range state
  const [year, setYear] = useState({ from: "", to: "" });

  // Length range state
  const [length, setLength] = useState({ from: "", to: "" });

  // Boat condition state
  const [condition, setCondition] = useState(null);

  // Other filters
  const [filters, setFilters] = useState({
    condition: null,
    seller_type: null,
    ad_type: null
  });

  // Location from map
  const [mapLocation, setMapLocation] = useState(null);
  
  // Toggle checkboxes
  const [checkboxes, setCheckboxes] = useState({
    fixFinished: false,
    freeShipping: false,
    newToday: false,
    retailer: false,
    private: false,
    forSale: false,
    forRent: false
  });

  // Get available features on component mount
  useEffect(() => {
    const fetchFeatures = async () => {
      try {
        const featuresData = await boatService.getFeatures();
        setFeatures(featuresData);
      } catch (error) {
        console.error("Error fetching features:", error);
      }
    };

    fetchFeatures();
  }, []);

  // Toggle for "Fix Finished" and "Free Shipping"
  const handleCheckboxChange = (checkboxName) => {
    setCheckboxes(prev => {
      const newState = { ...prev, [checkboxName]: !prev[checkboxName] };
      
      // Map checkboxes to actual filter values
      let newFilters = { ...filters };
      
      // Seller type filters
      if (checkboxName === 'retailer' || checkboxName === 'private') {
        // Set seller type based on checkbox
        if (checkboxName === 'retailer' && newState.retailer) {
          newFilters.seller_type = 'dealer';
        } else if (checkboxName === 'private' && newState.private) {
          newFilters.seller_type = 'private';
        } else {
          newFilters.seller_type = null; // Neither is checked
        }
      }
      
      // Ad type filters
      if (checkboxName === 'forSale' || checkboxName === 'forRent') {
        // Set ad type based on checkbox
        if (checkboxName === 'forSale' && newState.forSale) {
          newFilters.ad_type = 'for_sale'; // Use lowercase with underscore
        } else if (checkboxName === 'forRent' && newState.forRent) {
          newFilters.ad_type = 'for_rent'; // Use lowercase with underscore
        } else {
          newFilters.ad_type = null; // Neither is checked
        }
      }
      
      setFilters(newFilters);
      
      return newState;
    });
  };

  // Feature selection handler  
  const handleFeatureChange = (featureId) => {
    setSelectedFeatures(prev => {
      if (prev.includes(featureId)) {
        return prev.filter(id => id !== featureId);
      } else {
        return [...prev, featureId];
      }
    });
  };

  // Condition selection handler
  const handleConditionChange = (condition) => {
    setCondition(prev => prev === condition ? null : condition);
    setFilters(prev => ({
      ...prev,
      condition: prev.condition === condition ? null : condition
    }));
  };

  // Price range handlers
  const handlePriceChange = (type, value) => {
    setPrice(prev => ({ ...prev, [type]: value }));
  };

  // Year range handlers  
  const handleYearChange = (type, value) => {
    setYear(prev => ({ ...prev, [type]: value }));
  };

  // Length range handlers
  const handleLengthChange = (type, value) => {
    setLength(prev => ({ ...prev, [type]: value }));
  };

  // Search button handler
 const handleSearch = () => {
  // Construct the filter object
  const filterObject = {
    price_min: price.from ? parseFloat(price.from) : null,
    price_max: price.to ? parseFloat(price.to) : null,
    year_min: year.from ? parseInt(year.from) : null,
    year_max: year.to ? parseInt(year.to) : null,
    length_min: length.from ? parseFloat(length.from) : null,
    length_max: length.to ? parseFloat(length.to) : null,
    features: selectedFeatures.length > 0 ? selectedFeatures : null,
    condition: condition,
    seller_type: filters.seller_type,
    ad_type: filters.ad_type
  };

  // Add map-based location if selected
  if (mapLocation) {
    console.log("Including geo-filter with location:", mapLocation);
    filterObject.location = mapLocation;
    filterObject.distance = distance;
  }

  // If "new today" is checked, add created_at filter
  if (checkboxes.newToday) {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0]; // Format: YYYY-MM-DD
    filterObject.created_after = todayStr;
  }

  // Debug the final filter object
  console.log("✅ Final filter object to be sent:", JSON.stringify(filterObject, null, 2));
  console.log("✅ Selected condition:", condition);
  console.log("✅ Filters object:", JSON.stringify(filters, null, 2));
  console.log("✅ Selected features:", selectedFeatures);
  console.log("✅ Checkboxes state:", JSON.stringify(checkboxes, null, 2));

  // Pass the constructed filter to parent component
  if (onFilterChange) {
    onFilterChange(filterObject);
  }
};

  // Map click handler (to set location for filtering)
  const MapClickHandler = () => {
  const map = useMap();
  
  useEffect(() => {
    map.on('click', (e) => {
      const newLocation = {
        latitude: e.latlng.lat,
        longitude: e.latlng.lng
      };
      
      console.log("Selected map location:", newLocation);
      setMapLocation(newLocation);
    });
    
    return () => {
      map.off('click');
    };
  }, [map]);
  
  return null;
};

  // --- Mobile Sidebar Handlers ---
  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  // We'll stop clicks from propagating inside the sidebar,
  // so clicks inside don't close it
  const sidebarRef = useRef(null);
  const stopPropagation = (e) => e.stopPropagation();

  useEffect(() => {
    // Trigger initial filter on component mount
    handleSearch();
  }, []); // Empty dependency array means this runs once on mount

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

        {/* 2) Condition Section */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold mb-2">Condition</h3>
          <div className="space-y-2">
            {[
              { value: 'new', label: 'New' },
              { value: 'like_new', label: 'Like New' },
              { value: 'excellent', label: 'Excellent' },
              { value: 'good', label: 'Good' },
              { value: 'fair', label: 'Fair' },
              { value: 'poor', label: 'Poor' },
              { value: 'project_boat', label: 'Project Boat' }
            ].map(conditionOption => (
              <label key={conditionOption.value} className="flex items-center space-x-2 text-gray-800 text-sm">
                <input
                  type="checkbox"
                  checked={condition === conditionOption.value}
                  onChange={() => handleConditionChange(conditionOption.value)}
                  className="w-4 h-4"
                />
                <span>{conditionOption.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* 3) Fix Finished & Other Checkboxes */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold mb-2">Options</h3>
          <div className="space-y-2">
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={checkboxes.fixFinished}
                onChange={() => handleCheckboxChange("fixFinished")}
                className="w-4 h-4"
              />
              <span>Fix finished</span>
            </label>
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={checkboxes.freeShipping}
                onChange={() => handleCheckboxChange("freeShipping")}
                className="w-4 h-4 "
              />
              <span>Free shipping</span>
            </label>
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={checkboxes.newToday}
                onChange={() => handleCheckboxChange("newToday")}
                className="w-4 h-4 "
              />
              <span>New today</span>
            </label>
          </div>
        </div>

        {/* 4) Search Field */}
        <div className="mt-5 px-4">
          <input
            type="text"
            placeholder="Search"
            className="w-full p-2 border rounded text-gray-800"
            onChange={(e) => setFilters(prev => ({ ...prev, search_term: e.target.value }))}
          />
        </div>

        {/* 5) Map Section */}
        <div className="relative w-full h-64 rounded-md overflow-hidden mt-5 px-4">
          <MapContainer
            center={[60.472, 8.4689]} // Example center (Norway)
            zoom={5}
            className="w-full h-full"
            zoomControl={false}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MapControls />
            <MapClickHandler />
            
            {/* Display marker where the user clicked */}
            {mapLocation && (
              <Marker 
                position={[mapLocation.latitude, mapLocation.longitude]}
              >
                <Popup>
                  Selected location for filtering
                </Popup>
              </Marker>
            )}
          </MapContainer>
        </div>

        {/* 6) Distance Slider */}
        <div className="mt-5 px-4">
          <label className="text-gray-700 text-sm">Distance</label>
          <input
            type="range"
            min="1"
            max="200"
            value={distance}
            onChange={(e) => setDistance(parseInt(e.target.value))}
            className="w-full"
          />
          <div className="text-right text-gray-600 text-sm">{distance} km</div>
        </div>

        {/* 7) Features Checkboxes */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Features</h3>
          {features.map((feature) => (
            <label key={feature.id} className="flex items-center space-x-2 text-gray-700 text-sm">
              <input 
                type="checkbox" 
                className="w-4 h-4"
                checked={selectedFeatures.includes(feature.id)}
                onChange={() => handleFeatureChange(feature.id)}
              />
              <span>{feature.name}</span>
            </label>
          ))}
        </div>

        {/* 8) Private/Dealer */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Private/Dealer</h3>
          <label className="flex items-center space-x-2 text-gray-700 text-sm">
            <input 
              type="checkbox" 
              className="w-4 h-4"
              checked={checkboxes.retailer}
              onChange={() => handleCheckboxChange("retailer")}
            />
            <span>Retailer</span>
          </label>
          <label className="flex items-center space-x-2 text-gray-700 text-sm">
            <input 
              type="checkbox" 
              className="w-4 h-4"
              checked={checkboxes.private}
              onChange={() => handleCheckboxChange("private")}
            />
            <span>Private</span>
          </label>
        </div>

        {/* 9) Ad Type */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Ad Type</h3>
          <label className="flex items-center space-x-2 text-gray-700 text-sm">
            <input 
              type="checkbox" 
              className="w-4 h-4"
              checked={checkboxes.forSale}
              onChange={() => handleCheckboxChange("forSale")}
            />
            <span>For Sale</span>
          </label>
          <label className="flex items-center space-x-2 text-gray-700 text-sm">
            <input 
              type="checkbox" 
              className="w-4 h-4"
              checked={checkboxes.forRent}
              onChange={() => handleCheckboxChange("forRent")}
            />
            <span>For Rent</span>
          </label>
        </div>
        
        {/* 10) Price Section */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Price</h3>
          <div className="flex items-center space-x-2 mt-1">
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="From"
                value={price.from}
                onChange={(e) => handlePriceChange("from", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">From</span>
            </div>
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="To"
                value={price.to}
                onChange={(e) => handlePriceChange("to", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">To</span>
            </div>
          </div>
        </div>
        
        {/* 11) Year Range */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Year</h3>
          <div className="flex items-center space-x-2 mt-1">
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="From"
                value={year.from}
                onChange={(e) => handleYearChange("from", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">From</span>
            </div>
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="To"
                value={year.to}
                onChange={(e) => handleYearChange("to", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">To</span>
            </div>
          </div>
        </div>

        {/* 12) Length Range */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">Length (feet)</h3>
          <div className="flex items-center space-x-2 mt-1">
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="From"
                value={length.from}
                onChange={(e) => handleLengthChange("from", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">From</span>
            </div>
            <div className="flex flex-col">
              <input
                type="text"
                placeholder="To"
                value={length.to}
                onChange={(e) => handleLengthChange("to", e.target.value)}
                className="w-20 p-1 text-sm border rounded"
              />
              <span className="text-xs text-gray-500">To</span>
            </div>
          </div>
        </div>

        {/* 13) Search Button */}
        <div className="mt-5 px-4 pb-10">
          <button
            onClick={handleSearch}
            className="w-full py-2 bg-teal-500 text-white font-semibold rounded hover:bg-teal-600 transition"
          >
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  );
}