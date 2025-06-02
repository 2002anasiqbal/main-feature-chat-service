import BoatMain from "@/components/boat/BoatMain";
import Page from "@/components/GenerateCard";
import PopularAds from "@/components/home/PopularAds";

export default function Boat() {
  return (
    <div className="bg-white">
      <BoatMain />
      <div className="">
        {/* <PopularAds /> */}
        <h1 className="font-bold text-3xl text-gray-800 py-10">Find the boats that suits you</h1>
        <Page />
      </div>
    </div>
  );
}