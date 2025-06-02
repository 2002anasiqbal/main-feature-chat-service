"use client";
import React, { useState, useEffect } from "react";
import BoatCard from "./boat/BoatCard";
import boatService from "@/services/boatService";

const Page = ({ 
  columns = 3, 
  route, 
  cards: initialCards = null,
  disableAutoFetch = false  // New prop to explicitly disable auto-fetching
}) => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // If auto-fetch is disabled and no cards provided yet, just wait
    if (disableAutoFetch && !initialCards) {
      setLoading(true);
      return;
    }

    // If cards are provided as props, use them
    if (initialCards !== null && initialCards !== undefined) {
      console.log("Using provided cards:", initialCards);
      
      const formattedCards = initialCards.map(boat => {
        // Check if already formatted
        if (boat.image !== undefined && boat.title && boat.description && boat.price) {
          return boat;
        }
        
        // Format raw boat data
        return {
          id: boat.id,
          image: boat.primary_image || (boat.images && boat.images.length > 0 ? boat.images[0].image_url : null),
          title: boat.title || "Unnamed Boat",
          description: boat.make && boat.model 
            ? `${boat.make} ${boat.model}`.trim() 
            : boat.location_name || "No details available",
          price: boat.price ? `$${boat.price.toLocaleString()}` : "Price unavailable",
          originalData: boat
        };
      });
      
      setCards(formattedCards);
      setLoading(false);
      return;
    }

    // Only fetch if auto-fetch is NOT disabled
    if (!disableAutoFetch) {
       const fetchCards = async () => {
        try {
          console.log("GenerateCard is fetching its own data...");
          setLoading(true);
    
    let response;
    if (route && route.includes('boat')) {
      // Use the new homepage boats endpoint for main homepage
      const boats = await boatService.getHomepageBoats(10);
      
      const formattedBoats = boats.map(boat => ({
        id: boat.id,
        image: boat.primary_image,
        title: boat.title || "Unnamed Boat",
        description: boat.make && boat.model 
          ? `${boat.make} ${boat.model}`.trim() 
          : boat.location_name || "No details available",
        price: boat.price ? `$${boat.price.toLocaleString()}` : "Price unavailable",
        originalData: boat
      }));
      setCards(formattedBoats);
      
     
    } else {
      setCards(generateMockCards(10));
    }
  } catch (err) {
    console.error("Failed to fetch cards:", err);
    setError("Failed to load data");
  } finally {
    setLoading(false);
  }
};
      fetchCards();
    }
  }, [initialCards, route, disableAutoFetch]);

  const generateMockCards = (count) => {
    return Array.from({ length: count }, (_, i) => ({
      id: i.toString(),
      image: `https://picsum.photos/300/200?random=${Math.floor(Math.random() * 1000)}`,
      title: `Product ${i + 1}`,
      description: "Lorem ipsum dolor sit amet",
      price: `$${(Math.random() * 1000).toFixed(2)}`,
    }));
  };

  if (loading) return <p className="text-center py-10">Loading...</p>;
  if (error) return <p className="text-center py-10 text-red-500">{error}</p>;
  if (cards.length === 0 && disableAutoFetch) {
    return <p className="text-center py-10">No items to display</p>;
  }

  return (
    <div className="min-h-screen bg-white pb-10">
      <div className="w-full">
        <div className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-${columns} gap-4 md:gap-6`}>
          {cards.map((card) => (
            <BoatCard
              key={card.id}
              id={card.id}
              image={card.image}
              title={card.title}
              description={card.description}
              price={card.price}
              route={`${route}/${card.id}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Page;