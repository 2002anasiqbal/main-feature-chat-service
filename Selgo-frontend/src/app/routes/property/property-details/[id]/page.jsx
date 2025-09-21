// Selgo-frontend/src/app/routes/property/property-details/[id]/page.jsx (NEW)
"use client";
import React, { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import LocationMap from "@/components/general/LocationMap";
import PropertyDetails from "@/components/property/PropertyDetails";
import PropertySlider from "@/components/property/PropertySlider";
import propertyService from "@/services/propertyService";

export default function PropertyDetailsPage() {
    const params = useParams();
    const [property, setProperty] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchPropertyDetails = async () => {
            try {
                if (!params.id) {
                    setError("Property ID is required");
                    return;
                }

                const propertyData = await propertyService.getPropertyById(params.id);
                setProperty(propertyData);
            } catch (error) {
                console.error('Failed to fetch property details:', error);
                setError("Failed to load property details");
            } finally {
                setLoading(false);
            }
        };

        fetchPropertyDetails();
    }, [params.id]);

    if (loading) {
        return (
            <div className="bg-white">
                <div className="text-center py-20">Loading property details...</div>
            </div>
        );
    }

    if (error || !property) {
        return (
            <div className="bg-white">
                <div className="text-center py-20 text-red-500">
                    {error || "Property not found"}
                </div>
            </div>
        );
    }

    // Extract images for slider
    const propertyImages = property.images && property.images.length > 0 
        ? property.images.map(img => img.image_url)
        : ["https://picsum.photos/800/500?random=1"];

    return (
        <div className="bg-white">
            <PropertySlider 
                images={propertyImages}
                returnUrl="/routes/property/purchase"
            />
            <PropertyDetails property={property} />
            <LocationMap 
                heading="Property Location"
                latitude={property.latitude || 59.9139}
                longitude={property.longitude || 10.7522}
                locationName={`${property.city || 'Unknown'}, ${property.country || 'Norway'}`}
            />
        </div>
    );
}