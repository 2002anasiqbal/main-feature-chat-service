// Selgo-frontend/src/components/forms/MotorcycleForm.jsx
"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import motorcycleService from "@/services/motorcycleService";
import useAuthStore from "@/store/store";

const MotorcycleForm = ({ category = "Motorcycles" }) => {
  const router = useRouter();
  const { user } = useAuthStore();
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [formData, setFormData] = useState({
    // Basic info
    registration_number: "",
    chassis_number: "",
    brand: "",
    model: "",
    type_mc: "",
    model_year: "",
    
    // Engine and chassis
    fuel: "",
    power_hp: "",
    displacement_ccm: "",
    weight_kg: "",
    color: "",
    
    // Condition
    condition: "",
    mileage: "",
    number_of_owners: "",
    has_condition_report: "",
    maintenance_schedule_followed: false,
    warranty_type: "",
    
    // Media
    pictures: [],
    video: "",
    description: "",
    
    // Price
    exemption_from_re_registration_fee: "No",
    re_registration_fee_nok: "",
    selling_price_nok: "",
    
    // Contact
    postal_code: "",
    country: "Norge",
    hide_profile: false,
    
    // Backend fields
    title: "",
    price: "",
    seller_type: "private",
    location: "", 
    category_id: 1,
    seller_id: 1
  });

  const [imagePreviews, setImagePreviews] = useState([]);

  // Options for dropdowns
  const fuelTypes = [
    "Gasoline", "Diesel", "Electric", "Hybrid", "Other"
  ];

  const mcTypes = [
    "Adventure", "Cruiser", "Sport", "Touring", "Naked", "Scooter", "Off-road", "Enduro"
  ];

  const conditionReports = [
    "Yes", "No", "Not applicable"
  ];

  const warrantyTypes = [
    "No warranty", "Manufacturer warranty", "Extended warranty", "Dealer warranty"
  ];

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
  };

  // Handle radio button changes
  const handleRadioChange = (name, value) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  // Handle image upload
  const handleImageUpload = (e) => {
    const files = Array.from(e.target.files);
    
    if (files.length + imagePreviews.length > 10) {
      alert("Maximum 10 images allowed");
      return;
    }

    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreviews(prev => [...prev, reader.result]);
      };
      reader.readAsDataURL(file);
    });
  };

 // Handle form submission
const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);

  try {
    // CORRECT category mapping - this must match the database
    const categoryMap = {
      "Thresher 6000": 1,
      "Suzuki 6000": 2, 
      "Motorcycles 6000": 3,
      "Auto bikes 6000": 4,
      "Tractor 6000": 5,
      "Bikes 6000": 6
    };

    // Get the correct category ID
    const categoryId = categoryMap[category];
    
    console.log(`📂 Category: "${category}" -> ID: ${categoryId}`);
    
    if (!categoryId) {
      throw new Error(`Unknown category: ${category}`);
    }

    // Parse location into city and country
    const parseLocation = (location) => {
      if (!location) return { city: "Oslo", country: "Norway" };
      
      const parts = location.split(',').map(part => part.trim());
      if (parts.length >= 2) {
        return {
          city: parts[0],
          country: parts.slice(1).join(', ')
        };
      }
      return { city: parts[0] || "Oslo", country: "Norway" };
    };

    const { city, country } = parseLocation(formData.location);

    // Create full address from location field
    const fullAddress = formData.location || `${city}, ${country}`;

    // Debug what we're sending
    console.log("🔍 DEBUG - Form processing:");
    console.log("  location field:", formData.location);
    console.log("  postal_code field:", formData.postal_code);
    console.log("  parsed city:", city);
    console.log("  parsed country:", country);
    console.log("  full address for backend:", fullAddress);

    // Prepare data for backend
    const motorcycleData = {
      title: formData.brand && formData.model ? `${formData.brand} ${formData.model} ${formData.model_year}` : `${category} for sale`,
      description: formData.description || `${formData.brand} ${formData.model} from ${formData.model_year}`,
      brand: formData.brand || "Unknown",
      model: formData.model || "Unknown", 
      year: parseInt(formData.model_year) || new Date().getFullYear(),
      engine_size: parseInt(formData.displacement_ccm) || null,
      mileage: parseInt(formData.mileage) || null,
      price: parseFloat(formData.selling_price_nok) || 0,
      condition: mapConditionToEnum(formData.condition),
      motorcycle_type: mapTypeToEnum(formData.type_mc),
      seller_type: "private",
      city: city,                    // ← Now uses parsed city
      address: fullAddress,          // ← Now uses full location string
      category_id: categoryId,
      seller_id: user?.id || 1, // Use real user ID
      netbill: false,
      images: imagePreviews.map((preview, index) => ({
        image_url: preview,
        is_primary: index === 0,
        alt_text: `${formData.brand} ${formData.model}`
      }))
    };

    console.log("🚀 Sending motorcycle data to backend:");
    console.log("  city:", motorcycleData.city);
    console.log("  address:", motorcycleData.address);

    const result = await motorcycleService.createMotorcycle(motorcycleData);
    
    alert(`Motorcycle ad posted successfully in ${category}!`);
    
    // Redirect to the specific category page to see the new motorcycle
    router.push(`/routes/motor-cycle/category?category=${encodeURIComponent(category)}`);

  } catch (error) {
    console.error("❌ Error creating motorcycle ad:", error);
    
    let errorMessage = "Failed to post ad. Please try again.";
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage = `Error: ${error.response.data.detail}`;
    }
    alert(errorMessage);
  } finally {
    setLoading(false);
  }
};
// Add these helper functions to map form values to enum values
const mapConditionToEnum = (condition) => {
  const conditionMap = {
    "Used": "good",
    "New": "new",
    "Like New": "like_new",
    "Excellent": "excellent",
    "Good": "good",
    "Fair": "fair",
    "Poor": "poor"
  };
  return conditionMap[condition] || "good";
};

const mapTypeToEnum = (type) => {
  const typeMap = {
    "Adventure": "adventure",
    "Cruiser": "cruiser",
    "Sport": "sports",
    "Touring": "touring",
    "Naked": "nakne",
    "Scooter": "scooter",
    "Off-road": "adventure",
    "Enduro": "adventure"
  };
  return typeMap[type] || "adventure";
};
  // Calculate total searchable price
  const calculateTotalPrice = () => {
    const reRegFee = parseFloat(formData.re_registration_fee_nok) || 0;
    const sellingPrice = parseFloat(formData.selling_price_nok) || 0;
    const exemption = formData.exemption_from_re_registration_fee === "Yes";
    return exemption ? sellingPrice : sellingPrice + reRegFee;
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white">
      <form onSubmit={handleSubmit} className="space-y-8">
        
        {/* Title */}
        <h1 className="text-2xl font-bold text-gray-900 mb-6">{category} for sale</h1>

        {/* Registration Information */}
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Registration number <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="text"
              name="registration_number"
              value={formData.registration_number}
              onChange={handleInputChange}
              className="w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-blue-600 mt-1">Registration number or chassis number must be filled in.</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Chassis/chassis number <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="text"
              name="chassis_number"
              value={formData.chassis_number}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="text-xs text-blue-600 mt-1">
              It is listed on the first page of the vehicle registration document. You can also find it at vegvesen.no.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Brand Fire</label>
            <input
              type="text"
              name="brand"
              value={formData.brand}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Model <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="text"
              name="model"
              value={formData.model}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Type MC</label>
            <select
              name="type_mc"
              value={formData.type_mc}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select type</option>
              {mcTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Model year</label>
            <input
              type="number"
              name="model_year"
              value={formData.model_year}
              onChange={handleInputChange}
              className="w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              min="1900"
              max={new Date().getFullYear() + 1}
            />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex">
              <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-blue-700">
                <strong>Note:</strong> You cannot change the make, model, type or year of manufacture after the ad has been published.
              </p>
            </div>
          </div>
        </div>

        {/* Engine and chassis */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Engine and chassis</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Fuel <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <select
              name="fuel"
              value={formData.fuel}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select fuel type</option>
              {fuelTypes.map(fuel => (
                <option key={fuel} value={fuel}>{fuel}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Power in hp <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="power_hp"
                value={formData.power_hp}
                onChange={handleInputChange}
                className="w-64 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">hp</span>
            </div>
            <p className="text-xs text-blue-600 mt-1">
              Power/horsepower indicates engine power, and you can find this information in the vehicle registration document.
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Displacement in ccm <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="displacement_ccm"
                value={formData.displacement_ccm}
                onChange={handleInputChange}
                className="w-64 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">cc</span>
            </div>
            <p className="text-xs text-blue-600 mt-1">
              Displacement indicates the size of the engine, and you can find this information in the vehicle registration document.
            </p>
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex">
              <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <p className="text-sm text-blue-700">
                A two-wheeler with a displacement of less than 50 cc is classified as a moped, while a two-wheeler of 50 cc or more is classified as a MC. Make sure you select the correct category at the top of the form.
              </p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Weight in kg <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="weight_kg"
                value={formData.weight_kg}
                onChange={handleInputChange}
                className="w-64 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">kg</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Color <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="text"
              name="color"
              value={formData.color}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        {/* Condition and warranty */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Condition and warranty</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Condition <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="space-y-2">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="condition"
                  value="Used"
                  checked={formData.condition === "Used"}
                  onChange={(e) => handleRadioChange("condition", e.target.value)}
                  className="mr-2"
                />
                Used
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="condition"
                  value="New"
                  checked={formData.condition === "New"}
                  onChange={(e) => handleRadioChange("condition", e.target.value)}
                  className="mr-2"
                />
                New
              </label>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Mileage <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="mileage"
                value={formData.mileage}
                onChange={handleInputChange}
                className="w-48 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">km</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Number of owners <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="number"
              name="number_of_owners"
              value={formData.number_of_owners}
              onChange={handleInputChange}
              className="w-48 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Has condition report <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <select
              name="has_condition_report"
              value={formData.has_condition_report}
              onChange={handleInputChange}
              className="w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select option</option>
              {conditionReports.map(option => (
                <option key={option} value={option}>{option}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="maintenance_schedule_followed"
                checked={formData.maintenance_schedule_followed}
                onChange={handleInputChange}
                className="mr-2"
              />
              <span className="text-sm text-blue-600">Followed the motorcycle maintenance schedule</span>
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Warranty type <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <select
              name="warranty_type"
              value={formData.warranty_type}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Select warranty type</option>
              {warrantyTypes.map(warranty => (
                <option key={warranty} value={warranty}>{warranty}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Pictures, video and description */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Pictures, video and description</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">
              Pictures <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="file"
              multiple
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
              id="photo-upload"
            />
            <label
              htmlFor="photo-upload"
              className="inline-block px-4 py-2 border border-blue-500 text-blue-500 rounded-md hover:bg-blue-50 cursor-pointer"
            >
              Add photos
            </label>
            
            {imagePreviews.length > 0 && (
              <div className="grid grid-cols-4 gap-2 mt-4">
                {imagePreviews.map((preview, index) => (
                  <img
                    key={index}
                    src={preview}
                    alt={`Preview ${index + 1}`}
                    className="w-full h-20 object-cover rounded border"
                  />
                ))}
              </div>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Video <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <input
              type="url"
              name="video"
              value={formData.video}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Link to video on YouTube or Vimeo"
            />
            <p className="text-xs text-gray-600 mt-1">Link to video on YouTube or Vimeo</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">
              Description <span className="text-orange-600 text-sm">(optional)</span>
            </label>
            <div className="border border-gray-300 rounded-md">
              <div className="border-b border-gray-300 px-3 py-2 bg-gray-50">
                <button type="button" className="mr-4 font-bold">B</button>
                <button type="button">≡</button>
              </div>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={8}
                className="w-full px-3 py-2 border-0 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                placeholder="Describe your motorcycle..."
              />
            </div>
          </div>
        </div>

        {/* Price */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Price</h2>
          
          <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
            <div className="flex">
              <svg className="w-5 h-5 text-blue-500 mt-0.5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
              </svg>
              <div>
                <p className="text-sm text-blue-700">
                  As a seller, you are responsible for ensuring that the re-registration fee is correct.
                </p>
                <a href="#" className="text-blue-600 underline text-sm">Read more about the re-registration fee</a>
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-2">Exemption from re-registration fee</label>
            <div className="space-x-4">
              <button
                type="button"
                onClick={() => handleRadioChange("exemption_from_re_registration_fee", "Yes")}
                className={`px-4 py-2 border rounded-md ${
                  formData.exemption_from_re_registration_fee === "Yes" 
                    ? "bg-blue-500 text-white border-blue-500" 
                    : "border-gray-300 text-gray-700"
                }`}
              >
                Yes
              </button>
              <button
                type="button"
                onClick={() => handleRadioChange("exemption_from_re_registration_fee", "No")}
                className={`px-4 py-2 border rounded-md ${
                  formData.exemption_from_re_registration_fee === "No" 
                    ? "bg-blue-500 text-white border-blue-500" 
                    : "border-gray-300 text-gray-700"
                }`}
              >
                No
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Re-registration fee in NOK</label>
            <div className="relative">
              <input
                type="number"
                name="re_registration_fee_nok"
                value={formData.re_registration_fee_nok}
                onChange={handleInputChange}
                className="w-64 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">kr</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Selling price in NOK - ex. re-registration</label>
            <div className="relative">
              <input
                type="number"
                name="selling_price_nok"
                value={formData.selling_price_nok}
                onChange={handleInputChange}
                className="w-64 px-3 py-2 pr-8 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
              <span className="absolute right-3 top-2 text-gray-500 text-sm">kr</span>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Total searchable price</label>
            <p className="text-lg font-medium">{calculateTotalPrice()} kr</p>
          </div>
        </div>

           {/* Contact information */}
       {/* Contact information */}
        <div className="space-y-4">
          <h2 className="text-xl font-bold text-gray-900">Contact information</h2>
          
          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Location *</label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g., Islamabad, Pakistan or Oslo, Norway"
              required
            />
            <p className="text-xs text-gray-600 mt-1">Enter city, country (e.g., Islamabad, Pakistan)</p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-900 mb-1">Postal code</label>
            <input
              type="text"
              name="postal_code"
              value={formData.postal_code}
              onChange={handleInputChange}
              className="w-64 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          

          <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center mr-3">
                <span className="text-blue-600 font-bold">K</span>
              </div>
              <div>
                <p className="font-medium text-blue-600">kamjadkhan</p>
                <p className="text-sm text-gray-600">On FINN since 2025</p>
              </div>
            </div>
          </div>

          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                name="hide_profile"
                checked={formData.hide_profile}
                onChange={handleInputChange}
                className="mr-2"
              />
              <span className="text-sm text-gray-700">
                Do not show profile picture and link to profile page until buyer contacts me
              </span>
            </label>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-4">
          <button
            type="button"
            className="w-full px-6 py-3 border border-blue-500 text-blue-500 rounded-md hover:bg-blue-50 transition duration-200"
          >
            👁 See preview
          </button>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
          >
            {loading ? "Posting..." : "Go ahead"}
          </button>
          
          <p className="text-center text-sm text-gray-600">
            By continuing, you also agree to the{" "}
            <a href="#" className="text-blue-600 underline">advertising rules</a> 🔗
          </p>
        </div>
      </form>
    </div>
  );
};

export default MotorcycleForm;