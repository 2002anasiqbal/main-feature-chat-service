"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { CiHeart } from "react-icons/ci";

const SimpleCard = ({ 
    id, 
    image = "/default.jpg", 
    title = "Default Title", 
    description = "No description", 
    price = "$0",
    route = `/routes/product-details?id=${id}` // ✅ Default route if none provided
}) => {
    const [isMounted, setIsMounted] = useState(false);
    const router = useRouter(); 

    useEffect(() => setIsMounted(true), []);

    if (!isMounted) return null; // Prevents hydration mismatch

    // Handle redirection to the provided route
    const handleCardClick = () => {
        router.push(route); // ✅ Uses dynamic route
    };

    return (
        <div 
            className="hover:shadow-[2px_2px_4px_1px_rgba(0,0,0,0.9)] relative group rounded-lg overflow-visible transform transition duration-100 hover:scale-100 group-hover:border-transparent cursor-pointer"
            onClick={handleCardClick}
        >
            {/* Outer Container */}
            <div className="absolute hover:shadow-black h-84 inset-0 rounded-lg bg-white border border-gray-200 group-hover:bg-teal-800 transition duration-100 group-hover:border-transparent"></div>

            {/* Inner Container */}
            <div className="relative hover:shadow-[2px_2px_4px_1px_rgba(0,0,0,0.9)] h-80 m-2 rounded-lg bg-white overflow-hidden shadow-md group-hover:shadow-lg">
                {/* Image Section */}
                <div className="relative w-full h-4/6 hover:h-full group-hover:h-full rounded-lg overflow-hidden transition-all duration-300 shadow-md group-hover:shadow-lg">
                    <Image
                        src={image}
                        alt={title}
                        width={300}
                        height={200}
                        className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
                    />
                    {/* Price Overlay */}
                    <div className="absolute bottom-0 w-full transition-all duration-300 group-hover:h-1/3">
                        <div className="absolute inset-0 bg-black rounded-lg opacity-50"></div>
                        <div className="relative px-3 py-5 z-10">
                            <div className="flex justify-end group-hover:hidden">
                                <span className="text-white text-md font-black">{price}</span>
                            </div>
                            <div className="hidden group-hover:block">
                                <div className="flex justify-between items-start">
                                    <h3 className="text-sm font-semibold text-white">{title}</h3>
                                    <CiHeart className="text-white text-2xl cursor-pointer" />
                                </div>
                                <span className="block text-xs font-black text-white mt-1">{price}</span>
                                <p className="text-xs text-white mt-2 truncate">{description}</p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Bottom Text Section */}
                <div className="p-3 group-hover:hidden">
                    <div className="flex justify-between items-center">
                        <h3 className="text-md font-semibold text-gray-900">{title}</h3>
                        <CiHeart className="text-teal-600 text-lg cursor-pointer" />
                    </div>
                    <p className="truncate text-xs text-gray-600 mt-1">{description}</p>
                </div>
            </div>
        </div>
    );
};

export default SimpleCard;