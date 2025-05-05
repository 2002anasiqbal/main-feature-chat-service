"use client";
import Image from "next/image";
import { CiHeart } from "react-icons/ci";

export default function RecommendationJobCard({
  imageUrl,
  jobTitle,
  companyName,
  description,
  location,
  onHeartClick = () => {},
}) {
  return (
    <div className="flex flex-col gap-2 border rounded-xl shadow-sm p-4 w-full max-w-sm bg-white hover:shadow-md transition">
      {/* Top Row: Image + Title + Company + Heart */}
      <div className="flex items-start justify-between">
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 relative rounded-md overflow-hidden">
            <Image src={imageUrl} alt={jobTitle} fill className="object-contain" />
          </div>
          <div>
            <h3 className="text-sm font-semibold text-gray-800">{jobTitle}</h3>
            <p className="text-xs text-gray-500">{companyName}</p>
          </div>
        </div>
        <CiHeart
          size={20}
          className="text-gray-400 hover:text-red-500 cursor-pointer transition"
          onClick={onHeartClick}
        />
      </div>

      {/* Description */}
      <p className="text-sm text-gray-700 mt-1">{description}</p>

      {/* Location */}
      <p className="text-sm text-gray-500 mt-1">{location}</p>
    </div>
  );
}
