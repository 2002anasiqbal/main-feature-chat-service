"use client";
import { useState, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import TabNavigation from "@/components/travel/TabNavigation";
import Fly from "@/app/routes/travel/fly/page";
import Hotel from "@/app/routes/travel/hotel/page";
import RentalCar from "@/app/routes/travel/rental-car/page";
import FlyHotel from "@/app/routes/travel/fly-hotel/page";
import HolidayHomes from "@/app/routes/travel/holiday-homes/page";

const pageComponents = {
  "/routes/travel/fly": <Fly />,
  "/routes/travel/hotel": <Hotel />,
  "/routes/travel/rental-car": <RentalCar />,
  "/routes/travel/fly-hotel": <FlyHotel />,
  "/routes/travel/holiday-homes": <HolidayHomes />,
};

export default function Travel() {
  const router = useRouter();
  const pathname = usePathname();
  const [selectedPage, setSelectedPage] = useState("/routes/travel/fly");

  // Redirect to /routes/travel/fly if user is at /routes/travel
  useEffect(() => {
    if (pathname === "/routes/travel") {
      router.replace("/routes/travel/fly");
    }
  }, [pathname, router]);

  return (
    <div className="bg-white min-h-screen py-6">
      {/* Persistent Tab Navigation */}
      <TabNavigation onTabChange={(page) => setSelectedPage(page)} />

      {/* Render the selected page content under tabs */}
      <div className="mt-6">{pageComponents[selectedPage] || <Fly />}</div>
    </div>
  );
}
