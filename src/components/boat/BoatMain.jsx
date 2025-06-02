"use client";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";

const cardData = [
  {
    items: [
      { tag: "Buy Boats", icon: "1.svg", route: "/routes/boat/category"},
      { tag: "Buy Boats", icon: "2.svg", route: "/routes/boat/category"},
      { tag: "Boats in Norway", icon: "3.svg", route: "/routes/boat/category"},
      { tag: "Vans abroad", icon: "4.svg", route: "/routes/boat/category"},
    ],
  },
  {
    items: [
      { tag: "Boats parts", icon: "5.svg", route: "/routes/boat/category"},
      { tag: "Boats", icon: "6.svg", route: "/routes/boat/category"},
      { tag: "Boats for rent", icon: "7.svg", route: "/routes/boat/category"},
      { tag: "Boats for sale", icon: "8.svg", route: "/routes/boat/category"},
    ],
  },
];

// ================ for backend integration mock ================

// const cardData = [
//   {
//     items: [
//       { tag: "Buy Boats", icon: "1.svg", route: "/routes/boat/buy-boats" },
//       { tag: "Buy Boats", icon: "2.svg", route: "/routes/boat/buy-boats" },
//       { tag: "Boats in Norway", icon: "3.svg", route: "/routes/boat/boats-in-norway" },
//       { tag: "Vans abroad", icon: "4.svg", route: "/routes/boat/vans-abroad" },
//     ],
//   },
//   {
//     items: [
//       { tag: "Boats parts", icon: "5.svg", route: "/routes/boat/boats-parts" },
//       { tag: "Boats", icon: "6.svg", route: "/routes/boat/boats" },
//       { tag: "Boats for rent", icon: "7.svg", route: "/routes/boat/boats-for-rent" },
//       { tag: "Boats for sale", icon: "8.svg", route: "/routes/boat/boats-for-sale" },
//     ],
//   },
// ];

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

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      <h1 className="text-5xl text-gray-900 font-bold pb-10">Boat</h1>
      {/* Search Bar Centered */}
      <div className="justify-center items-center gap-4 w-full mb-6 ">
        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
      </div>
      {/* Cards Section */}
      <GenericCardCollection rows={cardData} rowStyles={rowStyles} imageBasePath="/assets/boat/" size="h-32 w-32" />
      {/* Centered Button */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}