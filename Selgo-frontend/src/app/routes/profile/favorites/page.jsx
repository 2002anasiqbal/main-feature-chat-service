"use client";
import { useState, useEffect } from "react";
import FindingsList from "@/components/profile/FindingLists";
import boatService from "@/services/boatService";
import motorcycleService from "@/services/motorcycleService";

export default function FavoritesPage() {
  const [totalFavoritesCount, setTotalFavoritesCount] = useState(0);

  useEffect(() => {
    const fetchFavoritesCount = async () => {
      try {
        // Fetch both boat and motorcycle favorites count
        const boatCount = await boatService.getFavoritesCount();
        const motorcycleCount = await motorcycleService.getFavoritesCount();
        
        // Combine the counts
        const totalCount = boatCount + motorcycleCount;
        setTotalFavoritesCount(totalCount);
      } catch (error) {
        console.error('Error fetching favorites count:', error);
      }
    };

    // Only fetch if user is logged in
    const token = localStorage.getItem('accessToken');
    if (token) {
      fetchFavoritesCount();
    }
  }, []);

  const findings = [
    { title: "My Findings", ads: 2 },
    { title: "Favorite Items", ads: totalFavoritesCount }, // Combined count
    { title: "Recently Viewed", ads: 3 },
  ];

  return (
    <div className="my-10">
      {/* No tabs - just pass "combined" as type to show both */}
      <FindingsList findings={findings} type="combined" />
    </div>
  );
}