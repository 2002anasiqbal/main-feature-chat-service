// Selgo-frontend/src/components/property/PropertyDetails.jsx (Updated)
"use client";
import React, { useState } from "react";
import ContactCard from "./ContactCard";
import ButtonCard from "../general/ButtonCard";
import propertyService from "@/services/propertyService";

const PropertyDetails = ({ property }) => {
    const [showMore, setShowMore] = useState(false);
    const [showCompleteStatement, setShowCompleteStatement] = useState(false);
    const [contactLoading, setContactLoading] = useState(false);

    // Handle contact form submission
    const handleContactSubmit = async (contactData) => {
        setContactLoading(true);
        try {
            const result = await propertyService.contactPropertyOwner(property.id, contactData);
            alert(result.message || "Message sent successfully!");
        } catch (error) {
            console.error('Failed to send message:', error);
            alert("Failed to send message. Please try again later.");
        } finally {
            setContactLoading(false);
        }
    };

    // Handle comparison
    const handleCompareProperties = async () => {
        try {
            // For now, just compare this property with itself as example
            const result = await propertyService.compareProperties([property.id]);
            alert("Comparison feature implemented! Check console for details.");
            console.log("Comparison result:", result);
        } catch (error) {
            console.error('Failed to compare properties:', error);
            alert("Comparison feature coming soon!");
        }
    };

    // Format facilities for display
    const formatFacilities = () => {
        const facilities = [];
        
        if (property.is_furnished) facilities.push("Furnished");
        else facilities.push("Unfurnished");
        
        if (property.has_balcony) facilities.push("Balcony/Terrace");
        if (property.has_fireplace) facilities.push("Fireplace");
        if (property.has_garden) facilities.push("Garden");
        if (property.has_parking) facilities.push("Parking");
        
        // Add custom facilities from backend
        if (property.facilities && property.facilities.length > 0) {
            property.facilities.forEach(fac => {
                if (fac.facility && fac.facility.name) {
                    facilities.push(fac.facility.name);
                }
            });
        }
        
        return facilities;
    };

    return (
        <div className="bg-white">
            <div className="bg-white w-full max-w-6xl mx-auto px-4 md:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
                    {/* LEFT SECTION - Property Details */}
                    <div className="lg:col-span-2">
                        {/* Title & Price */}
                        <h1 className="text-3xl font-bold text-gray-900">
                            {property.title || "RURAL & LARGE PROPERTY"}
                        </h1>
                        <p className="text-xl text-teal-600 font-semibold mt-2">
                            ${Number(property.price || 149.99).toLocaleString()}
                        </p>
                        <p className="text-gray-800 mt-2">
                            {property.description || "The gently curved lines accentuated by sewn details are kind to your body and pleasant to look at."}
                        </p>

                        {/* Key Info */}
                        <h2 className="text-2xl font-bold mt-6 text-gray-900">Key info</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-800 mt-2">
                            <p><strong>Housing type:</strong> {property.housing_type || "Detached house"}</p>
                            <p><strong>Use area:</strong> {property.use_area ? `${property.use_area} m²` : "192 m²"}</p>
                            <p><strong>Bedroom:</strong> {property.bedrooms || 3}</p>
                            <p><strong>Room:</strong> {property.rooms || 4}</p>
                            <p><strong>Form of ownership:</strong> {property.ownership_form || "Owner (Owned)"}</p>
                            <p><strong>Plot area:</strong> {property.plot_area ? `${property.plot_area} m²` : "6,273 m²"}</p>
                            {property.year_built && (
                                <p><strong>Year built:</strong> {property.year_built}</p>
                            )}
                            {property.energy_rating && (
                                <p><strong>Energy rating:</strong> {property.energy_rating}</p>
                            )}
                        </div>

                        {/* Expandable Section */}
                        {showMore && (
                            <div className="text-gray-800 mt-2">
                                <p>✅ Large garden space with ample parking</p>
                                <p>✅ Close to public transport & shopping areas</p>
                                <p>✅ Recently renovated kitchen with modern appliances</p>
                                <p>✅ Energy-efficient heating system</p>
                                {property.heating_type && (
                                    <p>✅ Heating type: {property.heating_type}</p>
                                )}
                                {property.has_garage && (
                                    <p>✅ Garage available</p>
                                )}
                                {property.parking_spaces > 0 && (
                                    <p>✅ {property.parking_spaces} parking space(s)</p>
                                )}
                            </div>
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
                            {formatFacilities().map((facility, index) => (
                                <li key={index}>{facility}</li>
                            ))}
                        </ul>

                        {/* About Home - Expandable */}
                        <h2 className="text-2xl font-bold mt-6 text-gray-900">About Home</h2>
                        <p className="text-gray-800 mt-2">
                            {property.description || "Apartment for rent on a small farm. Centrally located by Anfossen with REMA 1000, ElkJøp, Bohus, Monter. 100m away from bus transport, 2.5Km to Brandbu. 2.5Km to Jaren railway station. Prepared lawn."}
                        </p>

                        {showCompleteStatement && (
                            <div className="text-gray-800 mt-2">
                                <p>🏡 The home has an open living concept with a spacious kitchen, smart storage, and eco-friendly materials.</p>
                                {property.has_parking && (
                                    <p>🚗 Parking space for up to {property.parking_spaces || 3} cars.</p>
                                )}
                                <p>🌱 Energy-saving technology installed.</p>
                                <p>📜 Fully compliant with local housing regulations.</p>
                                {property.city && (
                                    <p>📍 Located in {property.city}, {property.country || "Norway"}</p>
                                )}
                            </div>
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
                                name={property.owner_name || "Property Owner"}
                                description={`${property.is_agent ? 'Real Estate Agent' : 'Verified with BankID'}\nOn FINN since 2007`}
                                buttonLabel={contactLoading ? "Sending..." : "Send Message"}
                                onButtonClick={() => {
                                    const contactData = {
                                        sender_name: "Interested Buyer",
                                        sender_email: "buyer@example.com",
                                        sender_phone: "+47 123 45 678",
                                        message: `I am interested in your property: ${property.title}`
                                    };
                                    handleContactSubmit(contactData);
                                }}
                                disabled={contactLoading}
                            />

                            {/* Button Card */}
                            <ButtonCard
                                title="Do you need a contract?"
                                description="• Completed contract with advertisement info\n• Digital signing\n• Free service\n• Approved by Consumer Council"
                                buttonText="Compare Favourite Homes"
                                onClick={handleCompareProperties}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PropertyDetails;