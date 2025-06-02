"use client";
import React from "react";
import FlightTicketCard from "./FlightTicketCard";

const flightTickets = [
    { imageUrl: "https://picsum.photos/600/400?random=1", city: "Oslo", country: "Norway", large: true },
    { imageUrl: "https://picsum.photos/600/400?random=2", city: "Bergen", country: "Norway", large: true },
    { imageUrl: "https://picsum.photos/600/400?random=3", city: "Alicante", country: "Spain" },
    { imageUrl: "https://picsum.photos/600/400?random=4", city: "Gran Canaria", country: "Spain" },
    { imageUrl: "https://picsum.photos/600/400?random=5", city: "London", country: "UK" },
    { imageUrl: "https://picsum.photos/600/400?random=6", city: "New York", country: "USA" },
    { imageUrl: "https://picsum.photos/600/400?random=7", city: "Bangkok", country: "Thailand" },
    { imageUrl: "https://picsum.photos/600/400?random=8", city: "Amsterdam", country: "Netherlands" },
];

const FlightTicketCollection = () => {
    return (
        <div>
            <div className="w-full text-left pb-20 pt-5">
                <h2 className="text-2xl font-semibold text-center text-gray-800">Find cheap flights to popular cities</h2>
                <p className="text-gray-600 mb-6 text-center">Here is a selection of the most popular cities with cheap flights.</p>

                {/* First Row - 2 Large Cards */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
                    {flightTickets.slice(0, 2).map((ticket, index) => (
                        <FlightTicketCard key={index} {...ticket} large />
                    ))}
                </div>

                {/* Rest of the cards - 3 cards per row */}
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {flightTickets.slice(2).map((ticket, index) => (
                        <FlightTicketCard key={index} {...ticket} />
                    ))}
                </div>
            </div>
        </div>
    );
};

export default FlightTicketCollection;