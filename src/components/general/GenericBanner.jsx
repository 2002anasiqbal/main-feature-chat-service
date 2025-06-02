"use client";
import React from "react";
import Image from "next/image";

const GenericBanner = ({
  title = "Default Banner Title",
  description = "This is a default description for the banner.",
  buttonText = "Learn More",
  buttonLink = "#",
  imageUrl = "https://picsum.photos/500/300?random=1", // Placeholder image
}) => {
  return (
    <div className="w-full my-10 mx-auto bg-white shadow-md rounded-lg overflow-hidden flex flex-col md:flex-row">
      {/* Left Content Section (Takes 2/3 of space) */}
      <div className="w-full md:w-2/3 p-6 flex flex-col justify-center">
        <h2 className="text-2xl font-semibold text-gray-800 mb-2">{title}</h2>
        <p className="text-gray-600 mb-4">{description}</p>
        <a
          href={buttonLink}
          className="flex justify-center sm:w-1/4 w-1/3  bg-teal-600 text-white px-6 py-2 rounded-md hover:bg-teal-700 transition"
        >
          {buttonText}
        </a>
      </div>

      {/* Right Image Section (Takes 1/3 of space) */}
      <div className="w-full md:w-1/3">
        <Image
          src={imageUrl}
          alt="Banner Image"
          width={400}
          height={300}
          className="w-full h-full object-cover"
        />
      </div>
    </div>
  );
};

export default GenericBanner;