"use client";
import React from "react";
import Image from "next/image";

const FlightTicketCard = ({ imageUrl, city, country, large }) => {
  return (
    <div
      className={`relative overflow-hidden rounded-lg shadow-md bg-white transition-transform duration-300 hover:scale-105
        ${large ? "h-80 sm:h-96" : "h-60"} `}
    >
      <Image
        src={imageUrl}
        alt={`Ticket to ${city}, ${country}`}
        width={600}
        height={400}
        className="w-full h-full object-cover"
      />
      <div className="p-4 absolute bottom-0 left-0 w-full bg-white bg-opacity-80">
        <p className="text-sm text-gray-500">Ticket to</p>
        <h3 className="text-lg font-semibold text-gray-800">{city}, {country}</h3>
      </div>
    </div>
  );
};

export default FlightTicketCard;