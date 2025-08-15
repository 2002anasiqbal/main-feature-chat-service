import React from "react";
import { AiFillStar, AiOutlineStar } from "react-icons/ai";

export default function EvaluationCard({ data }) {
  const {
    rating,
    title,
    text,
    date,
    author,
    company,
    location
  } = data;

  // Renders stars up to 5, filling those <= rating.
  const renderStars = (ratingValue) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      if (i <= ratingValue) {
        stars.push(<AiFillStar key={i} className="text-gray-500 mr-1" />);
      } else {
        stars.push(<AiOutlineStar key={i} className="text-gray-500 mr-1" />);
      }
    }
    return <div className="flex">{stars}</div>;
  };

  return (
    <div className="w-full border border-gray-200 rounded-md shadow-sm overflow-hidden">
      <div className="p-4 bg-teal-50">
        {/* Star rating */}
        <div className="mb-2">{renderStars(rating)}</div>
        {/* Title */}
        <h2 className="text-lg font-semibold text-gray-900">{title}</h2>
        {/* Main text */}
        <p className="text-sm text-gray-700 mt-1">{text}</p>
        {/* Date */}
        <p className="text-sm text-gray-600 font-medium mt-3">{date}</p>
        {/* Author + Company + Location */}
        <div className="flex items-start mt-2">
          {/* Avatar Placeholder: first letter of author */}
          <div className="w-10 h-10 bg-gray-100 text-gray-700 rounded-sm flex items-center justify-center font-bold mr-3">
            {author?.[0]?.toUpperCase() || "?"}
          </div>
          <div className="text-sm text-gray-700 leading-tight">
            <p>
              <span className="font-medium">{author}</span> about {company}
            </p>
            <p>{location}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
