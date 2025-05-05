import Page from "@/components/GenerateCard";
import MCMain from "@/components/MC/MCMain";

export default function MotorCycle() {
  return (
    <div className="bg-white">
      <MCMain />
      <h1 className="font-bold text-3xl text-gray-800">Find Bikes</h1>
      <Page />
    </div>
  );
}