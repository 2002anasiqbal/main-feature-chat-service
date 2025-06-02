// /components/mt-tender/plummer/RecommendationCard.jsx

import React from "react";
// Optionally import an icon for stars, e.g., from react-icons: 
// import { AiFillStar } from "react-icons/ai";

export default function RecommendationCard({ data }) {
  const {
    companyName,
    logoUrl,
    promoted,
    rating,
    totalReviews,
    jobsCount,
    location,
    reviewHeadline,
    review
  } = data;

  return (
    <div className="relative w-full max-w-xl border border-gray-200 rounded-md bg-white shadow-sm p-4 mb-6">
      {/* "Promotert" badge in the top-left corner if promoted is true */}
      {promoted && (
        <div className="absolute top-5 left-0 -translate-x-2 -translate-y-2 bg-yellow-200 text-amber-900 text-xs font-semibold px-2 py-1 rounded-md shadow">
          Promotert
        </div>
      )}

      {/* Top Section: Logo, Company Name, Rating, and “Ask for quote” Button */}
      <div className="flex items-start justify-between mb-3">
        {/* Logo & Company Info */}
        <div className="flex items-start gap-3">
          <img
            src={logoUrl}
            alt={companyName}
            className="w-16 h-16 object-cover rounded-md border border-gray-100"
          />
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{companyName}</h2>
            <div className="flex items-center">
              {/* Optional star icon: <AiFillStar className="text-yellow-500 mr-1" /> */}
              <span className="text-yellow-500 font-bold mr-1">★</span>
              <p className="text-gray-800 text-sm">
                {rating} <span className="text-gray-500">({totalReviews})</span>
              </p>
            </div>
            <p className="text-xs text-gray-500 mt-1 bg-gray-200 text-center rounded-sm">{reviewHeadline}</p>
          </div>
        </div>

        {/* “Ask for quote” Button */}
        <button className="whitespace-nowrap bg-transparent border-2 hover:bg-teal-300 transition text-blue-800 hover:text-white text-sm font-medium py-2 px-4 rounded-md">
          Ask for quote
        </button>
      </div>

      {/* Middle Text: Job Count, Location, Average Rating */}
      <p className="text-sm text-gray-700">
        <span className="font-semibold">{companyName}</span> has carried out{" "}
        <span className="font-semibold">{jobsCount}</span> jobs at Mittanbud in{" "}
        <span className="font-semibold">{location}</span>, with an average of{" "}
        <span className="font-semibold">{rating}</span> out of 5 stars.
      </p>

      {/* Review Box */}
      <div className="mt-4 bg-gray-100 rounded-md p-3">
        <div className="flex">
        <img
            src={logoUrl}
            alt={companyName}
            className="w-10 h-10 object-cover rounded-md border border-gray-100"
          />
          <p className="text-xs text-gray-500 mb-1">
            Nylig evaluert av <span className="font-semibold">{review.author}</span> <br /> {review.date}
          </p>
        </div>
        <p className="text-sm text-gray-700 leading-relaxed">{review.text}</p>
        {/* “Show More” button can expand text if you implement toggling */}
        <button className="text-blue-600 text-sm mt-2 font-medium hover:underline">
          Show More
        </button>
      </div>
    </div>
  );
}
