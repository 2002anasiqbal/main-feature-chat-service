"use client";
import React, { useState, useRef, useEffect } from "react";
import { MapContainer, TileLayer, useMap, Marker, Popup } from "react-leaflet";
import L from 'leaflet';
import "leaflet/dist/leaflet.css";
import CategoriesSelector from "./catagory";
import MapControls from "./MapControls";
import boatService from "@/services/boatService";
import motorcycleService from "@/services/motorcycleService";

// Default icon fix for Leaflet
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function Sidebar({ onFilterChange }) {
  // All your existing state variables...
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [features, setFeatures] = useState([]);
  const [selectedFeatures, setSelectedFeatures] = useState([]);
  const [distance, setDistance] = useState(50);
  const [price, setPrice] = useState({ from: "", to: "" });
  const [year, setYear] = useState({ from: "", to: "" });
  const [length, setLength] = useState({ from: "", to: "" });
  const [condition, setCondition] = useState(null);
  const [filters, setFilters] = useState({
    condition: null,
    seller_type: null,
    ad_type: null
  });
  const [mapLocation, setMapLocation] = useState(null);
  const [checkboxes, setCheckboxes] = useState({
    fixFinished: false,
    freeShipping: false,
    newToday: false,
    retailer: false,
    private: false,
    forSale: false,
    forRent: false
  });

  // Service detection and brand types
  const [currentService, setCurrentService] = useState('boat');
  const [brandTypes, setBrandTypes] = useState([]);
  const [selectedBrandTypes, setSelectedBrandTypes] = useState([]);

  // Detect current service based on URL
  useEffect(() => {
    const detectService = () => {
      const path = window.location.pathname;
      if (path.includes('motor-cycle')) {
        setCurrentService('motorcycle');
      } else if (path.includes('boat')) {
        setCurrentService('boat');
      } else if (path.includes('car')) {
        setCurrentService('car');
      } else {
        setCurrentService('boat'); // default
      }
    };
    
    detectService();
    window.addEventListener('popstate', detectService);
    return () => window.removeEventListener('popstate', detectService);
  }, []);

  // Get brand types based on current service
  useEffect(() => {
    const getBrandTypes = () => {
      switch (currentService) {
        case 'motorcycle':
          setBrandTypes([
            { id: 'adventure', label: 'Adventure' },
            { id: 'cruiser', label: 'Cruiser' },
            { id: 'sports', label: 'Sports' },
            { id: 'touring', label: 'Touring' },
            { id: 'naked', label: 'Naked' },
            { id: 'scooter', label: 'Scooter' },
            { id: 'off-road', label: 'Off-road' },
            { id: 'enduro', label: 'Enduro' }
          ]);
          break;
        case 'boat':
          setBrandTypes([
            { id: 'motor_boat', label: 'Motor Boat' },
            { id: 'sail_boat', label: 'Sail Boat' },
            { id: 'fishing_boat', label: 'Fishing Boat' },
            { id: 'yacht', label: 'Yacht' },
            { id: 'jet_ski', label: 'Jet Ski' },
            { id: 'kayak', label: 'Kayak' },
            { id: 'canoe', label: 'Canoe' },
            { id: 'pontoon', label: 'Pontoon' },
            { id: 'inflatable', label: 'Inflatable Boat' },
            { id: 'dinghy', label: 'Dinghy' },
            { id: 'other', label: 'Other' }
          ]);
          break;
        case 'car':
          setBrandTypes([
            { id: 'sedan', label: 'Sedan' },
            { id: 'suv', label: 'SUV' },
            { id: 'hatchback', label: 'Hatchback' },
            { id: 'coupe', label: 'Coupe' },
            { id: 'convertible', label: 'Convertible' }
          ]);
          break;
        default:
          setBrandTypes([]);
      }
    };

    getBrandTypes();
    setSelectedBrandTypes([]); // Reset selected types when service changes
  }, [currentService]);

  // Handle brand type selection - ENSURE STATE UPDATE
const handleBrandTypeChange = (brandTypeId) => {
  console.log(`🚢 Toggling boat type: ${brandTypeId}`);
  
  setSelectedBrandTypes(prev => {
    const newSelection = prev.includes(brandTypeId) 
      ? prev.filter(id => id !== brandTypeId)
      : [...prev, brandTypeId];
    
    console.log(`🚢 Boat type ${brandTypeId} ${newSelection.includes(brandTypeId) ? 'selected' : 'deselected'}`);
    console.log(`🚢 New selection:`, newSelection);
    
    return newSelection;
  });
  };

  // Update features fetch to skip for motorcycles
  useEffect(() => {
    const fetchFeatures = async () => {
      if (currentService === 'motorcycle') {
        setFeatures([]);
        return;
      }
      
      try {
        const featuresData = await boatService.getFeatures();
        setFeatures(featuresData);
      } catch (error) {
        console.error("Error fetching features:", error);
        setFeatures([]);
      }
    };

    fetchFeatures();
  }, [currentService]);

  // Auto-trigger search when boat types change
  // ✅ FIXED: Auto-trigger search when boat types change (with debouncing)
useEffect(() => {
  console.log("🚢 selectedBrandTypes changed:", selectedBrandTypes);
}, [selectedBrandTypes]);

  // Your existing handler functions...
  const handleCheckboxChange = (checkboxName) => {
    setCheckboxes(prev => {
      const newState = { ...prev, [checkboxName]: !prev[checkboxName] };
      
      let newFilters = { ...filters };
      
      if (checkboxName === 'retailer' || checkboxName === 'private') {
        if (checkboxName === 'retailer' && newState.retailer) {
          newFilters.seller_type = 'dealer';
        } else if (checkboxName === 'private' && newState.private) {
          newFilters.seller_type = 'private';
        } else {
          newFilters.seller_type = null;
        }
      }
      
      if (checkboxName === 'forSale' || checkboxName === 'forRent') {
        if (checkboxName === 'forSale' && newState.forSale) {
          newFilters.ad_type = 'for_sale';
        } else if (checkboxName === 'forRent' && newState.forRent) {
          newFilters.ad_type = 'for_rent';
        } else {
          newFilters.ad_type = null;
        }
      }
      
      setFilters(newFilters);
      return newState;
    });
  };

  const handleFeatureChange = (featureId) => {
    setSelectedFeatures(prev => {
      if (prev.includes(featureId)) {
        return prev.filter(id => id !== featureId);
      } else {
        return [...prev, featureId];
      }
    });
  };

  const handleConditionChange = (condition) => {
    setCondition(prev => prev === condition ? null : condition);
    setFilters(prev => ({
      ...prev,
      condition: prev.condition === condition ? null : condition
    }));
  };

  const handlePriceChange = (type, value) => {
    setPrice(prev => ({ ...prev, [type]: value }));
  };

  const handleYearChange = (type, value) => {
    setYear(prev => ({ ...prev, [type]: value }));
  };

  const handleLengthChange = (type, value) => {
    setLength(prev => ({ ...prev, [type]: value }));
  };

  // UPDATED: Search button handler to include boat types
 const handleSearch = () => {
  console.log("🔍 Apply Filters button clicked");
  console.log("🚢 Current selectedBrandTypes:", selectedBrandTypes);
  
  const filterObject = {
    price_min: price.from ? parseFloat(price.from) : null,
    price_max: price.to ? parseFloat(price.to) : null,
    year_min: year.from ? parseInt(year.from) : null,
    year_max: year.to ? parseInt(year.to) : null,
    condition: condition,
    seller_type: filters.seller_type,
    ad_type: filters.ad_type
  };

  // Add service-specific filters
  if (currentService === 'motorcycle') {
    filterObject.mileage_min = length.from ? parseFloat(length.from) : null;
    filterObject.mileage_max = length.to ? parseFloat(length.to) : null;
    
    if (selectedBrandTypes.length > 0) {
      filterObject.motorcycle_types = selectedBrandTypes;
      console.log("🏍️ Selected motorcycle types:", selectedBrandTypes);
    }
  } else if (currentService === 'boat') {
    filterObject.length_min = length.from ? parseFloat(length.from) : null;
    filterObject.length_max = length.to ? parseFloat(length.to) : null;
    filterObject.features = selectedFeatures.length > 0 ? selectedFeatures : null;
    
    // ✅ Include boat types from current state
    if (selectedBrandTypes.length > 0) {
      filterObject.boat_types = selectedBrandTypes;
      console.log("🚢 Adding boat_types to filter:", selectedBrandTypes);
    } else {
      console.log("🚢 No boat types selected");
    }
  }

  // Add map-based location if selected
  if (mapLocation) {
    filterObject.location = mapLocation;
    filterObject.distance = distance;
  }

  // If "new today" is checked
  if (checkboxes.newToday) {
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    filterObject.created_after = todayStr;
  }

  console.log("✅ Final filter object being sent:", JSON.stringify(filterObject, null, 2));

  if (onFilterChange) {
    onFilterChange(filterObject);
  }
};

  // Your existing map handlers...
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

  const handleOpenSidebar = () => setIsSidebarOpen(true);
  const handleCloseSidebar = () => setIsSidebarOpen(false);

  const sidebarRef = useRef(null);
  const stopPropagation = (e) => e.stopPropagation();

useEffect(() => {
  console.log("🔍 Initial search on component mount");
  handleSearch();
}, []);

  // Get service display name
  const getServiceDisplayName = () => {
    switch (currentService) {
      case 'motorcycle': return 'motorcycles';
      case 'boat': return 'boats';
      case 'car': return 'cars';
      default: return 'items';
    }
  };

  return (
    <div className="overflow-y-auto hide-scrollbar">
      {/* Floating Button (mobile only) */}
      <button
        onClick={handleOpenSidebar}
        className="fixed top-1/2 left-2 -translate-y-1/2 bg-teal-500 text-white px-2 rounded-full shadow-md z-50 sm:hidden"
      >
        ☰
      </button>

      {isSidebarOpen && (
        <div
          className="fixed inset-0 z-40 bg-transparent"
          onClick={handleCloseSidebar}
        />
      )}

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
        <button
          onClick={handleCloseSidebar}
          className="absolute top-4 right-4 text-gray-600 sm:hidden"
        >
          ×
        </button>

        {/* Categories Section */}
        <div>
          <CategoriesSelector />
        </div>

        {/* FIXED: Brand Type Section - Dynamic based on service with proper checkboxes */}
        {brandTypes.length > 0 && (
          <div className="mt-5 px-4">
            <h3 className="text-gray-700 text-sm font-bold mb-2">
              {currentService === 'motorcycle' ? 'Type MC' : 
               currentService === 'boat' ? 'Boat Type' : 
               currentService === 'car' ? 'Car Type' : 'Type'}
            </h3>
            <div className="space-y-2">
              {brandTypes.map((brandType) => (
                <label key={brandType.id} className="flex items-center space-x-2 text-gray-700 text-sm cursor-pointer">
                  <input 
                    type="checkbox" 
                    className="w-4 h-4"
                    checked={selectedBrandTypes.includes(brandType.id)}
                    onChange={() => handleBrandTypeChange(brandType.id)}
                  />
                  <span>{brandType.label}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Condition Section */}
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
              { value: 'project_boat', label: currentService === 'motorcycle' ? 'Project Bike' : currentService === 'car' ? 'Project Car' : 'Project Boat' }
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

        {/* Options Section */}
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
                className="w-4 h-4"
              />
              <span>Free shipping</span>
            </label>
            <label className="flex items-center space-x-2 text-gray-800 text-sm">
              <input
                type="checkbox"
                checked={checkboxes.newToday}
                onChange={() => handleCheckboxChange("newToday")}
                className="w-4 h-4"
              />
              <span>New today</span>
            </label>
          </div>
        </div>

        {/* Search Field */}
        <div className="mt-5 px-4">
          <input
            type="text"
            placeholder={`Search ${getServiceDisplayName()}`}
            className="w-full p-2 border rounded text-gray-800"
            onChange={(e) => setFilters(prev => ({ ...prev, search_term: e.target.value }))}
          />
        </div>

        {/* Map Section */}
        <div className="relative w-full h-64 rounded-md overflow-hidden mt-5 px-4">
          <MapContainer
            center={[60.472, 8.4689]}
            zoom={5}
            className="w-full h-full"
            zoomControl={false}
          >
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <MapControls />
            <MapClickHandler />
            
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

        {/* Distance Slider */}
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

        {/* Features Checkboxes - Only for boats */}
        {currentService === 'boat' && features.length > 0 && (
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
        )}

        {/* Private/Dealer */}
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

        {/* Ad Type */}
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
        
        {/* Price Section */}
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
        
        {/* Year Range */}
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

        {/* Length/Mileage Range - Dynamic label */}
        <div className="mt-5 px-4">
          <h3 className="text-gray-700 text-sm font-bold">
            {currentService === 'motorcycle' ? "Mileage (km)" : 
             currentService === 'car' ? "Mileage (km)" : "Length (feet)"}
          </h3>
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

        {/* Apply Filters Button */}
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