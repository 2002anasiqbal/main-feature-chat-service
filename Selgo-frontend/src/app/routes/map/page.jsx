"use client";
import { useState } from "react";
import SearchBar from "@/components/root/SearchBar";

const cardData = [
  {
    items: [
      { tag: "The square", icon: "furniture.svg", route: "/routes/the-square" },
      { tag: "Property", icon: "home-09.svg", route: "/routes/property" },
      { tag: "Travel", icon: "airplane-take-off-01.svg", route: "/routes/travel" },
      { tag: "Boat", icon: "boat.svg", route: "/routes/boat" },
      { tag: "Electronics", icon: "fridge.svg", route: "/routes/nu-electronics" },
      { tag: "MC", icon: "motorbike-02.svg", route: "/routes/mc" },
      { tag: "Jobs", icon: "job-search.svg", route: "/routes/jobs" },
      { tag: "Homes for Rent", icon: "home-09-1.svg", route: "/routes/home-for-rent" },
      { tag: "Car and industry", icon: "bot.svg", route: "/routes/car-and-industry" },
      { tag: "Online Car", icon: "bot.svg", route: "/routes/online-car" },
      { tag: "My Tender", icon: "agreement-02.svg", route: "/routes/my-tender" },
    ],
  },
];

export default function Map() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCard, setSelectedCard] = useState(null);

  // Handle search input
  const handleSearch = (query) => {
    setSearchQuery(query);
  };

  // Handle card click & highlight selection
  const handleCardClick = (tag) => {
    console.log(`${tag} card is clicked`);
    setSelectedCard(tag);
  };

  return (
    <div className="relative w-full min-h-screen bg-white flex pt-5">
      {/* Scrollable Sidebar with Cards (Left Side) */}
      <div className="w-24 sm:w-32 h-screen overflow-y-auto bg-white">
        <div className="flex flex-col space-y-2">
          {cardData[0].items.map((card, index) => (
            <div
              key={index}
              onClick={() => handleCardClick(card.tag)}
              className={`w-20 h-20 md:w-28 md:h-28 flex flex-col items-center justify-center border-2 rounded-lg cursor-pointer transition
                ${
                  selectedCard === card.tag
                    ? "border-teal-600 bg-teal-100 shadow-md"
                    : "border-gray-300 bg-white hover:bg-gray-200"
                }`}
            >
              <img src={`/assets/header/dropdown/${card.icon}`} alt={card.tag} className="w-6 h-6 md:w-8 md:h-8" />
              <p className="text-gray-700 text-[10px] md:text-xs font-medium mt-1">{card.tag}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Main Content (Search Bar Centered) */}
      <div className="flex-1 flex flex-col justify-start items-center ml-5">
        <div className="w-full">
          <SearchBar
            placeholder="Search location..."
            onChange={(e) => setSearchQuery(e.target.value)}
            onSubmit={() => handleSearch(searchQuery)}
          />
        </div>
      </div>
    </div>
  );
}