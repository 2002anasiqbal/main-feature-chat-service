"use client";
import React, { useState, useEffect } from "react";
import Page from "@/components/GenerateCard";
import carService from "@/services/carService";

const RecommendedCars = () => {
  const [recommendedCars, setRecommendedCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
  const fetchRecommendedCars = async () => {
    try {
      setLoading(true);

      const cars = await carService.getRecommendedCars(6);

      const formattedCars = cars.map(car => ({
        id: car.id,
        image: car.primary_image,
        title: car.title,
        description: car.make ? `${car.make} ${car.model || ""}`.trim() : "No details available",
        price: car.price ? `$${car.price.toLocaleString()}` : "Price unavailable",
        originalData: car
      }));

      setRecommendedCars(formattedCars);
      } catch (err) {
        console.error("Failed to fetch recommended cars:", err);
        setError("Failed to load recommended cars");
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendedCars();


  }, []);

  if (loading) return <p className="text-center py-4">Loading recommendations...</p>;
  if (error) return <p className="text-center py-4 text-red-500">{error}</p>;
  if (recommendedCars.length === 0) return null;

  return (
    <div className="my-10">
      <h2 className="font-bold text-3xl text-gray-800 mb-6">Recommended Cars</h2>
      <Page columns={3} cards={recommendedCars} route="/routes/cars" disableAutoFetch={true} />
    </div>
  );
};

export default RecommendedCars;
