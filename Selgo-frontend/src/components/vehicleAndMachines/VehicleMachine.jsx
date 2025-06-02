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
      { tag: "Truck 6000", icon: "1.svg", route: "/routes/vehicle-machines/category" },
      { tag: "Truck Abroad 6000", icon: "2.svg", route: "/routes/vehicle-machines/category" },
      { tag: "Buses 6000", icon: "3.svg", route: "/routes/vehicle-machines/category" },
      { tag: "Mini Buses 6000", icon: "3.svg", route: "/routes/vehicle-machines/category" },
    ],
  },
  {
    items: [
      { tag: "Tools 6000", icon: "4.svg", route: "/routes/vehicle-machines/category" },
      { tag: "Threshor 6000", icon: "5.svg", route: "/routes/vehicle-machines/category" },
      { tag: "Tractor 6000", icon: "6.svg", route: "/routes/vehicle-machines/category" },
    ],
  },
];

// const cardData = [
//   {
//     items: [
//       { tag: "Truck 6000", icon: "1.svg", route: "/routes/vehicle-machines/truck" },
//       { tag: "Truck Abroad 6000", icon: "2.svg", route: "/routes/vehicle-machines/truck-abroad" },
//       { tag: "Buses 6000", icon: "3.svg", route: "/routes/vehicle-machines/buses" },
//       { tag: "Mini Buses 6000", icon: "3.svg", route: "/routes/vehicle-machines/mini-buses" },
//     ],
//   },
//   {
//     items: [
//       { tag: "Tools 6000", icon: "4.svg", route: "/routes/vehicle-machines/tools" },
//       { tag: "Threshor 6000", icon: "5.svg", route: "/routes/vehicle-machines/threshor" },
//       { tag: "Tractor 6000", icon: "6.svg", route: "/routes/vehicle-machines/tractor" },
//     ],
//   },
// ];


const rowStyles = {
  0: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-4",
    gap: "gap-6",
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-3",
    gap: "gap-6",
    centered: true,
  },
};

export default function VehicleAndMachineMain() {
  const router = useRouter();

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen px-20">
      {/* Hero Image with increased height */}
      <div className="relative w-full h-[500px] mb-6">
        <Image
          src="/assets/vehicleMachines/vehicles.svg"
          alt="Car Hero"
          fill
          className="object-cover object-center"
          priority
        />
      </div>

      <h1 className="text-5xl text-gray-900 font-bold pb-10 px-6 lg:px-28">
        Vehicle and Machinary
      </h1>

      {/* Search Bar */}
      <div className="justify-center items-center gap-4 w-full max-w-5xl mx-auto mb-6 px-6">
        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
      </div>

      {/* Cards Section */}
      <GenericCardCollection
        rows={cardData}
        rowStyles={rowStyles}
        imageBasePath="/assets/vehicleMachines/"
        size="h-32 w-32"
      />

      {/* Centered Button */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}