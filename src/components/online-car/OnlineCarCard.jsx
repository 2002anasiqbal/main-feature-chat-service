"use client";
import React from "react";
import Image from "next/image";

const OnlineCarCard = ({
  image = "/assets/online-car/carCard.svg", // Default placeholder image
  title = "Tesla MODEL 3 LONG RANGE AWD | FSD | Premium Sound | H. Fastening",
  details = ["2020", "45,000 km", "Automatic", "Electric"],
}) => {
  return (
    <div className="relative w-full max-w-md rounded-lg overflow-hidden shadow-lg">
      {/* Car Image */}
      <Image
        src={image}
        alt="Car"
        width={500}
        height={300}
        className="w-full object-cover"
      />

      {/* Overlay Section */}
      <div className="absolute bottom-0 w-full bg-gray-400/40 text-white p-4 rounded-lg">
        <h3 className="text-sm font-semibold">{title}</h3>
        <ul className="text-xs mt-1">
          {details.map((item, index) => (
            <li key={index} className="list-disc list-inside">
              {item}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default OnlineCarCard;