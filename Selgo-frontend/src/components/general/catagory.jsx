"use client";
import { useState } from "react";
import { categoriesData } from "@/data/categoriesData";
import { FaAngleDown } from "react-icons/fa";

export default function CategoriesSelector() {
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [selectedSubcategories, setSelectedSubcategories] = useState([]);

  // Handle category selection
  const handleCategoryClick = (categoryName) => {
    setSelectedCategory(categoryName === selectedCategory ? null : categoryName);
  };

  // Handle subcategory selection
  const handleSubcategoryClick = (subcategoryName) => {
    setSelectedSubcategories((prev) =>
      prev.includes(subcategoryName)
        ? prev.filter((sub) => sub !== subcategoryName)
        : [...prev, subcategoryName]
    );
  };

  return (
    <div className="max-w-sm mx-auto pr-4 bg-white">
      {/* Categories List */}
      <div className="space-y-2">
        {categoriesData.map((category, index) => (
          <div key={index}>
            {/* Category Button */}
            <button
              className={`w-full py-2 px-4 flex items-center justify-between cursor-pointer border-b ${
                selectedCategory === category.name
                  ? "border-teal-600 text-teal-600"
                  : "border-gray-300 text-gray-700"
              }`}
              onClick={() => handleCategoryClick(category.name)}
            >
              <span className="text-left w-full">{category.name}</span>
              <span
                className={`transition-transform ${
                  selectedCategory === category.name ? "rotate-180" : ""
                }`}
              >
                <FaAngleDown />
              </span>
            </button>

            {/* Subcategories */}
            {selectedCategory === category.name && (
              <div className="ml-4 mt-2 space-y-2">
                {category.subcategories.map((sub, subIndex) => (
                  <button
                    key={subIndex}
                    className={`flex justify-between items-center w-full py-1 px-4 border-b text-sm ${
                      selectedSubcategories.includes(sub.name)
                        ? "border-teal-500 text-teal-500 bg-teal-100"
                        : "border-gray-300 text-gray-600"
                    }`}
                    onClick={() => handleSubcategoryClick(sub.name)}
                  >
                    {sub.name}
                    <span className="text-lg">
                      {selectedSubcategories.includes(sub.name) ? "✔" : "+"}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}