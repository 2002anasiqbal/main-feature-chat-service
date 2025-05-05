"use client";
import { usePathname } from "next/navigation";
import TabNavigation from "@/components/travel/TabNavigation";

export default function TravelLayout({ children }) {
  const pathname = usePathname();

  // Define the route(s) where TabNavigation should be hidden
  const excludedRoutes = [
    "/routes/travel/fly/search",
    "/routes/travel/fly-hotel/search",
    "/routes/travel/hotel/search",
    "/routes/travel/rental-car/search",
    "/routes/travel/holiday-homes/search"
  ];

  // Check if current route is in the excluded list
  const shouldShowTabs = !excludedRoutes.includes(pathname);

  return (
    <div className="bg-white min-h-screen pt-6">
      {/* Conditionally render TabNavigation */}
      {shouldShowTabs && <TabNavigation />}

      {/* Main Content */}
      <div className="mt-6">{children}</div>
    </div>
  );
}