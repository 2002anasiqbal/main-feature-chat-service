"use client";
import { useState } from "react";

const mockCategories = [
  { title: "The Square", description: "Find local shops, deals, and services in your area." },
  { title: "Car and Caravan", description: "Buy, sell, or rent cars, caravans, and trailers." },
  { title: "Property", description: "Explore houses, apartments, and land for sale or rent." },
  { title: "Boat", description: "Browse boats, yachts, and marine equipment for sale." },
  { title: "Holiday homes and cabins", description: "Discover vacation rentals and holiday homes." },
  { title: "Motorcycle", description: "Buy or sell motorcycles, parts, and accessories." },
  { title: "My Tender", description: "Post and find tendering opportunities and contracts." },
  { title: "Job", description: "Find jobs or post job listings in different industries." },
  { title: "Nutrition", description: "Health supplements, organic food, and meal plans." },
];

export default function CreateAd() {
  const [openIndex, setOpenIndex] = useState(null);

  const handleToggle = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="w-full min-h-screen bg-white flex justify-center">
      <div className="w-full bg-white py-8">
        <h1 className="text-2xl font-bold mb-6 text-gray-900">Create a New Ad</h1>

        <div className="space-y-2">
          {mockCategories.map((category, index) => (
            <div key={index} className="border border-gray-300 rounded-md overflow-hidden">
              <button
                onClick={() => handleToggle(index)}
                className="w-full flex justify-between items-center p-4 text-left text-gray-800 font-medium bg-white hover:bg-gray-100 transition-all duration-200"
              >
                <span>{category.title}</span>
                <span className="text-gray-500">{openIndex === index ? "▲" : "▼"}</span>
              </button>

              {openIndex === index && (
                <div className="p-4 bg-gray-50 text-gray-600 transition-all duration-300">
                  {category.description}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}