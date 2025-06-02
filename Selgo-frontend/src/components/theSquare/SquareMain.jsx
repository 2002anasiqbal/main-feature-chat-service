"use client";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";


const cardData = [
  {
    items: [
      { tag: "Antiques and Art", icon: "art.svg", route: "/routes/the-square/category" },
      { tag: "Mobile Phones", icon: "mobile-protect.svg", route: "/routes/the-square/category" },
      { tag: "Garden, Renovation and House", icon: "garden.svg", route: "/routes/the-square/category" },
      { tag: "Parents and Childrens", icon: "child.svg", route: "/routes/the-square/category" },
      { tag: "Commercial Activities", icon: "activites.svg", route: "/routes/the-square/category" },
      { tag: "Electronics", icon: "electronics.svg", route: "/routes/the-square/category" },
    ],
  },
  {
    items: [
      { tag: "Clothing, Cosmetics & Accessories", icon: "clothing.svg", route: "/routes/the-square/category" },
      { tag: "Furniture & Entertainment", icon: "furniture.svg", route: "/routes/the-square/category" },
      { tag: "Leisure, Hobby & Entertainment", icon: "leasure.svg", route: "/routes/the-square/category" },
      { tag: "Equipment for Cars, Boats & Motorbikes", icon: "equipment.svg", route: "/routes/the-square/category" },
      { tag: "Animals & Equipment", icon: "animals.svg", route: "/routes/the-square/category" },
      { tag: "Sports & Outdoor Life", icon: "sports.svg", route: "/routes/the-square/category" },
    ],
  },
];

// const cardData = [
//   {
//     items: [
//       { tag: "Antiques and Art", icon: "art.svg", route: "/routes/antiques" },
//       { tag: "Mobile Phones", icon: "mobile-protect.svg", route: "/routes/mobile-phones" },
//       { tag: "Garden, Renovation and House", icon: "garden.svg", route: "/routes/garden-renovation" },
//       { tag: "Parents and Childrens", icon: "child.svg", route: "/routes/parents-childrens" },
//       { tag: "Commercial Activities", icon: "activites.svg", route: "/routes/commercial" },
//       { tag: "Electronics", icon: "electronics.svg", route: "/routes/electronics" },
//       { tag: "Clothing, Cosmetics & Accessories", icon: "clothing.svg", route: "/routes/clothing-cosmetics" },
//       { tag: "Furniture & Entertainment", icon: "furniture.svg", route: "/routes/furniture-entertainment" },
//     ],
//   },
//   {
//     items: [
//       { tag: "Leisure, Hobby & Entertainment", icon: "leasure.svg", route: "/routes/leisure-hobby" },
//       { tag: "Equipment for Cars, Boats & Motorbikes", icon: "equipment.svg", route: "/routes/auto-equipment" },
//       { tag: "Animals & Equipment", icon: "animals.svg", route: "/routes/animals" },
//       { tag: "Sports & Outdoor Life", icon: "sports.svg", route: "/routes/outdoor-life" },
//     ],
//   },
// ];

const rowStyles = {
  0: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-8", // 🔹 First row: 8 cards
    gap: "gap-8", // Increased gap for better spacing
    marginBottom: "mb-8",
  },
  1: {
    gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", // 🔹 Second row: 4 cards
    gap: "gap-8",
    centered: true,
  },
};



export default function SquareMain() {
  const router = useRouter();

  return (
    <div className="pt-24 sm:pt-16 w-full bg-white">
      <h1 className="text-5xl text-gray-900 font-bold">The Square</h1>
      {/* Search Bar Centered */}
      <div className="justify-center items-center gap-4 w-full mb-6">
        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
      </div>
      {/* Cards Section */}
      <GenericCardCollection rows={cardData} rowStyles={rowStyles} imageBasePath="/assets/theSquare/" size="h-32 w-32" />

    </div>
  );
}