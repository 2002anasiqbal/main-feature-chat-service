"use client";

import GenericBanner from "@/components/general/GenericBanner";
import FindFlight from "@/components/travel/FindFlight";
import FlightTicketCollection from "@/components/travel/FlightTicketCollection";
import InfoSection from "@/components/travel/InfoSection";
import TravelDestinationsCollection from "@/components/travel/ravelDestinationsCollection";

export default function FlyHotel() {
  return (
    <div className="p-6">
      <h2 className="flex justify-center content-center my-10 text-lg font-normal text-gray-900">Find Cheap Prices at Selgo</h2>
      <FindFlight searchRoute="/routes/travel/fly-hotel/search" />
      <GenericBanner />
      <InfoSection />
      <h1 className="mt-15 ml-32 text-3xl font-bold text-gray-800">Useful Articles</h1>
      <FlightTicketCollection />
      <FlightTicketCollection />
      <TravelDestinationsCollection />
    </div>
  );
}
