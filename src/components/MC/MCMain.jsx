"use client";
import Image from "next/image";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import { useRouter } from "next/navigation";

// Example card data (two rows, each with three items)
const cardData = [
  {
    items: [
      { tag: "Thresher 6000", icon: "1.svg", route: "/routes/motor-cycle/category" },
      { tag: "Suzuki 6000", icon: "2.svg", route: "/routes/motor-cycle/category" },
      { tag: "Motorcycles 6000", icon: "3.svg", route: "/routes/motor-cycle/category" },
    ],
  },
  {
    items: [
      { tag: "Auto bikes 6000", icon: "4.svg", route: "/routes/motor-cycle/category" },
      { tag: "Tractor 6000", icon: "5.svg", route: "/routes/motor-cycle/category" },
      { tag: "Bikes 6000", icon: "6.svg", route: "/routes/motor-cycle/category" },
    ],
  },
];

const rowStyles = {
  0: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-3",
    gap: "gap-6",
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-3",
    gap: "gap-6",
    centered: true,
  },
};

export default function MCMain() {
  const router = useRouter();

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      {/* Hero Image with increased height */}
      <div className="relative w-full h-[500px] mb-6">
        <Image
          src="/assets/MC/motorcycle.svg"
          alt="Motorcycle Hero"
          fill
          className="object-cover object-center"
          priority
        />
      </div>

      <h1 className="text-5xl text-gray-900 font-bold pb-10">
        Motorcycles
      </h1>

      {/* Search Bar */}
      <div className="justify-center items-center gap-4 w-full mb-6">
        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
      </div>

      {/* Cards Section */}
      <GenericCardCollection
        rows={cardData}
        rowStyles={rowStyles}
        imageBasePath="/assets/MC/"
        size="h-32 w-32"
      />

      {/* Centered Button */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}