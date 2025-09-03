"use client";
import React from "react";

export default function FlightResult({
  dateRange = "Nov 22 - Nov 24",
  route = "DANDONG - KUDAHUVADHOO",
  travelers = "2 adults",
  tabs = ["Best", "Cheapest", "Fastest"],
  activeTab = "Best",
  onTabChange = () => {},
  flight = {},
  providersCount = 6,
}) {
  const {
    airlineName = "United Airlines",
    segments = [],
    price = "Nok 0",
    ticketCount = 0,
    onChoose = () => {},
  } = flight;

  return (
    
    <div className="space-y-6 py-8 md:py-16">

      <div className="flex flex-col sm:flex-row items-center sm:justify-around text-center space-y-2 sm:space-y-0">
        <div className="flex flex-col">
          <span className="font-bold text-xl text-gray-900">{dateRange}</span>
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-xl text-gray-900">{route}</span>
        </div>
        <div className="flex flex-col">
          <span className="font-bold text-xl text-gray-900">{travelers}</span>
        </div>
      </div>

      <div className="flex justify-between px-4 sm:px-8 md:px-16 lg:px-32 space-x-2 sm:space-x-8 border-b border-gray-300 pb-2">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => onTabChange(tab)}
            className={`
              text-sm font-semibold 
              px-4 sm:px-8 md:px-12 
              ${activeTab === tab ? "text-gray-900 border-b-2 border-teal-600" : "text-gray-600 hover:text-gray-900"}
            `}
          >
            {tab}
          </button>
        ))}
      </div>

     
      <div className="border rounded-md p-4 flex flex-col sm:flex-row justify-between space-y-4 sm:space-y-0">
      
        <div className="space-y-1 flex-1">
          <div className="font-semibold text-gray-900">{airlineName}</div>
          {segments.map((segment, idx) => (
            <div key={idx} className="p-3 mt-2">
              <div className="flex flex-wrap gap-2 items-center text-sm text-gray-900">
                <span className="font-bold">{segment.from}</span>
                <span>{segment.departureTime}</span>
                <span className="text-xs text-gray-700">
                  {segment.duration} {segment.direct ? "- direct" : ""}
                </span>
                <span>{segment.arrivalTime}</span>
                <span className="font-bold">{segment.to}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Right: Price & Action */}
        <div className="flex flex-col items-end space-y-2 min-w-[120px]">
          <div className="text-gray-700 text-xs">
            {ticketCount} <span className="ml-1">Ticket</span>
          </div>
          <div className="text-xl font-bold text-gray-900">{price}</div>
          <button
            onClick={onChoose}
            className="bg-teal-500 text-white px-4 py-2 rounded-md font-semibold hover:bg-teal-600"
          >
            Choose the journey
          </button>
        </div>
      </div>

      {/* Show details */}
      <div className="text-center">
        <button className="text-teal-700 text-sm font-semibold hover:underline">
          Show details and all {providersCount} providers
        </button>
      </div>
    </div>
  );
}