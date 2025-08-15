"use client";
import React, { useState, useEffect } from "react";
import Page from "@/components/GenerateCard";
import boatService from "@/services/boatService";

const RecommendedBoats = () => {
  const [recommendedBoats, setRecommendedBoats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  const fetchRecommendedBoats = async () => {
    try {
      setLoading(true);
      
      // Use the new recommended boats endpoint
      const boats = await boatService.getRecommendedBoats(6);
      
      // Format boats for display
      const formattedBoats = boats.map(boat => ({
        id: boat.id,
        image: boat.primary_image,
        title: boat.title,
        description: boat.make ? `${boat.make} ${boat.model || ""}`.trim() : "No details available",
        price: boat.price ? `$${boat.price.toLocaleString()}` : "Price unavailable",
        originalData: boat
      }));
      
      setRecommendedBoats(formattedBoats);
      } catch (err) {
        console.error("Failed to fetch recommended boats:", err);
        setError("Failed to load recommended boats");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendedBoats();
    
  
  }, []);

  if (loading) return <p className="text-center py-4">Loading recommendations...</p>;
  if (error) return <p className="text-center py-4 text-red-500">{error}</p>;
  if (recommendedBoats.length === 0) return null;

  return (
    <div className="my-10">
      <h2 className="font-bold text-3xl text-gray-800 mb-6">Recommended Boats</h2>
      <Page columns={3} cards={recommendedBoats} route="/routes/boat" disableAutoFetch={true} />
    </div>
  );
};

export default RecommendedBoats;