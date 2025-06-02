"use client";
import React from "react";
import OnlineCarCard from "./OnlineCarCard"; // Importing the car card component

const stats = [
    { value: "102,973 +", label: "Cars so far in the bidding round" },
    { value: "148 +", label: "New cars on the bidding round every day" },
    { value: "1,203", label: "Cars on the way in the next few days" },
];

const BidOnCars = () => {
    return (
        <div className="w-full py-10 space-y-6">
            {/* Heading & Description */}
            <div className="flex flex-col md:flex-row items-center md:items-start gap-8">
                {/* Left Side (Text + Buttons) */}
                <div className="w-full md:w-1/2 space-y-4">
                    <p className="text-teal-600 font-medium">Online car company</p>
                    <h1 className="text-3xl font-bold text-gray-900 leading-tight">
                        Bid on cars with condition report
                    </h1>
                    <p className="text-gray-600">
                        Buy cars for resale. Get the opportunity to buy appraised cars with a condition report for an attractive price.
                    </p>

                    {/* Buttons */}
                    <div className="flex flex-col sm:flex-row gap-4">
                        <button className="w-full sm:w-auto px-6 py-3 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all">
                            Create a free reseller account
                        </button>
                        <button className="w-full sm:w-auto px-6 py-3 border text-gray-800 border-gray-400 rounded-md font-semibold hover:bg-gray-200 transition-all">
                            Login
                        </button>
                    </div>

                    {/* Bullet Points */}
                    <ul className="list-disc list-inside text-gray-700 space-y-1">
                        <li>Free access to the auction platform</li>
                        <li>An average of 148 new cars on the bidding round each day</li>
                        <li>Wide selection of cars with condition report</li>
                    </ul>
                </div>

                {/* Right Side (Car Card) */}
                <div className="w-full md:w-1/2 flex justify-center">
                    <div className="w-full max-w-md">
                        <OnlineCarCard />
                    </div>
                </div>
            </div>

            {/* Statistics Section */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {stats.map((stat, index) => (
                    <div key={index} className="bg-teal-700 text-white p-4 rounded-md text-center">
                        <p className="text-2xl font-bold">{stat.value}</p>
                        <p className="text-sm">{stat.label}</p>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BidOnCars;