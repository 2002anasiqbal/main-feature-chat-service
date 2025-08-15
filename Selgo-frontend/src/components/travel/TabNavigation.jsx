"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { CiPlane } from "react-icons/ci";
import { RiHotelLine } from "react-icons/ri";
import { LuCarTaxiFront } from "react-icons/lu";
import { TbBuildingAirport, TbHomeSearch } from "react-icons/tb";

const tabs = [
  { name: "Fly", icon: <CiPlane />, page: "/routes/travel/fly" },
  { name: "Hotel", icon: <RiHotelLine />, page: "/routes/travel/hotel" },
  { name: "Rental Car", icon: <LuCarTaxiFront />, page: "/routes/travel/rental-car" },
  { name: "Fly + Hotel", icon: <TbBuildingAirport />, page: "/routes/travel/fly-hotel" },
  { name: "Holiday Homes", icon: <TbHomeSearch />, page: "/routes/travel/holiday-homes" },
];

export default function TabNavigation() {
  const pathname = usePathname();

  return (
    <div className="w-full border-b border-gray-200 pb-2 px-4">
      {/* Grid Layout for Large & Medium Screens */}
      <div className="hidden sm:grid sm:grid-cols-3 md:flex md:justify-center space-x-6">
        {tabs.map((tab) => (
          <Link key={tab.name} href={tab.page} prefetch>
            <div
              className={`flex flex-col items-center p-2 text-gray-500 transition-all cursor-pointer
                ${pathname === tab.page ? "text-teal-700 border-b-2 border-teal-700" : "hover:text-gray-800"}`}
            >
              <div className="text-2xl">{tab.icon}</div>
              <span className="text-sm mt-1">{tab.name}</span>
            </div>
          </Link>
        ))}
      </div>

      {/* Two Rows for Small Screens */}
      <div className="sm:hidden flex flex-col items-center gap-4 mt-4">
        {/* First Row - 3 Icons */}
        <div className="grid grid-cols-3 gap-4">
          {tabs.slice(0, 3).map((tab) => (
            <Link key={tab.name} href={tab.page} prefetch>
              <div
                className={`flex flex-col items-center p-2 text-gray-500 transition-all cursor-pointer
                  ${pathname === tab.page ? "text-teal-700 border-b-2 border-teal-700" : "hover:text-gray-800"}`}
              >
                <div className="text-2xl">{tab.icon}</div>
                <span className="text-sm mt-1">{tab.name}</span>
              </div>
            </Link>
          ))}
        </div>

        {/* Second Row - 2 Icons Centered */}
        <div className="grid grid-cols-2 gap-4">
          {tabs.slice(3).map((tab) => (
            <Link key={tab.name} href={tab.page} prefetch>
              <div
                className={`flex flex-col items-center p-2 text-gray-500 transition-all cursor-pointer
                  ${pathname === tab.page ? "text-teal-700 border-b-2 border-teal-700" : "hover:text-gray-800"}`}
              >
                <div className="text-2xl">{tab.icon}</div>
                <span className="text-sm mt-1">{tab.name}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}