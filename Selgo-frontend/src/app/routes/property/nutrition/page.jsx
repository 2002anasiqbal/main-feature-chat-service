// Selgo-frontend/src/app/routes/property/nutrition/page.jsx (Updated)
"use client";
import React, { useState, useEffect } from "react";
import GenericCardCollection from "@/components/GenericCardCollection";
import propertyService from "@/services/propertyService";

export default function NutritionPage() {
    const [nutritionCategories, setNutritionCategories] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchNutritionCategories = async () => {
            try {
                const categories = await propertyService.getPropertyCategories('nutrition');
                
                // If no nutrition categories from backend, use default property categories
                if (categories.length === 0) {
                    setNutritionCategories([
                        { tag: "Plots", icon: "1.svg", route: "/plots" },
                        { tag: "Residence Abroad", icon: "2.svg", route: "/residence-abroad" },
                        { tag: "Housing for Sale", icon: "3.svg", route: "/housing-sale" },
                        { tag: "New Homes", icon: "4.svg", route: "/new-homes" },
                        { tag: "Vacation Homes", icon: "5.svg", route: "/vacation-homes" },
                        { tag: "Leisure Plots", icon: "6.svg", route: "/leisure-plots" },
                    ]);
                } else {
                    // Transform backend categories to expected format
                    const transformedCategories = categories.map(cat => ({
                        tag: cat.label,
                        icon: cat.icon || "1.svg",
                        route: cat.route || `/nutrition/${cat.label.toLowerCase().replace(/\s+/g, '-')}`
                    }));
                    setNutritionCategories(transformedCategories);
                }
            } catch (error) {
                console.error('Failed to fetch nutrition categories:', error);
                // Fallback to default categories
                setNutritionCategories([
                    { tag: "Plots", icon: "1.svg", route: "/plots" },
                    { tag: "Residence Abroad", icon: "2.svg", route: "/residence-abroad" },
                    { tag: "Housing for Sale", icon: "3.svg", route: "/housing-sale" },
                    { tag: "New Homes", icon: "4.svg", route: "/new-homes" },
                    { tag: "Vacation Homes", icon: "5.svg", route: "/vacation-homes" },
                    { tag: "Leisure Plots", icon: "6.svg", route: "/leisure-plots" },
                ]);
            } finally {
                setLoading(false);
            }
        };

        fetchNutritionCategories();
    }, []);

    if (loading) {
        return (
            <div>
                <div className="text-center py-20">Loading nutrition categories...</div>
            </div>
        );
    }

    return (
        <div>
            <div className="relative -top-10">
                <GenericCardCollection
                    rows={[{ items: nutritionCategories }]}
                    imageBasePath="/assets/property/"
                    containerStyles={{ container: "mt-6" }}
                    rowStyles={{
                        0: { gridCols: "grid-cols-2 sm:grid-cols-3 md:grid-cols-6", centered: true },
                    }}
                />
            </div>
        </div>
    );
}