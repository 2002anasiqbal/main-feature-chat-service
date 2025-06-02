"use client";
import React, { useState, useEffect } from "react";
import SimpleCard from "./root/Card";
// import axios from "axios"; // BACKEND INTEGRATION POINT - Uncomment when integrating API
import { faker } from "@faker-js/faker"; // REMOVE THIS AFTER BACKEND INTEGRATION

// MOCK DATA FUNCTION - REMOVE THIS AFTER BACKEND INTEGRATION
const GenerateCards = (count) => {
  return Array.from({ length: count }, () => ({
    id: faker.string.uuid(),
    image: `https://picsum.photos/300/200?random=${Math.floor(Math.random() * 1000)}`,
    title: faker.commerce.productName(),
    description: faker.commerce.productDescription(),
    price: `$${faker.commerce.price(50, 200, 0)}`,
  }));
};

const Page = ({ columns = 3, route }) => { // Accept columns as a prop, default is 5
  const [cards, setCards] = useState([]); // State to store fetched data
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // BACKEND INTEGRATION POINT - Replace this with actual API calls
    const fetchCards = async () => {
      try {
        // const response = await axios.get("YOUR_BACKEND_API_ENDPOINT_HERE"); // BACKEND INTEGRATION POINT
        // setCards(response.data); // BACKEND INTEGRATION POINT
        setCards(GenerateCards(10)); // REMOVE THIS AFTER BACKEND INTEGRATION
      } catch (err) {
        console.error("Failed to fetch cards:", err);
        setError("Failed to load data"); // BACKEND INTEGRATION POINT
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, []);

  if (loading) return <p className="text-center py-10">Loading...</p>;
  if (error) return <p className="text-center py-10 text-red-500">{error}</p>;

  return (
    // <div className="min-h-screen bg-white p-6 sm:p-8 md:p-10 lg:p-12">
    <div className="min-h-screen bg-white pb-10">
      <div className="w-full">
        <div className={`grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-${columns} gap-2 md:gap-10`}>
          {cards.map((card) => (
            <SimpleCard
              key={card.id}
              image={card.image}
              title={card.title}
              description={card.description}
              price={card.price}
              route={route}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Page;