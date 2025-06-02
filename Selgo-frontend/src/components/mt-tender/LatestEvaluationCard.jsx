"use client";
import React from "react";
import Image from "next/image";
import { FaStar } from "react-icons/fa";

const LatestEvaluationCard = ({
  rating = 5,
  title = "Title Here",
  description = "Some brief feedback about the product or service.",
  userImage = "/placeholder.jpg",
  userName = "User Name",
  date = "24-03-26",
  maxStars = 5,
  starSize = 20,
  cardWidth = "w-full md:w-80",
}) => {
  return (
    <div className={`border border-gray-200 rounded-xl p-4 bg-white ${cardWidth}`}>
      {/* Rating Stars */}
      <div className="flex mb-2">
        {[...Array(maxStars)].map((_, i) => (
          <FaStar
            key={i}
            className={i < rating ? "text-yellow-500" : "text-gray-300"}
            size={starSize}
          />
        ))}
      </div>

      {/* Title */}
      <h3 className="text-lg font-bold text-gray-900">{title}</h3>

      {/* Description */}
      <p className="text-gray-700 mt-1">{description}</p>

      {/* User Info */}
      <div className="flex items-center gap-3 mt-4">
        <Image
          src={userImage}
          alt={userName}
          width={40}
          height={40}
          className="rounded-full object-cover"
        />
        <div>
          <p className="text-sm font-semibold text-gray-800">{userName}</p>
          <p className="text-xs text-gray-500">{date}</p>
        </div>
      </div>
    </div>
  );
};

export default LatestEvaluationCard;
