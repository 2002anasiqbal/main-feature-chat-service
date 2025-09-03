// In BoatGrid.jsx
"use client";
import React from "react";
import BoatCard from "./BoatCard";

const BoatGrid = ({ boats, columns = 3, route = "/routes/boat" }) => {
  if (!boats || boats.length === 0) {
    return <p className="text-center py-4">No boats found.</p>;
  }

  // Format boats data
  const formattedBoats = boats.map(boat => {
    // Check for different image formats
    let primaryImage = null;
    
    if (boat.primary_image) {
      primaryImage = boat.primary_image;
    } else if (boat.images && boat.images.length > 0) {
      // Find primary image or use first one
      const primary = boat.images.find(img => img.is_primary);
      primaryImage = primary ? primary.image_url : boat.images[0].image_url;
    }
    
    console.log(`Boat ${boat.id} image:`, primaryImage);
    
    return {
      id: boat.id,
      image: primaryImage,
      title: boat.title || "Unnamed Boat",
      description: boat.make && boat.model 
        ? `${boat.make} ${boat.model}`.trim() 
        : boat.location_name || "No details available",
      price: boat.price ? `$${boat.price.toLocaleString()}` : "Price unavailable",
    };
  });

  return (
    <div className="min-h-screen bg-white pb-10">
      <div className="w-full">
        <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-${columns} gap-4 md:gap-6`}>
          {formattedBoats.map((boat) => (
            <BoatCard
              key={boat.id}
              id={boat.id}
              image={boat.image}
              title={boat.title}
              description={boat.description}
              price={boat.price}
              route={`${route}/${boat.id}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default BoatGrid;