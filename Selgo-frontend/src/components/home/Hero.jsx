"use client";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import ButtonWithIcon from "../root/ButtonWithIcon";
import { LiaMapMarkedAltSolid } from "react-icons/lia";
import { useRouter } from "next/navigation";
// Import the new React icons
import { PiCouchLight } from "react-icons/pi";
import { IoHomeOutline } from "react-icons/io5";
import { CiFileOn } from "react-icons/ci";
import { PiSailboatLight } from "react-icons/pi";
import { PiSnowflakeLight } from "react-icons/pi";
import { PiMotorcycleLight } from "react-icons/pi";
import { GoBriefcase } from "react-icons/go";
import { BsHouses } from "react-icons/bs";
import { LiaIndustrySolid } from "react-icons/lia";
import { IoCarOutline } from "react-icons/io5";
import { CiHome } from "react-icons/ci";
import { PiAirplaneTaxiingLight } from "react-icons/pi";


// Updated card data with the new icons
const cardData = [
  {
    items: [
      { tag: "The square", IconComponent: PiCouchLight, route: "/routes/the-square", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Property", IconComponent: CiHome, route: "/routes/property", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Travel", IconComponent: PiAirplaneTaxiingLight, route: "/routes/travel", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Boat", IconComponent: PiSailboatLight, route: "/routes/boat", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "NU Electronics", IconComponent: PiSnowflakeLight, route: "/routes/nu-electronics", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "MC", IconComponent: PiMotorcycleLight, route: "/routes/motor-cycle", iconProps: { className: "text-teal-700", size: 24 } },
    ]
  },
  {
    items: [
      { tag: "Jobs", IconComponent: GoBriefcase, route: "/routes/jobs", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Homes for Rent", IconComponent: BsHouses, route: "/routes/home-for-rent", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Car and industry", IconComponent: LiaIndustrySolid, route: "/routes/car-and-industry", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "Online Car", IconComponent: IoCarOutline, route: "/routes/online-car", iconProps: { className: "text-teal-700", size: 24 } },
      { tag: "My Tender", IconComponent: CiFileOn, route: "/routes/my-tender", iconProps: { className: "text-teal-700", size: 24 } },
    ]
  }
];

const rowStyles = {
  0: {
    gridCols: "grid-cols-2 md:grid-cols-3 lg:grid-cols-6",
    gap: "gap-6",
    marginBottom: ""
  },
  1: {
    gridCols: "grid-cols-2 md:grid-cols-3 lg:grid-cols-5",
    gap: "gap-6",
    centered: true
  }
};

export default function Hero() {
  const router = useRouter();

  const navigateToMap = () => {
    router.push("/routes/map");
  };

  return (
    <div className="relative pt-5">
      <div className="flex justify-center items-center gap-4 w-full mb-4">
        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
        <ButtonWithIcon
          icon={LiaMapMarkedAltSolid}
          label="Map"
          onClick={navigateToMap}
          iconProps={{ className: "text-teal-700", size: 24 }} // Also update the map button icon for consistency
        />
      </div>

      <div className="text-center max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-900 leading-tight">
          <span className="text-teal-600 text-3xl"> Simplify {" "}</span>
          Your Shopping with Us!
        </h1>
      </div>

      <div>
        <div>
          <GenericCardCollection
            rows={cardData}
            rowStyles={rowStyles}
            imageBasePath="/assets/header/dropdown/"
          />
        </div>
      </div>
    </div>
  );
}