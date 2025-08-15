"use client";
import { useState } from "react";

export default function CompaniesIFollow({ companies = [] }) {
  const [followedCompanies, setFollowedCompanies] = useState(companies);

  const handleUnfollow = (companyName) => {
    setFollowedCompanies(followedCompanies.filter((c) => c !== companyName));
  };

  return (
    <div className="py-6 bg-white">
      {/* Header Section */}
      <h2 className="text-2xl font-semibold text-gray-800">Companies I follow</h2>
      <p className="mt-2 text-gray-700 font-semibold">
        Want to change your notification setting?
      </p>
      <p className="text-gray-600">
        Our customize notification lets you change notification settings. Here you can also
        get an overview of saved searches and others.
      </p>

      {/* Jobs Section */}
      <h3 className="mt-6 text-xl font-semibold text-gray-800">Jobs</h3>
      {followedCompanies.length > 0 ? (
        <div className="mt-4 space-y-4">
          {followedCompanies.map((company, index) => (
            <div key={index} className="flex justify-between items-center border-b pb-2">
              <p className="font-semibold text-gray-800">{company}</p>
              <button
                onClick={() => handleUnfollow(company)}
                className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 transition"
              >
                Unfollow
              </button>
            </div>
          ))}
        </div>
      ) : (
        <p className="mt-4 text-gray-500">You are not following any companies.</p>
      )}
    </div>
  );
}