import Page from "@/components/GenerateCard";
import PopularCitiesGrid from "@/components/property/PopularCitiesGrid";
import RentingTips from "@/components/property/RentingTips";
export default function RentPage() {
    return (
        <div className="bg-white">
        
            <PopularCitiesGrid/>
            <RentingTips />
            <h1 className="font-bold text-3xl text-gray-800">Popular Cities to Rent In</h1>
            <Page columns={3} route="/routes/property/property-details" />
        </div>
    );
}
