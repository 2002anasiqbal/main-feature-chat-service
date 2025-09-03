import SquareMain from "@/components/square/SquareMain";
import Page from "@/components/GenerateCard";
import RecommendedItems from "@/components/square/RecommendedItems";

export default function Square() {
  return (
    <div className="bg-white">
      <SquareMain />
      <div className="container mx-auto px-4">
        <h1 className="font-bold text-3xl text-gray-800 py-10">Find the items that suit you</h1>

        <Page route="/routes/square" />

        <RecommendedItems />
      </div>
    </div>
  );
}
