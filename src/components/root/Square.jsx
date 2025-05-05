// components/root/Square.jsx
"use client";
import React, { useState } from "react";
import Image from "next/image";

const SquareCard = ({
  Icon,
  IconComponent, // Prop to accept React icons
  tag,
  description = "",
  showDetails = false,
  onClick,
  size = "w-full h-auto sm:w-25 sm:h-25",
  iconProps = {}, // Props to pass to the IconComponent
}) => {
  const [isLoading, setIsLoading] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  
  const handleClick = async () => {
    if (isLoading) return;
    setIsLoading(true);
    try {
      onClick();
    } catch (error) {
      console.error("Error:", error);
    }
    setIsLoading(false);
  };
  
  // Create the glow style that will be applied when hovered
  const iconStyle = isHovered ? {
    filter: 'drop-shadow(0 0 8px rgba(20, 184, 166, 0.99))',
    transition: 'filter 0.3s ease'
  } : {
    transition: 'filter 0.3s ease'
  };
  
  // Apply default icon styling (teal-700 color, size 24) if not specified in iconProps
  const defaultIconProps = {
    size: 24,
    className: "text-teal-700",
    style: iconStyle,
    ...iconProps, // Custom props will override defaults
    // Merge styles if iconProps already has a style object
    ...(iconProps.style ? { style: { ...iconStyle, ...iconProps.style } } : {})
  };
  const iconHoverClass =
    "transition-all duration-200 hover:drop-shadow-[0_0_1px_rgba(20,184,166,0.65)] transform hover:scale-102";

  return (
    <div
      className={`${size} ${iconHoverClass} flex flex-col items-center justify-center bg-white shadow-md rounded-sm sm:rounded-xl p-4 cursor-pointer hover:shadow-lg hover:scale-105 transition-transform duration-200 ${
        isLoading ? "opacity-50 cursor-not-allowed" : ""
      }`}
      onClick={handleClick}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative">
        {isLoading ? (
          <span>Loading...</span>
        ) : IconComponent ? (
          <IconComponent {...defaultIconProps} />
        ) : (
          Icon && (
            <div style={iconStyle}>
              <Icon className="w-6 h-6 text-teal-700" />
            </div>
          )
        )}
      </div>
      <p className="text-sm text-gray-800 mt-2 text-center">{tag}</p>
      {description && <p className="text-xs text-gray-500 text-center mt-1">{description}</p>}
      {showDetails && <p className="text-xs text-gray-500 text-center mt-1">See details</p>}
    </div>
  );
};

export default SquareCard;