"use client";
import React from "react";
import Image from "next/image";

const TravelDestinationCard = ({ imageSrc, title, destinations }) => {
  return (
    <div className="flex flex-col items-center text-left">
      {/* Category Icon */}
      <Image src={imageSrc} alt={title} width={150} height={150} className="mb-3" />

      {/* Category Title */}
      <div className="bg-teal-700 text-white font-semibold px-6 py-2 w-full max-w-xs">
        {title}
      </div>

      {/* Destinations List */}
      <ul className="w-full max-w-xs bg-white">
        {destinations.map((destination, index) => (
          <li key={index} className="py-2 px-4 border-b border-gray-200 text-gray-700">
            {destination}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TravelDestinationCard;