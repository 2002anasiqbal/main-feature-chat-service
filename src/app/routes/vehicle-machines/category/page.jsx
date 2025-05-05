"use client";
import Sidebar from "@/components/general/Sidebar";
import Page from "@/components/GenerateCard";
import SearchBar from "@/components/root/SearchBar";
import ButtonWithIcon from "@/components/root/ButtonWithIcon";
import { LiaMapMarkedAltSolid } from "react-icons/lia";
import { useRouter } from "next/navigation";

export default function TwoColumnLayoutPage() {
  const router = useRouter();

  const navigateToMap = () => {
    router.push("/routes/map");
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header Section with Search Bar & Map Button */}
      <div className="w-full bg-white py-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="w-full md:w-auto flex-1">
          <SearchBar placeholder="Search" onChange={() => console.log("change")} />
        </div>
        <div className="w-full md:w-auto md:ml-4">
          <ButtonWithIcon
            icon={LiaMapMarkedAltSolid}
            label="Map"
            onClick={navigateToMap}
            className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md w-full md:w-auto"
          />
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 relative">
        {/* Sidebar - Now properly positioned below header */}
        <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto">
          <Sidebar />
        </div>

        {/* Main Page Content */}
        <div className="flex-1 bg-white p-6 max-h-[calc(100vh-4rem)] overflow-y-auto">
          <Page columns={4} />
          {/* <Page columns={4} /> */}
        </div>
      </div>
    </div>
  );
}