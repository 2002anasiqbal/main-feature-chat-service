import CarMain from "@/components/cars/CarMain";
import Page from "@/components/GenerateCard";
import RecommendedCars from "@/components/cars/RecommendedCars";

export default function Car() {
  return (
    <div className="bg-white">
      <CarMain />
      <div className="container mx-auto px-4">
        <h1 className="font-bold text-3xl text-gray-800 py-10">Find the cars that suit you</h1>

        <Page route="/routes/cars" />

        <RecommendedCars />
      </div>
    </div>
  );
}
