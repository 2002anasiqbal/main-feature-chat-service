"use client";
import React, { useState } from "react";

const PriceGrid = ({ data }) => {
    const [searchQuery, setSearchQuery] = useState("");

    // Filtered Data based on Search
    const filteredData = data.filter((item) =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase())
    );

    return (
        <div className="w-full max-w-6xl mx-auto mt-10 px-4 py-10">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Price per square meter</h2>

            {/* Search Bar */}
            <div className="mb-6">
                <input
                    type="text"
                    placeholder="🔍 Search"
                    className="block text-gray-500 mx-auto w-full max-w-lg px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>

            {/* Grid Layout */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                {filteredData.length > 0 ? (
                    filteredData.map((item, index) => (
                        <div key={index} className="bg-gray-100 p-6 rounded-lg shadow-md">
                            <h3 className="text-md font-semibold text-gray-700">{item.title}</h3>
                            <p className="text-xl font-bold text-gray-900">{item.value}</p>
                            <p className="text-sm text-gray-600">{item.description}</p>
                        </div>
                    ))
                ) : (
                    <p className="text-gray-500">No results found.</p>
                )}
            </div>
        </div>
    );
};

export default PriceGrid;
