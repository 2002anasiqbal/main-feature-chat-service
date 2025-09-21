"use client";
import React from "react";
import Image from "next/image";

export default function MapAdCard({
  imageUrl = "/assets/carcarvan/car.svg", // Default image
  brand = "Toyota",
  model = "Toyota Land Cruiser",
  year = "2014",
  mileage = "15000 km",
  price = "NOK 180000",
  outlet = "Car outlet",
  warranty = "12 month warranty",
}) {
  return (
    <div className="flex items-center bg-white shadow-md rounded-lg overflow-hidden border border-gray-200 max-w-md">
      {/* Image Section */}
      <div className="w-1/3">
        <Image
          src={imageUrl}
          alt={model}
          width={120}
          height={100}
          className="object-cover w-full h-full"
        />
      </div>

      {/* Details Section */}
      <div className="p-4 flex-1">
        {/* Brand Name */}
        <h3 className="font-bold text-lg text-gray-900">{brand}</h3>
        
        {/* Model & Year */}
        <p className="text-sm text-gray-700">{model}</p>
        <p className="text-sm text-gray-600 mt-1">
          {year} &nbsp; | &nbsp; {mileage} &nbsp; | &nbsp; {price}
        </p>

        {/* Outlet & Warranty */}
        <p className="text-sm text-gray-700 mt-2">{outlet}</p>
        <p className="text-sm text-gray-600">{warranty}</p>
      </div>
    </div>
  );
}
