"use client";
import { useState } from "react";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";

const cardData = [
  {
    items: [
      { tag: "Antiques and Art", icon: "1.svg", route: "/routes/square/category/1"},
      { tag: "Animals and Equipment", icon: "2.svg", route: "/routes/square/category/2"},
      { tag: "Electronics and White Goods", icon: "3.svg", route: "/routes/square/category/3"},
      { tag: "For Parents and Children", icon: "4.svg", route: "/routes/square/category/4"},
    ],
  },
  {
    items: [
      { tag: "Holidays and Hobbies", icon: "5.svg", route: "/routes/square/category/5"},
      { tag: "Garden, Renovation and House", icon: "6.svg", route: "/routes/square/category/6"},
      { tag: "Clothes, Cosmetics and Accessories", icon: "7.svg", route: "/routes/square/category/7"},
      { tag: "Furniture and Interior", icon: "8.svg", route: "/routes/square/category/8"},
    ],
  },
];

const rowStyles = {
  0: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4",
    gap: "gap-6",
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4",
    gap: "gap-6",
    centered: true,
  },
};

export default function SquareMain() {
  const router = useRouter();
  const [searchTerm, setSearchTerm] = useState("");

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      router.push(`/routes/square/search?q=${encodeURIComponent(searchTerm)}`);
    }
  };

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      <h1 className="text-5xl text-gray-900 font-bold pb-10">Square</h1>
      <div className="justify-center items-center gap-4 w-full mb-6 ">
        <form onSubmit={handleSearchSubmit}>
          <SearchBar
            placeholder="Search"
            value={searchTerm}
            onChange={handleSearch}
          />
        </form>
      </div>
      <GenericCardCollection rows={cardData} rowStyles={rowStyles} imageBasePath="/assets/square/" size="h-32 w-32" />
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}
