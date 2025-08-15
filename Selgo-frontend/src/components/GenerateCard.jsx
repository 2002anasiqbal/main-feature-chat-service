// Selgo-frontend/src/components/GenerateCard.jsx (Updated for Property Integration)
"use client";
import React, { useState, useEffect } from "react";
import BoatCard from "./boat/BoatCard";
import boatService from "@/services/boatService";
import motorcycleService from "@/services/motorcycleService";
import propertyService from "@/services/propertyService"; // NEW IMPORT

const Page = ({ 
  columns = 3, 
  route, 
  cards: initialCards = null,
  disableAutoFetch = false
}) => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (disableAutoFetch && !initialCards) {
      setLoading(true);
      return;
    }

    if (initialCards !== null && initialCards !== undefined) {
      console.log("Using provided cards:", initialCards);
      
      const formattedCards = initialCards.map(item => {
        if (item.image !== undefined && item.title && item.description && item.price) {
          return item;
        }
        
        // Handle property data using existing format
        if (route && route.includes('property')) {
          return {
            id: item.id,
            image: item.primary_image || item.image || "/assets/property/property.jpeg",
            title: item.title || "Unnamed Property",
            description: item.description || propertyService.formatPropertyDescription(item),
            price: item.price ? `$${Number(item.price).toLocaleString()}` : "Price unavailable",
            originalData: item
          };
        } else if (route && route.includes('motor-cycle')) {
          // Existing motorcycle formatting
          return {
            id: item.id,
            image: item.primary_image || item.image || "/assets/swiper/1.jpg",
            title: item.title || "Unnamed Motorcycle",
            description: item.brand && item.model 
              ? `${item.brand} ${item.model} - ${item.year}`.trim() 
              : item.description || "No details available",
            price: item.price ? `$${item.price.toLocaleString()}` : "Price unavailable",
            originalData: item
          };
        } else {
          // Existing boat/default formatting - NO CHANGES
          return {
            id: item.id,
            image: item.primary_image || (item.images && item.images.length > 0 ? item.images[0].image_url : null),
            title: item.title || "Unnamed Item",
            description: item.make && item.model 
              ? `${item.make} ${item.model}`.trim() 
              : item.location_name || "No details available",
            price: item.price ? `$${item.price.toLocaleString()}` : "Price unavailable",
            originalData: item
          };
        }
      });
      
      setCards(formattedCards);
      setLoading(false);
      return;
    }

    if (!disableAutoFetch) {
      const fetchCards = async () => {
        try {
          console.log("GenerateCard is fetching its own data...");
          setLoading(true);
    
          let response;
          if (route && route.includes('boat')) {
            // Existing boat logic - NO CHANGES
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
            
          } else if (route && route.includes('motor-cycle')) {
            // Existing motorcycle logic - NO CHANGES
            const motorcycles = await motorcycleService.getHomepageMotorcycles(10);
            
            const formattedMotorcycles = motorcycles.map(motorcycle => 
              motorcycleService.formatMotorcycleForDisplay(motorcycle)
            );
            setCards(formattedMotorcycles);
            
          } else if (route && route.includes('property')) {
            // NEW: Property logic
            const properties = await propertyService.getHomepageProperties(10);
            setCards(properties); // Already formatted by service
            
          } else {
            // Existing default logic - NO CHANGES
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
    // Existing function - NO CHANGES
    return Array.from({ length: count }, (_, i) => ({
      id: i.toString(),
      image: `https://picsum.photos/300/200?random=${Math.floor(Math.random() * 1000)}`,
      title: `Product ${i + 1}`,
      description: "Lorem ipsum dolor sit amet",
      price: `${(Math.random() * 1000).toFixed(2)}`,
    }));
  };

  // Existing render logic - NO CHANGES
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