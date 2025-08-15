"use client";
import React from "react";

// Individual Tile Component
function InformationTile({ 
  title, 
  description, 
  buttonText = "Read More", 
  imageUrl, 
  imagePosition = "left", 
  onClick 
}) {
  const handleClick = onClick || (() => console.log("Button clicked"));

  return (
    <div className="flex flex-col md:flex-row items-center gap-20 my-8">
      {/* Conditional rendering based on image position */}
      {imagePosition === "left" && (
        <div className="w-full md:w-1/3">
          <div className="rounded-lg overflow-hidden">
            <img 
              src={imageUrl} 
              alt={`${title || 'Information'} illustration`} 
              className="w-full h-40 object-cover"
            />
          </div>
        </div>
      )}

      <div className="w-full md:w-2/3 flex flex-col justify-center">
        {title && <h2 className="text-2xl font-semibold text-gray-700 mb-2">{title}</h2>}
        
        {description && <p className="text-gray-700 mb-4">{description}</p>}
        
        <div>
          <button 
            onClick={handleClick}
            className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-2 px-6 rounded transition duration-200"
          >
            {buttonText}
          </button>
        </div>
      </div>

      {/* Conditional rendering based on image position */}
      {imagePosition === "right" && (
        <div className="w-full md:w-1/3">
          <div className="rounded-lg overflow-hidden">
            <img 
              src={imageUrl} 
              alt={`${title || 'Information'} illustration`} 
              className="w-full h-40 object-cover"
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Main Component that renders a list of tiles with alternating positions
export default function InformationTiles({ tiles = [] }) {
  return (
    <div className="w-full">
      {tiles.map((tile, index) => (
        <InformationTile
          key={index}
          title={tile.title}
          description={tile.description}
          buttonText={tile.buttonText || "Read More"}
          imageUrl={tile.imageUrl}
          imagePosition={index % 2 === 0 ? "left" : "right"}
          onClick={tile.onClick}
        />
      ))}
    </div>
  );
}

