// Selgo-frontend/src/app/routes/property/rent/page.jsx (Updated)
"use client";
import React, { useState, useEffect } from "react";
import Page from "@/components/GenerateCard";
import PopularCitiesGrid from "@/components/property/PopularCitiesGrid";
import RentingTips from "@/components/property/RentingTips";
import propertyService from "@/services/propertyService";

export default function RentPage() {
    const [popularCities, setPopularCities] = useState([]);
    const [rentalTips, setRentalTips] = useState([]);
    const [rentalProperties, setRentalProperties] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Fetch all required data
                const [cities, tips, properties] = await Promise.all([
                    propertyService.getPopularCities(),
                    propertyService.getRentalTips(),
                    propertyService.getRecommendedProperties('rent', 3)
                ]);

                setPopularCities(cities);
                setRentalTips(tips);
                setRentalProperties(properties);
            } catch (error) {
                console.error('Failed to fetch rental data:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="bg-white">
                <div className="text-center py-20">Loading rental information...</div>
            </div>
        );
    }

    return (
        <div className="bg-white">
            <PopularCitiesGrid cities={popularCities} />
            <RentingTips tips={rentalTips} />
            <h1 className="font-bold text-3xl text-gray-800">Popular Cities to Rent In</h1>
            <Page 
                columns={3} 
                route="/routes/property/property-details" 
                cards={rentalProperties}
                disableAutoFetch={true}
            />
        </div>
    );
}