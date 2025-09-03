// Selgo-frontend/src/app/routes/property/purchase/page.jsx (Updated)
"use client";
import React, { useState, useEffect } from "react";
import GenericCardCollection from "@/components/GenericCardCollection";
import RecentlyVisitedSlider from "@/components/general/RecentlyVisitedSlider";
import Page from "@/components/GenerateCard";
import Purchase from "@/components/property/Purchase";
import propertyService from "@/services/propertyService";

export default function PurchasePage() {
    const [featuredProperties, setFeaturedProperties] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFeaturedProperties = async () => {
            try {
                const properties = await propertyService.getRecommendedProperties('purchase', 3);
                setFeaturedProperties(properties);
            } catch (error) {
                console.error('Failed to fetch featured properties:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchFeaturedProperties();
    }, []);

    return (
        <div className="bg-white w-full">
            <Purchase />
            <RecentlyVisitedSlider />
            <h1 className="font-bold text-3xl text-gray-800">We think you might like these</h1>
            {loading ? (
                <div className="text-center py-10">Loading featured properties...</div>
            ) : (
                <Page 
                    columns={3} 
                    route="/routes/property/property-details"
                    cards={featuredProperties}
                    disableAutoFetch={true}
                />
            )}
        </div>
    );
}