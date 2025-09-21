"use client";
import { useState } from "react";
import FindFlight from "@/components/travel/FindFlight";
import FlightResult from "@/components/travel/FlightResults";
import TravelSidebar from "@/components/travel/TravelSidebar";

export default function FlightSearch() {
  const [activeTab, setActiveTab] = useState("Best");

  const flightDataByTab = {
    Best: [
      {
        airlineName: "United Airlines",
        segments: [
          { from: "EWR", departureTime: "21:45", duration: "12h55", arrivalTime: "19:40", to: "DXB", direct: true },
          { from: "DXB", departureTime: "02:15", duration: "15h20", arrivalTime: "08:35", to: "EWR", direct: true },
        ],
        price: "Nok 9,225",
        ticketCount: 0,
        onChoose: () => alert("Journey chosen"),
      },
    ],
    Cheapest: [
      {
        airlineName: "CheapAir",
        segments: [
          { from: "EWR", departureTime: "22:00", duration: "18h05", arrivalTime: "16:05", to: "DXB", direct: false },
          { from: "DXB", departureTime: "02:25", duration: "20h40", arrivalTime: "23:05", to: "EWR", direct: false },
        ],
        price: "Nok 7,500",
        ticketCount: 1,
        onChoose: () => alert("Cheapest flight selected"),
      },
    ],
    Fastest: [
      {
        airlineName: "SpeedyFlights",
        segments: [
          { from: "EWR", departureTime: "09:00", duration: "10h10", arrivalTime: "19:10", to: "DXB", direct: true },
          { from: "DXB", departureTime: "01:00", duration: "10h00", arrivalTime: "11:00", to: "EWR", direct: true },
        ],
        price: "Nok 10,300",
        ticketCount: 2,
        onChoose: () => alert("Fastest flight selected"),
      },
    ],
  };

  return (

    <div className="flex flex-col lg:flex-row gap-6">
      
      {/* Sidebar: full width on small screens, fixed width on large */}
      <div className="w-full lg:w-64 flex-shrink-0">
        <TravelSidebar />
      </div>

      {/* Main Content grows to fill remaining space */}
      <div className="flex-grow">
        <FindFlight />
        <FlightResult
          dateRange="Nov 22 - Nov 24"
          route="DANDONG - KUDAHUVADHOO"
          travelers="2 adults"
          tabs={["Best", "Cheapest", "Fastest"]}
          activeTab={activeTab}
          onTabChange={setActiveTab}
          flight={flightDataByTab[activeTab][0]}
          providersCount={6}
        />
      </div>
    </div>
  );
}
