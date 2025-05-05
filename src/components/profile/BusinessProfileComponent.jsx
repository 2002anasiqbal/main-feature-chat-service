"use client";
import React from "react";
import Image from "next/image";
import InformationTiles from "./InformationTile";

// Example Information Tiles
const informationTiles = [
  {
    title: "Contact and information",
    description:
      "Here you will find what you need in terms of practical information as a business customer in FINN",
    imageUrl: "/assets/profile/5.svg",
    buttonText: "Read More",
    onClick: () => window.location.href = "/contact",
  },
  {
    description:
      "Read more about our products and be inspired by how you can get the most out of FINN.no as a business customer",
    imageUrl: "/assets/profile/5.svg",
    buttonText: "Read More",
    onClick: () => window.location.href = "/products",
  },
];

// User Info
const userInfo = {
  name: "Alexa Rawles",
  email: "alexarawles@gmail.com",
  profileImage: "/assets/profile/4.svg",
};

export default function BusinessProfileComponent() {
  return (
    <div className="w-full">
      {/* Banner Image */}
      <div className="w-full h-64 bg-gray-200 mb-4 relative">
        <Image 
          src="/assets/profile/4.svg" 
          alt="Accessories banner" 
          layout="fill"
          objectFit="cover"
        />
      </div>

      {/* Main Content */}
      <div className="py-4">
        {/* Companies Section */}
        <h1 className="text-4xl font-semibold text-gray-700 mb-4">
          Companies you have access to
        </h1>

        <div className="mb-8">
          <p className="text-gray-700 mb-2">
            You have no businesses associated with this Schibsted Marketplaces account
          </p>
          <p className="text-gray-700">
            It appears that your account is not associated with a company in our system yet. We
            recommend that you speak to your Schibsted Marketplaces account administrator to access
            the Business Center.
          </p>
        </div>

        {/* User Profile Section */}
        <div className="flex items-center mb-10">
          <div className="w-16 h-16 rounded-full overflow-hidden mr-4 relative">
            <Image 
              src={userInfo.profileImage} 
              alt={`${userInfo.name}'s profile`} 
              layout="fill"
              objectFit="cover"
            />
          </div>
          <div>
            <h2 className="text-xl font-medium text-gray-800">{userInfo.name}</h2>
            <p className="text-gray-600">{userInfo.email}</p>
          </div>
        </div>

        {/* Become a Customer Section */}
        <div className="mb-10">
          <h2 className="text-3xl font-semibold text-gray-700 mb-4">
            Become a business customer
          </h2>
          <p className="text-gray-700 mb-4">
            As a business customer at FINN.no, we make it easier to advertise and hit the right
            target group.
          </p>

          <ul className="list-disc pl-6 mb-6 text-gray-700">
            <li className="mb-1">Advertisements on Norway's largest websites</li>
            <li className="mb-1">Payment by invoice</li>
            <li className="mb-1">Company profiling</li>
          </ul>

          <button className="bg-teal-500 hover:bg-teal-600 text-white font-medium py-2 px-6 rounded transition duration-200">
            Get started
          </button>
        </div>
      </div>

      {/* Information Tiles */}
      <InformationTiles tiles={informationTiles} />
    </div>
  );
}