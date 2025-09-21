"use client";
import React, { useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { FaArrowLeft } from "react-icons/fa";
import { FiArrowRight, FiArrowLeft } from "react-icons/fi";

const ProductDetail = ({
  title,
  price,
  currency,
  salePrice,
  productImages,
  description,
  keyInfo,
  sellerInfo,
  onMessageClick,
  onFixDoneClick,
  onContactSellerClick,
  expandedKeyInfo, // New prop for expanded info
}) => {
  const router = useRouter();
  const [currentImage, setCurrentImage] = useState(0);
  const [showExpandedInfo, setShowExpandedInfo] = useState(false); // Local state for expansion
  

// In ProductDetail.jsx - Add this function near the top of the component
  const getImageUrl = (imageUrl) => {
    if (!imageUrl) return "/assets/boat/placeholder.jpg";
    
    // If it's already a full URL
    if (imageUrl.startsWith('http')) return imageUrl;
    
    // If it's a relative path starting with /uploads/
    if (imageUrl.startsWith('/uploads/')) return imageUrl;
    
    // Otherwise, prepend the uploads path
    return `/uploads/${imageUrl}`;
  };


  // Next Image Function
  const nextImage = () => {
    setCurrentImage((prev) => (prev + 1) % productImages.length);
  };

  // Previous Image Function
  const prevImage = () => {
    setCurrentImage((prev) =>
      prev === 0 ? productImages.length - 1 : prev - 1
    );
  };

  // Handle See More click locally
  const handleSeeMoreClick = () => {
    setShowExpandedInfo(!showExpandedInfo);
  };
  
  return (
    <div className="max-w-6xl mx-auto p-6 lg:p-12 bg-white">
      {/* Back Button */}
      <button
        className="flex items-center text-gray-700 hover:text-black font-medium mb-6"
        onClick={() => router.back()}
      >
        <FaArrowLeft className="mr-2" />
        Back
      </button>

      {/* Image Carousel - Full Width at Top */}
      <div className="w-full mb-8">
        <div className="relative">
          <Image
            src={getImageUrl(productImages[currentImage])}
            alt={title}
            width={1200}
            height={600}
            className="rounded-lg object-cover w-full h-80 sm:h-96 md:h-[500px] lg:h-[600px] xl:h-[700px] border"
            unoptimized={true}
          />
          
          {/* Image Counter */}
          <div className="absolute top-3 right-3 bg-black text-white px-3 py-1 text-sm rounded-lg shadow-md">
            <span className="font-semibold">{currentImage + 1}</span> / {productImages.length}
          </div>

          {/* Navigation Arrows */}
          <button
            onClick={prevImage}
            className="absolute left-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100"
          >
            <FiArrowLeft size={22} className="text-gray-600"/>
          </button>
          <button
            onClick={nextImage}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100"
          >
            <FiArrowRight size={22} className="text-gray-600"/>
          </button>
        </div>
      </div>

      {/* Product Information - Below Image */}
      <div className="space-y-6">
        {/* Title */}
        <h1 className="text-3xl lg:text-4xl font-bold text-gray-900">{title}</h1>

        {/* Pricing Section */}
        <div className="text-gray-700 text-lg">
          <p className="text-2xl font-bold text-black">
            {currency} {price}
          </p>
          {salePrice && (
            <p className="mb-3 text-gray-800 text-lg font-medium">
              For Sale: <br /> {currency} {salePrice}
            </p>
          )}
        </div>

        {/* Key Info */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800">Key Info</h3>
          {showExpandedInfo && expandedKeyInfo ? (
            <div className="text-gray-600">{expandedKeyInfo}</div>
          ) : (
            <p className="text-gray-600">{keyInfo}</p>
          )}
          <button
            onClick={handleSeeMoreClick}
            className="mt-2 px-5 py-2 border border-gray-400 rounded-md font-medium text-gray-800 hover:bg-gray-100 transition"
          >
            {showExpandedInfo ? "See Less" : "See More"}
          </button>
        </div>
      </div>

      {/* Seller Info and Contact - Below Product Info */}
      <div className="mt-10 border-t pt-6 flex flex-col lg:flex-row justify-between items-start">
        {/* Product Description Section */}
        <div className="w-full lg:w-3/4 space-y-4 mb-6 lg:mb-0">
          <h3 className="text-2xl font-bold text-gray-900">Description</h3>
          <p className="text-gray-700">{description}</p>
        </div>

        {/* Seller Info Card */}
        <div className="w-full lg:w-1/4 shadow-md p-4 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-900">{sellerInfo.name}</h3>
          {sellerInfo.website && (
            <a
              href={sellerInfo.website}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-teal-600 hover:underline mt-1"
            >
              Company website
            </a>
          )}
          {sellerInfo.moreAds && (
            <a
              href={sellerInfo.moreAds}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-teal-600 hover:underline mt-1"
            >
              More ads
            </a>
          )}
          {sellerInfo.followCompany && (
            <a
              href={sellerInfo.followCompany}
              target="_blank"
              rel="noopener noreferrer"
              className="block text-teal-600 hover:underline mt-1"
            >
              Follow company
            </a>
          )}

          {/* Buttons */}
          <button
            onClick={onMessageClick}
            className="w-full mt-4 px-5 py-2 bg-teal-600 text-white rounded-md font-medium hover:bg-teal-700 transition"
          >
            Send Message
          </button>
          <button
            onClick={onContactSellerClick}
            className="w-full mt-2 px-5 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition"
          >
            Contact Seller
          </button>
          <button
            onClick={onFixDoneClick}
            className="w-full mt-2 px-5 py-2 border border-gray-400 rounded-md font-medium text-gray-800 hover:bg-gray-100 transition"
          >
            Ask for Fix Done
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail;