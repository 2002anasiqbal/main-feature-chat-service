"use client";
import React from "react";
import OnlineCarCard from "./OnlineCarCard";
const cars = [
  {
    image: "/assets/online-car/carCard.svg",
    title: "Tesla MODEL 3 LONG RANGE AWD | FSD | Premium Sound | H. Fastening",
    details: ["2020", "45,000 km", "Automatic", "Electric"],
  },
  {
    image: "/assets/online-car/carCard.svg",
    title: "BMW iX M60 | High Performance | Sport Package",
    details: ["2023", "10,000 km", "Automatic", "Electric"],
  },
  {
    image: "/assets/online-car/carCard.svg",
    title: "Mercedes EQS 580 4MATIC | AMG Line | Luxury Interior",
    details: ["2022", "20,000 km", "Automatic", "Electric"],
  },
  {
    image: "/assets/online-car/carCard.svg",
    title: "Audi e-tron GT RS | Quattro | Performance Edition",
    details: ["2021", "30,000 km", "Automatic", "Electric"],
  },
  {
    image: "/assets/online-car/carCard.svg",
    title: "Porsche Taycan Turbo S | High-Performance EV",
    details: ["2021", "15,000 km", "Automatic", "Electric"],
  },
  {
    image: "/assets/online-car/carCard.svg",
    title: "Lucid Air Grand Touring | 1000 HP | Luxury Sedan",
    details: ["2023", "5,000 km", "Automatic", "Electric"],
  },
];

const CarCollection = () => {
  return (
    <div className="w-full py-4">
      {/* Section Title */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Examples of cars</h2>

      {/* Car Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {cars.map((car, index) => (
          <OnlineCarCard
            key={index}
            image={car.image}
            title={car.title}
            details={car.details}
          />
        ))}
      </div>
    </div>
  );
};

export default CarCollection;