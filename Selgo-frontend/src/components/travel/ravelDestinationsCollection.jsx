"use client";
import React from "react";
import TravelDestinationCard from "./TravelDestinationCard";

const travelDestinations = [
  {
    imageSrc: "/assets/travel/1.svg",
    title: "Europe",
    destinations: ["France", "Island", "Greece", "Croatia", "Hungary"],
  },
  {
    imageSrc: "/assets/travel/2.svg",
    title: "Asia",
    destinations: ["Cyprus", "Maldives", "Sri Lanka", "Japan", "Georgia"],
  },
  {
    imageSrc: "/assets/travel/3.svg",
    title: "Africa",
    destinations: ["Egypt", "Mauritius", "Seychelles", "Cape Verde", "Angola"],
  },
  {
    imageSrc: "/assets/travel/4.svg",
    title: "North-Amerika",
    destinations: ["Canada", "Mexico", "Bahamas", "Cuba", "Jamaica"],
  },
  {
    imageSrc: "/assets/travel/5.svg",
    title: "South-America",
    destinations: ["Brazil", "Argentina", "Chile", "Venezuela", "Colombia"],
  },
  {
    imageSrc: "/assets/travel/6.svg",
    title: "Oceania",
    destinations: ["Australia", "New Zealand", "Cook Island", "Fiji", "French Polynesia"],
  },
];

const TravelDestinationsCollection = () => {
  return (
    <div className="w-full max-w-6xl mx-auto text-center">
      <h2 className="text-2xl font-semibold text-gray-800">
        Find plane tickets to several exciting destinations
      </h2>
      <p className="text-gray-600 mb-6">
        The world is full of exciting new destinations. If you don’t know where your next trip should go, we give you inspiration here.
      </p>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
        {travelDestinations.map((category, index) => (
          <TravelDestinationCard key={index} {...category} />
        ))}
      </div>
    </div>
  );
};

export default TravelDestinationsCollection;