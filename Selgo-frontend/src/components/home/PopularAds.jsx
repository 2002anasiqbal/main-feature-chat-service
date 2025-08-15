"use client";
import React, { useEffect, useState } from "react";
import SimpleCard from "../root/Card";
import { MdChevronLeft, MdChevronRight } from "react-icons/md";
import boatService from "@/services/boatService";

const PopularAds = () => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [perPage, setPerPage] = useState(3);
  const [startIndex, setStartIndex] = useState(0);
  
  // Responsive perPage count
  useEffect(() => {
    const calc = () => {
      if (window.innerWidth >= 1024) setPerPage(3);
      else if (window.innerWidth >= 768) setPerPage(2);
      else setPerPage(1);
    };
    calc();
    window.addEventListener("resize", calc);
    return () => window.removeEventListener("resize", calc);
  }, []);

  // Fetch data with newly created boat prioritized
useEffect(() => {
  // Replace the fetchBoats function:

  const fetchBoats = async () => {
    try {
      setLoading(true);
      // Use the new featured boats endpoint
      const boats = await boatService.getFeaturedBoats(10);
      
      if (boats && boats.length > 0) {
        const formattedBoats = boats.map(boat => ({
          id: boat.id,
          image: boat.primary_image || "/assets/swiper/1.jpg",
          title: boat.title || "Boat",
          description: boat.make && boat.model ? 
                      `${boat.make} ${boat.model}` : 
                      "No description",
          price: boat.price ? `$${boat.price.toLocaleString()}` : "$0",
          route: `/routes/boat/${boat.id}`
        }));
        
        setCards(formattedBoats);
      }
    } catch (error) {
      console.error("Failed to fetch featured boats:", error);
    } finally {
      setLoading(false);
    }
  };

  fetchBoats();
}, []);

  // Auto-slide and touch navigation code...
  // Navigation buttons
  const handlePrev = () => {
    if (cards.length > 0) {
      setStartIndex((prev) => (prev - 1 + cards.length) % cards.length);
    }
  };

  const handleNext = () => {
    if (cards.length > 0) {
      setStartIndex((prev) => (prev + 1) % cards.length);
    }
  };

  // Get visible cards
  const displayedCards = Array.from({ length: perPage }, (_, i) => {
    if (cards.length === 0) return null;
    const idx = (startIndex + i) % cards.length;
    return cards[idx];
  }).filter(Boolean);

  if (loading) {
    return (
      <div className="bg-white py-10">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-6">Feature Ads</h2>
          <div className="flex justify-center items-center h-64">
            <p>Loading featured ads...</p>
          </div>
        </div>
      </div>
    );
  }

  if (cards.length === 0) {
    return (
      <div className="bg-white py-10">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-6">Feature Ads</h2>
          <div className="flex justify-center items-center h-64">
            <p>No featured ads available</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white py-10">
      <div className="max-w-6xl mx-auto">
        {/* Heading */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800">Feature Ads</h2>
        </div>

        {/* Cards Grid with Swipe */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {displayedCards.map((card) => (
            <SimpleCard
              key={card.id}
              id={card.id}
              image={card.image}
              title={card.title}
              description={card.description}
              price={card.price}
              route={card.route}
            />
          ))}
        </div>

        {/* Navigation Buttons */}
        <div className="flex space-x-3 mt-10 justify-center">
          <button
            onClick={handlePrev}
            className="p-2 rounded-full text-black bg-gray-100 hover:bg-gray-200 shadow"
            aria-label="Previous"
          >
            <MdChevronLeft size={28} />
          </button>
          <button
            onClick={handleNext}
            className="p-2 rounded-full text-black bg-gray-100 hover:bg-gray-200 shadow"
            aria-label="Next"
          >
            <MdChevronRight size={28} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PopularAds;