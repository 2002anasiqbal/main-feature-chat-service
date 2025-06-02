"use client";
import React from "react";
import Image from "next/image";

const cities = [
    "Oslo",
    "Bergen",
    "Trondheim",
    "Stavanger",
    "Drammen",
    "Kristiansand",
    "Tromsø",
    "Ålesund",
];

export default function PopularCitiesGrid() {
    return (
        <div className="w-full mt-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
                Popular cities to rent in
            </h2>

            {/* Grid Layout */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
                {cities.map((city, index) => (
                    <div 
                        key={index} 
                        className="relative rounded-lg overflow-hidden shadow-md transition-transform duration-300 hover:scale-105 hover:shadow-lg"
                    >
                        {/* Dynamic Image from Picsum.photos */}
                        <Image
                            src={`https://picsum.photos/300/200?random=${index}`}
                            alt={city}
                            width={300}
                            height={200}
                            className="w-full h-40 object-cover"
                        />
                        {/* Overlay with City Name */}
                        <div className="absolute bottom-0 left-0 right-0 bg-black bg-opacity-40 p-2 text-white text-sm">
                            {city}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}