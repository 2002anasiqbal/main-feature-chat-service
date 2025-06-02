"use client";
import React, { useEffect, useRef, useState } from "react";
import SimpleCard from "../root/Card";
import { MdChevronLeft, MdChevronRight } from "react-icons/md";

const mockCards = [
  { id: 1, image: "/assets/swiper/1.jpg", title: "Gaming Laptop", description: "High‑performance laptop for gaming and design.", price: "$1299" },
  { id: 2, image: "/assets/swiper/2.jpg", title: "Wireless Headphones", description: "Noise‑cancelling over‑ear wireless headphones.", price: "$199" },
  { id: 3, image: "/assets/swiper/3.jpg", title: "Smartwatch", description: "Track fitness, receive notifications and more.", price: "$149" },
  { id: 4, image: "/assets/swiper/4.jpg", title: "Camera Gear", description: "DSLR with dual‑lens package.", price: "$899" },
  { id: 5, image: "/assets/swiper/5.jpg", title: "Ergonomic Chair", description: "Perfect comfort for long work sessions.", price: "$350" }
];

const PopularAds = () => {
  const [perPage, setPerPage] = useState(3);
  const [startIndex, setStartIndex] = useState(0);
  const touchStartX = useRef(null);
  const touchEndX = useRef(null);

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

  // Auto-slide every 5 seconds (without flicker)
  useEffect(() => {
    const id = setInterval(() => {
      requestAnimationFrame(() => {
        setStartIndex((prev) => (prev + 1) % mockCards.length);
      });
    }, 5000);
    return () => clearInterval(id);
  }, []);

  // Navigation buttons
  const handlePrev = () => {
    requestAnimationFrame(() => {
      setStartIndex((prev) => (prev - 1 + mockCards.length) % mockCards.length);
    });
  };

  const handleNext = () => {
    requestAnimationFrame(() => {
      setStartIndex((prev) => (prev + 1) % mockCards.length);
    });
  };

  // Touch gestures for swipe
  const handleTouchStart = (e) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e) => {
    touchEndX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = () => {
    if (!touchStartX.current || !touchEndX.current) return;
    const delta = touchStartX.current - touchEndX.current;
    if (Math.abs(delta) > window.innerWidth * 0.1) {
      delta > 0 ? handleNext() : handlePrev();
    }
    touchStartX.current = null;
    touchEndX.current = null;
  };

  // Get visible cards
  const displayedCards = Array.from({ length: perPage }, (_, i) => {
    const idx = (startIndex + i) % mockCards.length;
    return mockCards[idx];
  });

  return (
    <div className="bg-white py-10">
      <div className="max-w-6xl mx-auto">
        {/* Heading */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-800">Feature Ads</h2>
        </div>

        {/* Cards Grid with Swipe */}
        <div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
        >
          {displayedCards.map((card) => (
            <SimpleCard
              key={card.id}
              image={card.image}
              title={card.title}
              description={card.description}
              price={card.price}
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