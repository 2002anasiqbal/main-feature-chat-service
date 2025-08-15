"use client";
import React from "react";

const TwoButtonComponent = ({
  primaryLabel = "Primary Button",
  secondaryLabel = "Secondary Button",
  onPrimaryClick = () => console.log("Primary Clicked"),
  onSecondaryClick = () => console.log("Secondary Clicked"),
}) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md w-full max-w-md">
      {/* Header */}
      <h2 className="text-lg font-semibold text-gray-900">Display</h2>
      <p className="text-gray-600 mt-1">Tuesday, November 19</p>

      {/* Description */}
      <p className="text-gray-500 text-sm mt-2">
        Sign up for a viewing or contact the estate agent for a private viewing. Viewing will not be carried out without registration.
      </p>

      {/* Button Section */}
      <div className="flex flex-col sm:flex-row gap-4 mt-4">
        {/* Secondary Button */}
        <button
          className="px-5 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-100 transition-all"
          onClick={onSecondaryClick}
        >
          {secondaryLabel}
        </button>

        {/* Primary Button */}
        <button
          className="px-5 py-2 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all"
          onClick={onPrimaryClick}
        >
          {primaryLabel}
        </button>
      </div>
    </div>
  );
};

export default TwoButtonComponent;