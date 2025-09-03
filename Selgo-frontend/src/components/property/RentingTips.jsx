"use client";
import React from "react";
import Image from "next/image";

const RentingTips = () => {
    return (
        <div className="w-full px-4 sm:px-6 mt-10 py-10">
            {/* Heading */}
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-6">
                5 tips from us for those who are going to rent
            </h2>

            {/* Desktop Layout (lg screens) - Absolute positioning */}
            <div className="relative hidden lg:block mb-16">
                {/* Image - Moved more to the left */}
                <div className="w-3/4">
                    <Image
                        src="/assets/property/7.svg"
                        alt="Couple Renting"
                        width={600}
                        height={400}
                        className="rounded-lg object-cover w-full h-auto"
                    />
                </div>

                {/* Tips Box - Positioned absolute on large screens */}
                <div className="absolute top-1/2 right-0 transform -translate-y-1/2 max-w-md">
                    <div className="bg-gray-100 py-20 px-6 rounded-lg shadow-md">
                        <ol className="list-decimal list-inside text-gray-700 text-lg space-y-2">
                            <li>
                                Write a lease with a notice period. Use{" "}
                                <span className="text-blue-600 cursor-pointer underline">
                                    FINN's rental contract
                                </span>{" "}
                                completely free of charge.
                            </li>
                            <li>
                                Make sure you have a deposit in your own account in your name
                                (deposit account).
                            </li>
                            <li>
                                Document any errors or defects in the home upon moving in.
                            </li>
                            <li>
                                Report any repairs to the landlord. It is not your responsibility!
                            </li>
                            <li>
                                Remember that the electricity bill is often not included in the
                                rent, take this into account in the calculation.
                            </li>
                        </ol>
                    </div>

                    {/* Button */}
                    <div className="flex justify-center relative left-18 mt-4">
                        <button className="px-8 text-teal-600 py-2 border-2 border-gray-400 rounded-md bg-white hover:bg-gray-100 transition">
                            More rental tips
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile & Tablet Layout (md and below) - Stacked */}
            <div className="lg:hidden mb-16">
                {/* Image */}
                <div className="w-full mb-6">
                    <Image
                        src="/assets/property/7.svg"
                        alt="Couple Renting"
                        width={600}
                        height={400}
                        className="rounded-lg object-cover w-full h-auto"
                    />
                </div>

                {/* Tips Box - Stacked below image */}
                <div className="w-full">
                    <div className="bg-gray-100 py-8 px-6 rounded-lg shadow-md">
                        <ol className="list-decimal list-outside ml-5 text-gray-700 text-base space-y-2">
                            <li>
                                Write a lease with a notice period. Use{" "}
                                <span className="text-blue-600 cursor-pointer underline">
                                    FINN's rental contract
                                </span>{" "}
                                completely free of charge.
                            </li>
                            <li>
                                Make sure you have a deposit in your own account in your name
                                (deposit account).
                            </li>
                            <li>
                                Document any errors or defects in the home upon moving in.
                            </li>
                            <li>
                                Report any repairs to the landlord. It is not your responsibility!
                            </li>
                            <li>
                                Remember that the electricity bill is often not included in the
                                rent, take this into account in the calculation.
                            </li>
                        </ol>
                    </div>

                    {/* Button */}
                    <div className="flex justify-center mt-4">
                        <button className="px-8 text-teal-600 py-2 border-2 border-gray-400 rounded-md bg-white hover:bg-gray-100 transition">
                            More rental tips
                        </button>
                    </div>
                </div>
            </div>

            <div className="mt-10 flex flex-col md:flex-row items-center justify-between gap-8">
                {/* Text Content (Left Side) */}
                <div className="w-full md:w-2/3">
                    <h3 className="text-2xl font-bold text-gray-900">Rent out housing?</h3>
                    <p className="text-gray-600 mt-2 leading-relaxed">
                        Renting out is a great way to make a little extra money. However,
                        there are a{" "}
                        <span className="text-blue-600 cursor-pointer underline">
                            few things you should keep in mind
                        </span>{" "}
                        if you are considering renting. The lease is particularly important!
                        To make the process as simple as possible, FINN has drawn up a{" "}
                        <span className="text-blue-600 cursor-pointer underline">
                            lease
                        </span>{" "}
                        in collaboration with the Consumer Council, which ensures the rights
                        of both the landlord and the tenant.
                    </p>

                    {/* Buttons */}
                    <div className="flex flex-wrap sm:flex-nowrap gap-4 mt-4">
                        <button className="px-4 py-2 bg-teal-600 text-white font-semibold rounded-md hover:bg-teal-700 transition">
                            + New rental ad
                        </button>
                        <button className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-200 transition">
                            Lease contract
                        </button>
                    </div>
                </div>

                {/* Notepad Image (Right Side) */}
                <div className="w-full md:w-1/3 flex justify-end">
                    <Image
                        src="/assets/property/8.svg"
                        alt="Notepad"
                        width={230}
                        height={230}
                        className="object-contain"
                    />
                </div>
            </div>

        </div>
    );
};

export default RentingTips;