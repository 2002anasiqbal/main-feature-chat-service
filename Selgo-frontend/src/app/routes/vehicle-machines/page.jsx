// import OnlineCarMain from "@/components/vehicleAndMachines/OnlineCarMain";
// import CarValuation from "@/components/carCarvan/CarValuation";
// import UsefulTools from "@/components/carCarvan/UsefulTools";
import Page from "@/components/GenerateCard";
import VehicleAndMachineMain from "@/components/vehicleAndMachines/VehicleMachine";

export default function OnlineCar() {
  return (
    <div className="bg-white">
      <VehicleAndMachineMain />
      {/* <VehicleMachine/> */}
      {/* <CarValuation /> */}
      <div className="">
        {/* <PopularAds /> */}
        <h1 className="font-bold text-3xl text-gray-800 px-15">Find the Cars that suits you</h1>
        <Page />
        {/* <UsefulTools/> */}
        {/* <h1 className="font-bold text-3xl text-gray-800 px-15">Recommended</h1>
        <Page /> */}
      </div>
    </div>
  );
}