"use client";
import React, { useState, useEffect } from "react";
import Page from "@/components/GenerateCard";
import squareService from "@/services/squareService";

const RecommendedItems = () => {
  const [recommendedItems, setRecommendedItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  const fetchRecommendedItems = async () => {
    try {
      setLoading(true);

      const items = await squareService.getRecommendedItems(6);

      const formattedItems = items.map(item => ({
        id: item.id,
        image: item.primary_image,
        title: item.title,
        description: "General Item",
        price: item.price ? `$${item.price.toLocaleString()}` : "Price unavailable",
        originalData: item
      }));

      setRecommendedItems(formattedItems);
      } catch (err) {
        console.error("Failed to fetch recommended items:", err);
        setError("Failed to load recommended items");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendedItems();


  }, []);

  if (loading) return <p className="text-center py-4">Loading recommendations...</p>;
  if (error) return <p className="text-center py-4 text-red-500">{error}</p>;
  if (recommendedItems.length === 0) return null;

  return (
    <div className="my-10">
      <h2 className="font-bold text-3xl text-gray-800 mb-6">Recommended Items</h2>
      <Page columns={3} cards={recommendedItems} route="/routes/square" disableAutoFetch={true} />
    </div>
  );
};

export default RecommendedItems;
