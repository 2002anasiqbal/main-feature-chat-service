"use client";
import React from "react";
import Image from "next/image";

const OnlineCarSquare = ({
  icon, 
  title, 
  description, 
  size = 150, // Default size (150x150)
  iconSize = 40, // Default icon size
}) => {
  return (
    <div 
      className="flex flex-col items-center justify-center bg-white shadow-md rounded-lg border border-gray-200 p-4 text-center"
      style={{ width: `${size}px`, height: `${size}px` }} // Dynamically set width & height
    >
      {/* Icon/Image */}
      {icon && (
        <Image
          src={icon}
          alt={title}
          width={iconSize}
          height={iconSize}
          className="mb-2"
        />
      )}

      {/* Title */}
      <h3 className="text-sm font-semibold text-gray-900">{title}</h3>

      {/* Description */}
      <p className="text-xs text-gray-600">{description}</p>
    </div>
  );
};

export default OnlineCarSquare;
