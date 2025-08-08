// Selgo-frontend/src/app/routes/property/sell/page.jsx (Updated)
"use client";
import React, { useState, useEffect } from "react";
import PriceGrid from "@/components/property/PriceGrid";
import LocationMap from "@/components/general/LocationMap";
import Image from "next/image";
import FeedbackForm from "@/components/general/FeedbackForm";
import propertyService from "@/services/propertyService";

export default function SellPage() {
    const [priceInsights, setPriceInsights] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPriceInsights = async () => {
            try {
                const insights = await propertyService.getPriceInsights();
                
                // Transform insights to match the expected format
                const transformedData = insights.map(insight => ({
                    title: insight.city,
                    value: `${insight.currency} ${Number(insight.avg_price_per_sqm).toLocaleString()}`,
                    description: insight.period_description
                }));

                setPriceInsights(transformedData);
            } catch (error) {
                console.error('Failed to fetch price insights:', error);
                // Fallback to static data if API fails
                setPriceInsights([
                    { title: "Bergen", value: "NOK 541235", description: "On average per advertisement in last 30 days" },
                    { title: "Oslo", value: "NOK 620000", description: "On average per advertisement in last 30 days" },
                    { title: "Stavanger", value: "NOK 495000", description: "On average per advertisement in last 30 days" },
                    { title: "Trondheim", value: "NOK 560000", description: "On average per advertisement in last 30 days" },
                    { title: "Drammen", value: "NOK 480000", description: "On average per advertisement in last 30 days" },
                    { title: "Kristiansand", value: "NOK 510000", description: "On average per advertisement in last 30 days" },
                ]);
            } finally {
                setLoading(false);
            }
        };

        fetchPriceInsights();
    }, []);

    // Handle feedback submission
    const handleFeedbackSubmit = async (message) => {
        try {
            const result = await propertyService.submitFeedback({
                message,
                page_url: window.location.href
            });
            
            console.log("Feedback submitted successfully:", result);
            alert("Thank you for your feedback!");
        } catch (error) {
            console.error("Failed to submit feedback:", error);
            alert("Failed to submit feedback. Please try again later.");
        }
    };

    return (
        <div>
            <LocationMap 
                heading="Check what price homes in your area have sold for"
                latitude={59.9139}
                longitude={10.7522}
                locationName="Norway"
            />
            <button className="block mx-auto bg-teal-600 hover:bg-teal-800 h-15 px-10 border rounded-lg text-white font-semibold">
                See Sale Price
            </button>
            
            <div className="bg-white">
                {loading ? (
                    <div className="text-center py-10">Loading price insights...</div>
                ) : (
                    <PriceGrid data={priceInsights} />
                )}
            </div>
            
            <div className="mt-10 flex flex-col md:flex-row items-center justify-between gap-8">
                {/* Text Content (Left Side) */}
                <div className="w-full md:w-2/3">
                    <h3 className="text-2xl font-bold text-gray-900">Are you going to sell a home?</h3>
                    <p className="text-gray-600 mt-2 leading-relaxed">
                        Selling a home can be both time-consuming, exciting and perhaps a little scary?<br/>
                        We have put together a number of tips and tricks that can be nice to think about when you are selling a property.
                    </p>

                    {/* Buttons */}
                    <div className="flex flex-wrap sm:flex-nowrap gap-4 mt-4">
                        <button className="px-10 py-2 bg-teal-600 text-white font-semibold rounded-md hover:bg-teal-700 transition">
                            Checkout tips and tricks here
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
            
            <h3 className="my-10 text-2xl font-bold text-gray-900">
                Are you wondering about something, or are you missing something on this page?
            </h3>            
            <FeedbackForm onSubmit={handleFeedbackSubmit} />
        </div>
    );
}