import RecentlyVisitedSlider from "@/components/general/RecentlyVisitedSlider";
import Page from "@/components/GenerateCard";
import Purchase from "@/components/property/Purchase";
export default function PurchasePage() {
    return (
        <div className="bg-white w-full">
            {/* <PropertyMain /> */}
            <Purchase />
            <RecentlyVisitedSlider />
            <h1 className="font-bold text-3xl text-gray-800">We think you might like these</h1>
            <Page columns={3} route="/routes/property/property-details"/>
        </div>
    );
}
