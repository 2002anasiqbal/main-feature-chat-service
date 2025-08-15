"use client";
import { useState } from "react";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";

// Hardcoded boat category data - this matches what should be in your database
const cardData = [
  {
    items: [
      { tag: "Buy Boats", icon: "1.svg", route: "/routes/boat/category/1"},
      { tag: "Buy Boats Abroad", icon: "2.svg", route: "/routes/boat/category/2"},
      { tag: "Boats in Norway", icon: "3.svg", route: "/routes/boat/category/3"},
      { tag: "Vans abroad", icon: "4.svg", route: "/routes/boat/category/4"},
    ],
  },
  {
    items: [
      { tag: "Boats parts", icon: "5.svg", route: "/routes/boat/category/5"},
      { tag: "Boats", icon: "6.svg", route: "/routes/boat/category/6"},
      { tag: "Boats for rent", icon: "7.svg", route: "/routes/boat/category/7"},
      { tag: "Boats for sale", icon: "8.svg", route: "/routes/boat/category/8"},
    ],
  },
];

const rowStyles = {
  0: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", // First row: 4 cards
    gap: "gap-6", // Adjust spacing
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", // Second row: 4 cards
    gap: "gap-6",
    centered: true,
  },
};

export default function BoatMain() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      router.push(`/routes/boat/search?q=${encodeURIComponent(searchTerm)}`);
    }
  };

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      <h1 className="text-5xl text-gray-900 font-bold pb-10">Boat</h1>
      {/* Search Bar Centered */}
      <div className="justify-center items-center gap-4 w-full mb-6 ">
        <form onSubmit={handleSearchSubmit}>
          <SearchBar 
            placeholder="Search" 
            value={searchTerm}
            onChange={handleSearch}
          />
        </form>
      </div>
      {/* Cards Section - Using hardcoded data */}
      <GenericCardCollection rows={cardData} rowStyles={rowStyles} imageBasePath="/assets/boat/" size="h-32 w-32" />
      {/* Centered Button */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}