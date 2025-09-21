import BidOnCars from "@/components/online-car/BidOnCars";
import CarCollection from "@/components/online-car/CarCollection";
import ContactSection from "@/components/online-car/ContactSection";

export default function BidOnCarPage() {
    return (
        <div className="bg-white">
            <BidOnCars />
            <CarCollection/>
            <ContactSection />
        </div>
    );
}