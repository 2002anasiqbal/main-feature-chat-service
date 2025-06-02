import CarCaravanMain from "@/components/carCarvan/CarCaravanMain";
import CarValuation from "@/components/carCarvan/CarValuation";
import UsefulTools from "@/components/carCarvan/UsefulTools";
import Page from "@/components/GenerateCard";

export default function CarAndIndustry() {
  return (
    <div className="bg-white">
      <CarCaravanMain/>
      <CarValuation />
      <div className="">
        {/* <PopularAds /> */}
        <h1 className="font-bold text-3xl text-gray-800">Find the Cars that suits you</h1>
        <Page />
        <UsefulTools/>
        <h1 className="font-bold text-3xl text-gray-800">Recommended</h1>
        <Page />
      </div>
    </div>
  );
}