"use client";
import { useState } from "react";
import Image from "next/image";

export default function Alris() {
    const [selectedText, setSelectedText] = useState("Add text");

    return (
        <div className="w-full bg-white min-h-screen py-6">
            {/* Header */}
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-teal-600">Alris</h1>
                <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600">
                    Button
                </button>
            </div>

            {/* Banner Section */}
            <div className="mt-4 w-full h-60 bg-gray-300 rounded-lg"></div>

            {/* Content Section */}
            <div className="mt-6">
                <h2 className="text-xl text-gray-900 font-bold">Alris</h2>
                <p className="text-gray-700">
                    Lorem Ipsum is simply dummy text of the printing and typesetting
                    industry. Lorem Ipsum has been the industry's standard dummy text ever
                    since the 1500s, when an unknown printer took a galley of type and
                    scrambled it to make a type specimen book. It has survived not only
                    five centuries, but also the leap into electronic typesetting,
                    remaining essentially unchanged.
                </p>
                <button className="mt-4 border border-gray-500 text-gray-700 px-5 py-2 rounded-md hover:bg-gray-200">
                    Button
                </button>
            </div>

            {/* Image Grid */}
            <div className="mt-10 grid grid-cols-3 gap-4">
                <div className="col-span-2 h-128 bg-gray-300 rounded-lg"></div>
                <div className="space-y-4">
                    <div className="h-62 bg-gray-300 rounded-lg"></div>
                    <div className="h-62 bg-gray-300 rounded-lg"></div>
                </div>
                <div className="col-span-3 h-60 bg-gray-300 rounded-lg"></div>
            </div>

            {/* Center Button */}
            <div className="flex justify-center mt-4">
                <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600">
                    Button
                </button>
            </div>

            {/* Text and Dropdown Section */}
            <div className="mt-10 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-800">
                    Lorem Ipsum is simply dummy text of the printing and typesetting
                    industry
                </h2>
                {/* Right Aligned Button */}
                    <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600">
                        Button
                    </button>
            </div>
            <select
                value={selectedText}
                onChange={(e) => setSelectedText(e.target.value)}
                className="border mt-10 w-sm text-gray-600 border-gray-400 px-4 py-2 rounded-md focus:outline-none"
            >
                <option>Add text</option>
                <option>Option 1</option>
                <option>Option 2</option>
            </select>

            {/* Centered and Smaller Text Sections */}
            <div className="max-w-2/3 mx-auto mt-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-44">
                    <div>
                        <p className="font-semibold text-teal-600">Lorem Ipsum</p>
                        <p className="text-gray-700 text-sm">
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </p>
                        <p className="font-semibold text-teal-600 mt-2">Lorem Ipsum</p>
                        <p className="text-gray-700 text-sm">
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </p>
                        <p className="font-semibold text-teal-600 mt-2">Lorem Ipsum</p>
                        <p className="text-gray-700 text-sm">
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </p>
                    </div>
                    <div>
                        <p className="font-semibold text-teal-600">Lorem Ipsum</p>
                        <p className="text-gray-700 text-sm">
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </p>
                        <p className="font-semibold text-teal-600 mt-2">Lorem Ipsum</p>
                        <p className="text-gray-700 text-sm">
                            Lorem Ipsum is simply dummy text of the printing and typesetting industry.
                        </p>
                    </div>
                </div>
            </div>


        </div>
    );
}