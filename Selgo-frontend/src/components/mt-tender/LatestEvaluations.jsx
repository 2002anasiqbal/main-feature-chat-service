"use client";
import React, { useRef } from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";
import LatestEvaluationCard from "@/components/mt-tender/LatestEvaluationCard";

const evaluations = [
  {
    name: "John Doe",
    rating: 4.8,
    review: "Excellent service, quick turnaround!",
    job: "Bathroom renovation",
    location: "Oslo",
    avatar: "/assets/my-tender/user1.jpg",
  },
  {
    name: "Anna Smith",
    rating: 5.0,
    review: "Very professional and polite.",
    job: "Kitchen remodeling",
    location: "Bergen",
    avatar: "/assets/my-tender/user2.jpg",
  },
  {
    name: "Mikkel Hansen",
    rating: 4.5,
    review: "Happy with the work done.",
    job: "Flooring installation",
    location: "Trondheim",
    avatar: "/assets/my-tender/user3.jpg",
  },
  {
    name: "Emma Larsen",
    rating: 4.9,
    review: "Great communication and quality.",
    job: "Painting exterior",
    location: "Stavanger",
    avatar: "/assets/my-tender/user4.jpg",
  },
];

export default function LatestEvaluations() {
  const scrollRef = useRef(null);

  const scrollLeft = () => {
    const card = scrollRef.current?.firstElementChild;
    const cardWidth = card ? card.offsetWidth : 350;
    scrollRef.current?.scrollBy({ left: -cardWidth, behavior: "smooth" });
  };

  const scrollRight = () => {
    const card = scrollRef.current?.firstElementChild;
    const cardWidth = card ? card.offsetWidth : 350;
    scrollRef.current?.scrollBy({ left: cardWidth, behavior: "smooth" });
  };

  return (
    <div className="w-full max-w-7xl mx-auto px-4 md:px-6 lg:px-8 pb-10">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Latest evaluations</h2>
          <p className="text-sm text-gray-500">
            Latest evaluations of completed jobs at{" "}
            <span className="text-teal-600 font-medium">Mittanbud</span>
          </p>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={scrollLeft}
            className="p-2 border rounded-full text-teal-600 hover:bg-gray-100"
          >
            <FaChevronLeft />
          </button>
          <button
            onClick={scrollRight}
            className="p-2 border rounded-full text-teal-600 hover:bg-gray-100"
          >
            <FaChevronRight />
          </button>
        </div>
      </div>
      <div
        ref={scrollRef}
        className="flex overflow-x-auto space-x-4 scroll-smooth 
          [&::-webkit-scrollbar]:hidden 
          [-ms-overflow-style:none] 
          [scrollbar-width:none]"
      >
        {evaluations.map((evaluation, index) => (
          <div key={index} className="min-w-[300px] max-w-sm flex-shrink-0">
            <LatestEvaluationCard {...evaluation} />
          </div>
        ))}
      </div>
    </div>
  );
}