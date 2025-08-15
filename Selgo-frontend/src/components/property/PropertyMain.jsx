"use client";
import React from "react";
import Image from "next/image";
import { useRouter, usePathname } from "next/navigation";
import SearchBar from "../root/SearchBar";
import ButtonWithIcon from "../root/ButtonWithIcon";
import { LiaMapMarkedAltSolid } from "react-icons/lia";

const tabs = ["Purchase", "Rent", "Sell", "Nutrition"];

const PropertyMain = () => {
    const router = useRouter();
    const pathname = usePathname();

    // Function to navigate to the selected tab's route
    const handleTabChange = (tab) => {
        const route = `/routes/property/${tab.toLowerCase()}`;
        router.push(route);
    };

    return (
        <div className="w-full">
            {/* Hero Section with Background Image */}
            <div className="relative w-full h-[400px]">
                <Image
                    src="/assets/property/property.jpeg"
                    alt="Property Background"
                    layout="fill"
                    objectFit="cover"
                    className="absolute inset-0"
                />
                <div className="absolute inset-0 bg-black/40 flex flex-col justify-center items-center text-white px-4">
                    <h1 className="text-3xl font-bold text-center">Has winters already moved in?</h1>
                    <p className="text-lg mt-2 text-center">
                        Don't think about it, at FINN we have 71,842 places you can stay
                    </p>

                    {/* Search Bar */}
                    <div className="flex flex-col sm:flex-row w-full max-w-xl pt-10 justify-center items-center gap-4 mx-auto px-4">
                        <SearchBar placeholder="Search" onChange={() => console.log("change")} />
                        <ButtonWithIcon
                            icon={LiaMapMarkedAltSolid}
                            label="Map"
                            onClick={() => router.push("/routes/map")}
                        />
                    </div>
                </div>
            </div>

            {/* Tabs Section - Responsive */}
            <div className="relative flex flex-wrap justify-center md:justify-between bg-white max-w-5xl mx-auto -top-10 h-20 rounded-lg px-10">
                {tabs.map((tab) => (
                    <button
                        key={tab}
                        className={`px-6 py-3 text-sm sm:text-md font-bold hover:underline ${
                            pathname.includes(tab.toLowerCase()) ? "underline border-black text-black font-bold" : "text-gray-600"
                        }`}
                        onClick={() => handleTabChange(tab)}
                    >
                        {tab}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default PropertyMain;