import React from "react";
import { FaMapMarkerAlt } from "react-icons/fa"; // or any map pin icon

export default function JobCard({ job }) {
  const {
    title = "Latest plumbing jobs posted on Mittanbud",
    location = "1470 LØRENSKOG",
    description = "I unscrewed the plastic pipe due to a slight smell...",
    mapEmbedUrl = "https://www.google.com/maps/embed?pb=..." // Replace with valid embed link
  } = job || {};

  return (
    <div className="w-full border border-gray-200 rounded-md bg-white shadow-sm overflow-hidden">
      {/* Map Preview */}
      <div className="w-full h-44 bg-gray-100">
        <iframe
          src={mapEmbedUrl}
          width="100%"
          height="100%"
          style={{ border: 0 }}
          allowFullScreen
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        />
      </div>

      {/* Card Content */}
      <div className="p-4">
        <h2 className="text-lg font-semibold text-gray-900 mb-2">
          {title}
        </h2>

        <div className="flex items-center text-sm text-gray-700 mb-2">
          <FaMapMarkerAlt className="text-blue-600 mr-1" />
          <span className="font-medium">{location}</span>
        </div>

        <p className="text-sm text-gray-700 leading-relaxed">
          {description}
        </p>
      </div>
    </div>
  );
}
