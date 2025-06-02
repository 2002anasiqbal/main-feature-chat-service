"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import boatService from "@/services/boatService";

export default function BoatAdForm({ subcategory }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState([]);
  const [features, setFeatures] = useState([]);
  const [previewVisible, setPreviewVisible] = useState(false);
  const [locationName, setLocationName] = useState("");
  const [country, setCountry] = useState("Norge");

  const [formData, setFormData] = useState({
    title: "",
    category_id: "",
    price: "",
    year: "",
    make: "", // brand
    model: "",
    registration_number: "",
    engine_included: false,
    engine_make: "",
    engine_model: "",
    engine_type: "",
    engine_power: "",
    fuel_type: "",
    top_speed: "",
    length: "",
    beam: "", // width in cm
    draft: "", // depth in cm
    weight: "",
    hull_material: "",
    color: "",
    seats: "",
    sleeping_places: "",
    light_number: "",
    equipment: "",
    location_name: "",
    location_abroad: false,
    description: "",
    images: [],
    video_url: "",
    selected_features: [],
    ad_type: subcategory === "boats-for-rent" ? "for_rent" : "for_sale"
  });

  // Fetch categories and features when component mounts
useEffect(() => {
  const fetchData = async () => {
    try {
      const categoriesData = await boatService.getCategories();
      const featuresData = await boatService.getFeatures();
      
      setCategories(categoriesData);
      setFeatures(featuresData);
      
      // Define explicit mapping from URL slug to category ID
      const subcategoryToCategoryIdMap = {
        "buy-boats": 1,
        "buy-boats-abroad": 2,
        "boats-in-norway": 3,
        "vans-abroad": 4,
        "boats-parts": 5,
        "boats": 6,
        "boats-for-rent": 7,
        "boats-for-sale": 8
      };
      
      // Log available subcategory
      console.log(`Creating ad for subcategory: ${subcategory}`);
      
      // Set category_id based on subcategory from URL
      if (subcategory && subcategoryToCategoryIdMap[subcategory]) {
        const categoryId = subcategoryToCategoryIdMap[subcategory];
        console.log(`Setting category_id to ${categoryId}`);
        
        setFormData(prev => ({
          ...prev,
          category_id: categoryId,
          // Set ad_type based on subcategory
          ad_type: subcategory === "boats-for-rent" ? "for_rent" : "for_sale"
        }));
      } else {
        console.warn(`No mapping found for subcategory: ${subcategory}`);
      }
    } catch (error) {
      console.error("Error fetching form data:", error);
    }
  };
  
  fetchData();
}, [subcategory]);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === "checkbox") {
      setFormData({ ...formData, [name]: checked });
    } else if (name === "selected_features") {
      const featureId = parseInt(value);
      const updatedFeatures = checked 
        ? [...formData.selected_features, featureId]
        : formData.selected_features.filter(id => id !== featureId);
      
      setFormData({ ...formData, selected_features: updatedFeatures });
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setFormData({ ...formData, images: [...formData.images, ...files] });
  };

const handleLocationChange = (e) => {
  const { value } = e.target;
  setFormData({ 
    ...formData, 
    location_abroad: value === "abroad",
    // Don't reset location_name when changing country selection
  });
   // Set default country based on selection
  if (value === "abroad") {
    setCountry("");
  } else {
    setCountry("Norge");
  }
};
  
const handleLocationNameChange = (e) => {
  const value = e.target.value;
  setFormData({
    ...formData,
    location_name: value
  });
  setLocationName(value);
  
  // If location is abroad and has comma, assume the format is "City, Country"
  if (formData.location_abroad && value.includes(',')) {
    const parts = value.split(',');
    if (parts.length > 1) {
      setCountry(parts[parts.length - 1].trim());
    }
  }
};

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  
  try {
    // Format data for API
    const adData = {
      title: formData.title,
      description: formData.description,
      price: parseFloat(formData.price) || 0,
      category_id: parseInt(formData.category_id),
      condition: "good", // Default to good condition
      year: parseInt(formData.year) || null,
      make: formData.make,
      model: formData.model,
      length: parseFloat(formData.length) || null,
      beam: parseFloat(formData.beam) || null,
      draft: parseFloat(formData.draft) || null,
      fuel_type: formData.fuel_type,
      hull_material: formData.hull_material,
      engine_make: formData.engine_make,
      engine_model: formData.engine_model,
      engine_hours: 0, // Default to 0
      engine_power: parseInt(formData.engine_power) || null,
      location_name: formData.location_name,
      ad_type: formData.ad_type,
      features: [], // Empty features array since we removed that section
      status: "active"
    };
    
    // Handle image uploads first
    let imageUrls = [];
    if (formData.images.length > 0) {
      for (const imageFile of formData.images) {
        const formData = new FormData();
        formData.append("file", imageFile);
        
        const uploadResponse = await boatService.uploadImage(formData);
        imageUrls.push({
          image_url: uploadResponse.url,
          is_primary: imageUrls.length === 0 // First image is primary
        });
      }
    }
    
    // Add images to ad data
    adData.images = imageUrls;
    
    // Create the boat ad
    console.log("Sending ad data to API:", adData);
    const response = await boatService.createBoat(adData);
    console.log("Boat ad created successfully:", response);
    // Mark the boat as newly created for frontend prioritization
    if (response.id) {
      boatService.markNewlyCreated(response.id);
    }
    alert("Boat ad created successfully! Redirecting to home page...");
    
    // Force a hard refresh when redirecting to home page
    window.location.href = "/";
  } catch (error) {
    console.error("Error creating boat ad:", error);
    alert("Failed to create ad. Please try again.");
  } finally {
    setLoading(false);
  }
};

  const handlePreview = () => {
    setPreviewVisible(true);
    // In a real implementation, you might want to scroll to a preview section
    // or open a modal with the preview
  };

  // Find the ad type label based on subcategory
  const adTypeLabel = subcategory
    .split("-")
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");

  return (
    <div className="w-full bg-white pb-12">
      <h1 className="text-3xl font-bold mb-6">{adTypeLabel}</h1>
      
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Ad Headline */}
        <div className="space-y-2">
          <label className="block text-gray-700 font-medium">Ad headline</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md"
            required
          />
        </div>
        
        {/* Type of Boat */}
    <div className="space-y-2">
        <label className="block text-gray-700 font-medium">Type of boat</label>
        <select
            name="boat_type"
            value={formData.boat_type || ""}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md appearance-none"
        >
            <option value="">Select boat type</option>
            <option value="motor_boat">Motor Boat</option>
            <option value="sail_boat">Sail Boat</option>
            <option value="fishing_boat">Fishing Boat</option>
            <option value="yacht">Yacht</option>
            <option value="jet_ski">Jet Ski</option>
            <option value="kayak">Kayak</option>
            <option value="canoe">Canoe</option>
            <option value="pontoon">Pontoon</option>
            <option value="inflatable">Inflatable Boat</option>
            <option value="dinghy">Dinghy</option>
            <option value="other">Other</option>
        </select>
    </div>
        <input
  type="hidden"
  name="category_id"
  value={formData.category_id}
/>
        {/* Registration Number */}
        <div className="space-y-2">
          <label className="block text-gray-700 font-medium">
            Registration number <span className="text-gray-500">(optional)</span>
          </label>
          <input
            type="text"
            name="registration_number"
            value={formData.registration_number}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md"
          />
          <p className="text-sm text-gray-600">
            The boat's characteristics in the Small Boat Register or the Ship Register
          </p>
        </div>
        
        {/* Model Year */}
        <div className="space-y-2">
          <label className="block text-gray-700 font-medium">Model year</label>
          <input
            type="number"
            name="year"
            value={formData.year}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md"
            required
          />
        </div>
        
        {/* Brand */}
        <div className="space-y-2">
          <label className="block text-gray-700 font-medium">Brand</label>
          <input
            type="text"
            name="make"
            value={formData.make}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md"
            required
          />
        </div>
        
        {/* Model */}
        <div className="space-y-2">
          <label className="block text-gray-700 font-medium">
            Model <span className="text-gray-500">(optional)</span>
          </label>
          <input
            type="text"
            name="model"
            value={formData.model}
            onChange={handleInputChange}
            className="w-full p-2 border border-gray-300 rounded-md"
          />
        </div>
        
        {/* Location */}
        <div className="space-y-4">
          <label className="block text-gray-700 font-medium">The boat is located in</label>
          <div className="flex items-center space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="location"
                value="norway"
                checked={!formData.location_abroad}
                onChange={handleLocationChange}
                className="mr-2"
              />
              Norway
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="location"
                value="abroad"
                checked={formData.location_abroad}
                onChange={handleLocationChange}
                className="mr-2"
              />
              Abroad
            </label>
          </div>
          
          <div className="space-y-2 mt-4">
            <label className="block text-gray-700 font-medium">Location name</label>
                <input
                  type="text"
                  name="location_name"
                  value={formData.location_name}
                  onChange={handleLocationNameChange}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  placeholder={formData.location_abroad ? "City, Country" : "City, Region"}
                  required
                />
          </div>
        </div>
        
        {/* Engine and Drivetrain */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Engine and drivetrain</h2>
          
          <div className="flex items-center">
            <input
              type="checkbox"
              name="engine_included"
              checked={formData.engine_included}
              onChange={handleInputChange}
              className="mr-2"
            />
            <label>Engine included in the sale</label>
          </div>
          
          {formData.engine_included && (
            <>
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">
                  Engine brand <span className="text-gray-500">(optional)</span>
                </label>
                <input
                  type="text"
                  name="engine_make"
                  value={formData.engine_make}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md"
                />
              </div>
              
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">
                  Engine type <span className="text-gray-500">(optional)</span>
                </label>
                <select
                  name="engine_type"
                  value={formData.engine_type}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="">Select engine type</option>
                  <option value="outboard">Outboard</option>
                  <option value="inboard">Inboard</option>
                  <option value="electric">Electric</option>
                  <option value="other">Other</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">
                  Number of horsepower <span className="text-gray-500">(optional)</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    name="engine_power"
                    value={formData.engine_power}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md pr-12"
                  />
                  <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">hp</span>
                </div>
              </div>
              
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">
                  Fuel <span className="text-gray-500">(optional)</span>
                </label>
                <select
                  name="fuel_type"
                  value={formData.fuel_type}
                  onChange={handleInputChange}
                  className="w-full p-2 border border-gray-300 rounded-md appearance-none"
                >
                  <option value="">Select fuel type</option>
                  <option value="gasoline">Gasoline</option>
                  <option value="diesel">Diesel</option>
                  <option value="electric">Electric</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="other">Other</option>
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="block text-gray-700 font-medium">
                  Top speed in knots <span className="text-gray-500">(optional)</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    name="top_speed"
                    value={formData.top_speed}
                    onChange={handleInputChange}
                    className="w-full p-2 border border-gray-300 rounded-md pr-16"
                  />
                  <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">knot</span>
                </div>
              </div>
            </>
          )}
        </div>
        
        {/* Basic Information */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Basic information</h2>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">Length in feet</label>
            <div className="relative">
              <input
                type="number"
                name="length"
                value={formData.length}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded-md pr-16"
                required
              />
              <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">foot</span>
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Width in cm <span className="text-gray-500">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="beam"
                value={formData.beam}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded-md pr-12"
              />
              <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">cm</span>
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Depth in cm <span className="text-gray-500">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="draft"
                value={formData.draft}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded-md pr-12"
              />
              <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">cm</span>
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Net weight in kg <span className="text-gray-500">(optional)</span>
            </label>
            <div className="relative">
              <input
                type="number"
                name="weight"
                value={formData.weight}
                onChange={handleInputChange}
                className="w-full p-2 border border-gray-300 rounded-md pr-12"
              />
              <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">kg</span>
            </div>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Boat construction material <span className="text-gray-500">(optional)</span>
            </label>
            <select
              name="hull_material"
              value={formData.hull_material}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md appearance-none"
            >
              <option value="">Select material</option>
              <option value="fiberglass">Fiberglass</option>
              <option value="aluminum">Aluminum</option>
              <option value="wood">Wood</option>
              <option value="steel">Steel</option>
              <option value="carbon_fiber">Carbon Fiber</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Color <span className="text-gray-500">(optional)</span>
            </label>
            <input
              type="text"
              name="color"
              value={formData.color}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Number of seats <span className="text-gray-500">(optional)</span>
            </label>
            <input
              type="number"
              name="seats"
              value={formData.seats}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Number of sleeping places <span className="text-gray-500">(optional)</span>
            </label>
            <input
              type="number"
              name="sleeping_places"
              value={formData.sleeping_places}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              LIGHT number (sailboats only) <span className="text-gray-500">(optional)</span>
            </label>
            <input
              type="text"
              name="light_number"
              value={formData.light_number}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md"
            />
            <p className="text-sm text-gray-600">
              The number describes how fast the sailboat is, for example 1.15. The measurement certificate is issued by Norlys.
            </p>
          </div>
        </div>
        
        {/* Equipment */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Equipment</h2>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Equipment <span className="text-gray-500">(optional)</span>
            </label>
            <div className="border border-gray-300 rounded-md overflow-hidden">
              <div className="flex bg-gray-100 p-2 border-b">
                <button type="button" className="px-2 font-bold">B</button>
                <button type="button" className="px-2">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="8" y1="6" x2="21" y2="6"></line>
                    <line x1="8" y1="12" x2="21" y2="12"></line>
                    <line x1="8" y1="18" x2="21" y2="18"></line>
                    <line x1="3" y1="6" x2="3.01" y2="6"></line>
                    <line x1="3" y1="12" x2="3.01" y2="12"></line>
                    <line x1="3" y1="18" x2="3.01" y2="18"></line>
                  </svg>
                </button>
              </div>
              <textarea
                name="equipment"
                value={formData.equipment}
                onChange={handleInputChange}
                className="w-full p-2 min-h-[150px] border-0 focus:ring-0 resize-y"
              ></textarea>
            </div>
          </div>
          
       
        </div>
        
        {/* Pictures, Video, and Description */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-gray-900">Pictures, video and description</h2>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Pictures <span className="text-gray-500">(optional)</span>
            </label>
            <button
              type="button"
              onClick={() => document.getElementById('image-upload').click()}
              className="px-4 py-2 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition"
            >
              Add photos
            </button>
            <input
              id="image-upload"
              type="file"
              multiple
              accept="image/*"
              onChange={handleFileChange}
              className="hidden"
            />
            
            {formData.images.length > 0 && (
              <div className="mt-4 grid grid-cols-3 gap-4">
                {formData.images.map((file, index) => (
                  <div key={index} className="relative">
                    <img
                      src={URL.createObjectURL(file)}
                      alt={`Preview ${index}`}
                      className="w-full h-24 object-cover rounded-md"
                    />
                    <button
                      type="button"
                      onClick={() => setFormData({
                        ...formData,
                        images: formData.images.filter((_, i) => i !== index)
                      })}
                      className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Video <span className="text-gray-500">(optional)</span>
            </label>
            <input
              type="text"
              name="video_url"
              value={formData.video_url}
              onChange={handleInputChange}
              className="w-full p-2 border border-gray-300 rounded-md"
              placeholder="Link to video on YouTube or Vimeo"
            />
            <p className="text-sm text-gray-600">Link to video on YouTube or Vimeo.</p>
          </div>
          
          <div className="space-y-2">
            <label className="block text-gray-700 font-medium">
              Description <span className="text-gray-500">(optional)</span>
            </label>
            <div className="border border-gray-300 rounded-md overflow-hidden">
             <div className="flex bg-gray-100 p-2 border-b">
               <button type="button" className="px-2 font-bold">B</button>
               <button type="button" className="px-2">
                 <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                   <line x1="8" y1="6" x2="21" y2="6"></line>
                   <line x1="8" y1="12" x2="21" y2="12"></line>
                   <line x1="8" y1="18" x2="21" y2="18"></line>
                   <line x1="3" y1="6" x2="3.01" y2="6"></line>
                   <line x1="3" y1="12" x2="3.01" y2="12"></line>
                   <line x1="3" y1="18" x2="3.01" y2="18"></line>
                 </svg>
               </button>
             </div>
             <textarea
               name="description"
               value={formData.description}
               onChange={handleInputChange}
               className="w-full p-2 min-h-[150px] border-0 focus:ring-0 resize-y"
             ></textarea>
           </div>
         </div>
       </div>
       
       {/* Price */}
       <div className="space-y-4">
         <h2 className="text-2xl font-bold text-gray-900">Price</h2>
         
         <div className="space-y-2">
           <label className="block text-gray-700 font-medium">Selling price in NOK</label>
           <div className="relative">
             <input
               type="number"
               name="price"
               value={formData.price}
               onChange={handleInputChange}
               className="w-full p-2 border border-gray-300 rounded-md pr-12"
               required
             />
             <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">kr</span>
           </div>
         </div>
       </div>
       
       {/* Contact Information */}
       <div className="space-y-4">
         <h2 className="text-2xl font-bold text-gray-900">Contact information</h2>
         
         <div className="border border-gray-300 rounded-md p-4 flex items-center space-x-4">
           <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
             <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
               <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
               <circle cx="12" cy="7" r="4"></circle>
             </svg>
           </div>
           <div>
             <div className="text-blue-600">{localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')).username : 'User'}</div>
             <div className="text-gray-600">On SELGO since 2025</div>
           </div>
         </div>
         
         <div className="flex items-center">
           <input
             type="checkbox"
             name="hide_profile"
             className="mr-2"
           />
           <label>Do not show profile picture and link to profile page until buyer contacts me</label>
         </div>
         
         <div className="space-y-2">
           <label className="block text-gray-700 font-medium">Postal code</label>
           <input
             type="text"
             name="postal_code"
             className="w-full p-2 border border-gray-300 rounded-md"
             placeholder="Enter postal code"
           />
         </div>
         
       <div className="space-y-2">
          <label className="block text-gray-700 font-medium">Country</label>
          <div className="relative">
            <input
              type="text"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              readOnly={!formData.location_abroad}
              className={`w-full p-2 border border-gray-300 rounded-md ${formData.location_abroad ? "" : "bg-gray-100"}`}
            />
            {!formData.location_abroad && (
              <button 
                type="button"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
                onClick={() => setCountry("Norge")}
              >
                ✕
              </button>
            )}
          </div>
        </div>
       </div>
       
       {/* Preview and Submit Buttons */}
       <div className="space-y-4">
         <button
           type="button"
           onClick={handlePreview}
           className="w-full py-3 text-blue-600 border border-gray-300 rounded-md flex items-center justify-center hover:bg-gray-50 transition"
         >
           <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="mr-2">
             <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
             <circle cx="12" cy="12" r="3"></circle>
           </svg>
           See preview
         </button>
         
         <button
           type="submit"
           disabled={loading}
           className="w-full py-3 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition flex items-center justify-center"
         >
           {loading ? "Creating..." : "Go ahead"}
         </button>
         
         <p className="text-center text-sm">
           By continuing, you also agree to the 
           <a href="#" className="text-blue-600 ml-1">advertising rules</a>
         </p>
       </div>
     </form>
   </div>
 );
}