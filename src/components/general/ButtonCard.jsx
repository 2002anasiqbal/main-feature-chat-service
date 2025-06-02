"use client";
import React, { useState } from "react";

const ButtonCard = ({
  title = "Do you need a contract?",
  listItems = [
    "Completed contract with advertisement info",
    "Digital signing",
    "Free service",
    "Approved by Consumer Council"
  ],
  buttonText = "Compare Favourite Homes",
  onClick,
  showSlider = false,
}) => {
  const [sliderValue, setSliderValue] = useState(50);

  return (
    <div className="w-full max-w-sm p-4 bg-white shadow-md rounded-lg border border-gray-200">
      {/* Title */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
      
      {/* Custom list with proper line breaks */}
      <div className="text-sm text-gray-700 mb-4">
        {listItems.map((item, index) => (
          <div key={index} className="mb-1">
            <span className="mr-1">•</span> {item}
          </div>
        ))}
      </div>

      {/* Conditional Slider */}
      {showSlider && (
        <div className="mb-4">
          <input
            type="range"
            min="0"
            max="100"
            value={sliderValue}
            onChange={(e) => setSliderValue(e.target.value)}
            className="w-full accent-teal-500"
          />
          <div className="flex justify-between text-xs text-gray-600 mt-1">
            <span>0</span>
            <span>{sliderValue}</span>
            <span>100</span>
          </div>
        </div>
      )}

      {/* Button */}
      <button
        onClick={onClick}
        className="w-full px-4 py-2 bg-teal-600 text-white font-medium rounded-md hover:bg-teal-600 transition"
      >
        {buttonText}
      </button>
    </div>
  );
};

export default ButtonCard;