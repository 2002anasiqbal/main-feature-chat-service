"use client";

import ButtonCard from "@/components/general/ButtonCard";
import GenericCardCollection from "@/components/GenericCardCollection";
import SearchBar from "@/components/root/SearchBar";
import { useRouter } from "next/navigation";

const cardData = [
  {
    items: [
      { tag: "Craft", icon: "3.svg", route: "#" },
      { tag: "Car workshop", icon: "4.svg", route: "#" },
      { tag: "Terrace/paving", icon: "5.svg", route: "#" },
      { tag: "Cleaning", icon: "6.svg", route: "#" },
    ],
  },
  {
    items: [
      { tag: "Economy", icon: "7.svg", route: "#" },
      { tag: "Transport", icon: "8.svg", route: "#" },
      { tag: "Housing", icon: "9.svg", route: "#" },
      { tag: "Other", icon: "10.svg", route: "#" },
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

export default function CategoryPage() {
  const router = useRouter();

  return (
    <div className="bg-white py-16 min-h-screen">
      <div className="max-w-5xl mx-auto px-6">
        {/* Icon Grid */}
        <GenericCardCollection
          rows={cardData}
          rowStyles={rowStyles}
          imageBasePath="/assets/my-tender/"
          size="h-30 w-30"
        />

        {/* Label */}
        <p className="text-center text-sm text-gray-700 mt-8">
          Select category to post your job – completely free
        </p>

        {/* Search Box with Arrow */}
        <div className="max-w-xl mx-auto mt-4">
          <div className="flex items-center justify-between border rounded-md shadow px-4 py-2">
            <input
              type="text"
              placeholder="What do you need help with?"
              className="w-full focus:outline-none text-sm text-gray-600"
            />
            <img
              src="/assets/my-tender/1.svg"
              alt="arrow"
              className="w-7 h-7 ml-2"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
