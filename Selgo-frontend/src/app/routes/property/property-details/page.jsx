import LocationMap from "@/components/general/LocationMap";
import PropertyDetails from "@/components/property/PropertyDetails";
import PropertySlider from "@/components/property/PropertySlider";

export default function PropertyDetailsPage() {
    return (
      <div className="bg-white">
        <PropertySlider/>
        <PropertyDetails/>
        <LocationMap />
      </div>
    );
  }