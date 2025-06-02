"use client";
import React, { useState } from "react";
import ContactCard from "./ContactCard";
import ButtonCard from "../general/ButtonCard";

const PropertyDetails = () => {
    const [showMore, setShowMore] = useState(false);
    const [showCompleteStatement, setShowCompleteStatement] = useState(false);

    return (
        <div className="bg-white">
            <div className="bg-white w-full max-w-6xl mx-auto px-4 md:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                    {/* LEFT SECTION - Property Details */}
                    <div className="lg:col-span-2">
                        {/* Title & Price */}
                        <h1 className="text-3xl font-bold text-gray-900">RURAL & LARGE PROPERTY</h1>
                        <p className="text-xl text-teal-600 font-semibold mt-2">$149.99</p>
                        <p className="text-gray-800 mt-2">
                            The gently curved lines accentuated by sewn details are kind to your body and pleasant to look at.
                        </p>

                        {/* Key Info */}
                        <h2 className="text-2xl font-bold mt-6 text-gray-900">Key info</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-800 mt-2">
                            <p><strong>Housing type:</strong> Detached house</p>
                            <p><strong>Use area:</strong> 192 m²</p>
                            <p><strong>Bedroom:</strong> 3</p>
                            <p><strong>Room:</strong> 4</p>
                            <p><strong>Form of ownership:</strong> Owner (Owned)</p>
                            <p><strong>Plot area:</strong> 6,273 m²</p>
                        </div>

                        {/* Expandable Section */}
                        {showMore && (
                            <p className="text-gray-800 mt-2">
                                ✅ Large garden space with ample parking<br />
                                ✅ Close to public transport & shopping areas<br />
                                ✅ Recently renovated kitchen with modern appliances<br />
                                ✅ Energy-efficient heating system
                            </p>
                        )}
                        <button
                            onClick={() => setShowMore(!showMore)}
                            className="mt-3 px-6 py-2 border border-gray-700 text-gray-800 rounded-md font-semibold hover:bg-gray-100 transition-all"
                        >
                            {showMore ? "See Less" : "See More"}
                        </button>

                        {/* Facilities */}
                        <h2 className="text-2xl font-bold mt-6 text-gray-900">Facilities</h2>
                        <ul className="list-disc list-inside text-gray-800 mt-2">
                            <li>Unfurnished</li>
                            <li>Balcony/Terrace</li>
                            <li>Central</li>
                            <li>Hiking terrain</li>
                            <li>Fireplace/Fireplace</li>
                        </ul>

                        {/* About Home - Expandable */}
                        <h2 className="text-2xl font-bold mt-6 text-gray-900">About Home</h2>
                        <p className="text-gray-800 mt-2">
                            Apartment for rent on a small farm. Centrally located by Anfossen with REMA 1000, ElkJøp, Bohus, Monter.
                            100m away from bus transport, 2.5Km to Brandbu. 2.5Km to Jaren railway station. Prepared lawn.
                        </p>

                        {showCompleteStatement && (
                            <p className="text-gray-800 mt-2">
                                🏡 The home has an open living concept with a spacious kitchen, smart storage, and eco-friendly materials.
                                <br />🚗 Parking space for up to 3 cars.<br />
                                🌱 Energy-saving technology installed.<br />
                                📜 Fully compliant with local housing regulations.
                            </p>
                        )}

                        <button
                            onClick={() => setShowCompleteStatement(!showCompleteStatement)}
                            className="mt-3 px-6 py-2 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all"
                        >
                            {showCompleteStatement ? "Hide Statement" : "View Complete Statement"}
                        </button>
                    </div>

                    {/* RIGHT SECTION - Contact & Button Cards */}
                    <div className="sm:relative top-44">
                        <div className="space-y-6">
                            {/* Contact Card */}
                            <ContactCard
                                profileImage="https://picsum.photos/80?random"
                                name="Tor Anders"
                                description="Verified with BankID\nOn FINN since 2007"
                                buttonLabel="Send Message"
                                onButtonClick={() => alert("Message Sent!")}
                            />

                            {/* Button Card */}
                            <ButtonCard
                                title="Do you need a contract?"
                                description="• Completed contract with advertisement info\n• Digital signing\n• Free service\n• Approved by Consumer Council"
                                buttonText="Compare Favourite Homes"
                                onClick={() => alert("Comparing homes...")}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PropertyDetails;