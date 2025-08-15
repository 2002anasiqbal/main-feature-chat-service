"use client";

import GenericBanner from "@/components/general/GenericBanner";
import FindFlight from "@/components/travel/FindFlight";
import FlightTicketCollection from "@/components/travel/FlightTicketCollection";
import InfoSection from "@/components/travel/InfoSection";
import TravelDestinationsCollection from "@/components/travel/ravelDestinationsCollection";

export default function Fly() {
  return (
    <div className="py-6 w-full">
      <h2 className="flex text-2xl my-10 font-semibold text-gray-900">
        Find Cheap Prices at Selgo
      </h2>
      <FindFlight searchRoute="/routes/travel/fly/search" /> {/* Passed correctly */}
      <GenericBanner />
      <InfoSection />
      <h1 className="mt-16 ml-32 text-3xl font-bold text-gray-800">
        Useful Articles
      </h1>
      <FlightTicketCollection />
      <FlightTicketCollection />
      <TravelDestinationsCollection />
    </div>
  );
}
