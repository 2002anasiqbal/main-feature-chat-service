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
    <>
      {/* Hide scrollbars on all screens */}
      <style jsx>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none; /* IE and Edge */
          scrollbar-width: none;    /* Firefox */
        }
      `}</style>

      <div className=" flex flex-col">
        {/* Header Section */}
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
          {/* Sidebar */}
          <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
            <Sidebar />
          </div>

          {/* Main Page Content */}
          <div className="flex-1 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
            <Page columns={3} />
          </div>
        </div>
      </div>
    </>
  );
}