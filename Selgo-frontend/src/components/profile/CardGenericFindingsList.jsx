"use client";
import React, { useState } from "react";

export default function CardGenericFindingsList({ findings = [] }) {
  const [openMenuIndex, setOpenMenuIndex] = useState(null);
  
  // If no findings are provided, create a default one based on the image
  const defaultFindings = findings.length > 0 ? findings : [
    {
      title: "Sold to higest bidder",
      price: "100",
      status: "For sale",
      link: "#"
    }
  ];

  return (
    <div className="space-y-4 w-full">
      {defaultFindings.map((finding, index) => (
        <div 
          key={index} 
          className="relative flex items-start p-4 border border-gray-200 rounded-lg shadow-sm w-full"
        >
          {/* Image Placeholder */}
          <div className="w-24 h-24 bg-gray-200 rounded-md mr-4 flex-shrink-0"></div>
          
          {/* Main Content Area */}
          <div className="flex-1 flex">
            {/* Finding Details */}
            <div className="flex-grow">
              <h3 className="font-medium text-gray-800">{finding.title}</h3>
              <p className="text-base text-gray-800">{finding.price}</p>
              <p className="text-sm text-gray-600">{finding.status}</p>
            </div>
            
            {/* Menu Section */}
            <div className="relative">
              {/* Menu Toggle Button - Three Dots or X */}
              <button 
                className="text-gray-500 p-2 rounded-full hover:bg-gray-100"
                onClick={() => setOpenMenuIndex(openMenuIndex === index ? null : index)}
              >
                {openMenuIndex === index ? (
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="1"></circle>
                    <circle cx="12" cy="5" r="1"></circle>
                    <circle cx="12" cy="19" r="1"></circle>
                  </svg>
                )}
              </button>
              
              {/* Dropdown Menu */}
              {openMenuIndex === index && (
                <div className="absolute right-0 top-10 z-10 bg-white border border-gray-200 rounded-md shadow-md w-48">
                  <button 
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700 border-b border-gray-200"
                    onClick={() => {
                      navigator.clipboard.writeText(finding.link);
                      setOpenMenuIndex(null);
                    }}
                  >
                    Copy the link to ad
                  </button>
                  <button 
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700 border-b border-gray-200"
                    onClick={() => setOpenMenuIndex(null)}
                  >
                    Add note
                  </button>
                  <button 
                    className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700"
                    onClick={() => setOpenMenuIndex(null)}
                  >
                    Remove favourite
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}