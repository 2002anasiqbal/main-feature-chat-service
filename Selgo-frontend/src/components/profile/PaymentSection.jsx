"use client";
import GenericCardCollection from "../GenericCardCollection";
export default function PaymentsSection() {
    const imageBasePath = "/assets/profile/";

    const rows = [
        {
            items: [
                { tag: "Payment Information", description: "see details", icon: "2.svg", route: "/payments/info" },
                { tag: "Your Account", description: "see details", icon: "3.svg", route: "/payments/account" },
            ],
        },
    ];

    const rowStyles = {
        0: {
            gridCols: "grid-cols-1 sm:grid-cols-2", // Single column on mobile, two on larger screens
            gap: "gap-6",
            centered: true,
        },
    };

    return (
        <div className="w-full">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Payments</h2>
            <GenericCardCollection 
                rows={rows} 
                imageBasePath={imageBasePath} 
                size="w-64 h-36" 
                rowStyles={rowStyles} 
            />
        </div>
    );
}