"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

const categories = [
  { 
    title: "The Square", 
    description: "Find local shops, deals, and services in your area.",
    subcategories: ["Local shops", "Deals", "Services"]
  },
  { 
    title: "Car and Caravan", 
    description: "Buy, sell, or rent cars, caravans, and trailers.",
    subcategories: ["Cars", "Caravans", "Trailers"]
  },
  { 
    title: "Property", 
    description: "Explore houses, apartments, and land for sale or rent.",
    subcategories: ["Houses", "Apartments", "Land"]
  },
  { 
    title: "Boat", 
    description: "Browse boats, yachts, and marine equipment for sale.",
    subcategories: [
      "Buy Boats", 
      "Buy Boats Abroad", 
      "Boats in Norway", 
      "Vans Abroad", 
      "Boats Parts", 
      "Boats", 
      "Boats for Rent", 
      "Boats for Sale"
    ]
  },
  { 
    title: "Holiday homes and cabins", 
    description: "Discover vacation rentals and holiday homes.",
    subcategories: ["Vacation rentals", "Holiday homes"]
  },
  { 
    title: "Motorcycle", 
    description: "Buy or sell motorcycles, parts, and accessories.",
    subcategories: ["Motorcycles", "Parts", "Accessories"]
  },
  { 
    title: "My Tender", 
    description: "Post and find tendering opportunities and contracts.",
    subcategories: ["Tendering opportunities", "Contracts"]
  },
  { 
    title: "Job", 
    description: "Find jobs or post job listings in different industries.",
    subcategories: ["Job listings", "Industries"]
  },
  { 
    title: "Nutrition", 
    description: "Health supplements, organic food, and meal plans.",
    subcategories: ["Health supplements", "Organic food", "Meal plans"]
  },
];

export default function CreateAd() {
  const [openIndex, setOpenIndex] = useState(null);
  const [openSubcategory, setOpenSubcategory] = useState(null);
  const router = useRouter();

  const handleToggle = (index) => {
    setOpenIndex(openIndex === index ? null : index);
    setOpenSubcategory(null); // Reset subcategory when toggling categories
  };

  const handleSubcategoryClick = (categoryIndex, subcategoryIndex) => {
    const category = categories[categoryIndex].title;
    const subcategory = categories[categoryIndex].subcategories[subcategoryIndex];
    
    // For now, we're only handling Boat category
    if (category === "Boat") {
      // Create a slugified version of the subcategory for routing
      const subcategorySlug = subcategory.toLowerCase().replace(/ /g, "-");
      router.push(`/routes/create-ad/boat/${subcategorySlug}`);
    } else {
      alert(`Creating ads for ${category} - ${subcategory} will be implemented soon!`);
    }
  };

  return (
    <div className="w-full min-h-screen bg-white flex justify-center">
      <div className="w-full max-w-4xl bg-white py-8 px-4">
        <h1 className="text-2xl font-bold mb-6 text-gray-900">Create a New Ad</h1>

        <div className="space-y-2">
          {categories.map((category, index) => (
            <div key={index} className="border border-gray-300 rounded-md overflow-hidden">
              <button
                onClick={() => handleToggle(index)}
                className="w-full flex justify-between items-center p-4 text-left text-gray-800 font-medium bg-white hover:bg-gray-100 transition-all duration-200"
              >
                <span>{category.title}</span>
                <span className="text-gray-500">{openIndex === index ? "▲" : "▼"}</span>
              </button>

              {openIndex === index && (
                <div className="p-4 bg-gray-50 space-y-3">
                  <p className="text-gray-600 mb-3">{category.description}</p>
                  
                  <div className="space-y-1">
                    {category.subcategories.map((subcategory, subIndex) => (
                      <button
                        key={subIndex}
                        onClick={() => handleSubcategoryClick(index, subIndex)}
                        className="w-full text-left p-2 text-blue-600 hover:bg-gray-100 rounded-md transition-colors duration-200"
                      >
                        {subcategory}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}