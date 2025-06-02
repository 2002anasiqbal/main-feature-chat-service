"use client";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";

const cardData = [
  {
    items: [
      { tag: "Buy Cars", icon: "1.svg", route: "/routes/car-and-industry/category" },
      { tag: "Buy Caravans", icon: "2.svg", route: "/routes/car-and-industry/category" },
      { tag: "Cars in Norway", icon: "3.svg", route: "/routes/car-and-industry/category" },
      { tag: "Caravans Abroad", icon: "4.svg", route: "/routes/car-and-industry/category" },
    ],
  },
  {
    items: [
      { tag: "Car Parts", icon: "5.svg", route: "/routes/car-and-industry/category" },
      { tag: "Caravans", icon: "6.svg", route: "/routes/car-and-industry/category" },
      { tag: "Caravans for Rent", icon: "7.svg", route: "/routes/car-and-industry/category" },
      { tag: "Cars for Sale", icon: "8.svg", route: "/routes/car-and-industry/category" },
    ],
  },
];

const rowStyles = {
  0: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", // First row: 4 cards
    gap: "gap-6",
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", // Second row: 4 cards
    gap: "gap-6",
    centered: true,
  },
};

export default function CarCaravanMain() {
  const router = useRouter();

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      <h1 className="text-5xl text-gray-900 font-bold pb-10">Car & Caravan</h1>

      {/* Search Bar Centered */}
      <div className="justify-center items-center gap-4 w-full mb-6">
        <SearchBar placeholder="Search Cars & Caravans" onChange={() => console.log("change")} />
      </div>

      {/* Cards Section */}
      <GenericCardCollection rows={cardData} rowStyles={rowStyles} imageBasePath="/assets/carcarvan/" size="h-32 w-32" />

      {/* Centered Button */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}
