"use client";
import GenericCardCollection from "../GenericCardCollection";

export default function JobUniverseSection() {
    const imageBasePath = "/assets/profile/"; // Update if needed

    const rows = [
        {
            items: [
                { tag: "Job Profile", description: "see details", icon: "User.svg", route: "/jobs/profile" },
                { tag: "Application History", description: "see details", icon: "User.svg", route: "/jobs/history" },
                { tag: "Job Preference", description: "see details", icon: "User.svg", route: "/jobs/preference" },
                { tag: "Companies I follow", description: "see details", icon: "User.svg", route: "/jobs/companies" },
            ],
        },
    ];

    const rowStyles = {
        0: {
            gridCols: "grid-cols-1 sm:grid-cols-2 md:grid-cols-4", // Responsive layout
            gap: "gap-6",
            centered: true,
        },
    };

    return (
        <div className="w-full ">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Job Universe</h2>
            <GenericCardCollection 
                rows={rows} 
                imageBasePath={imageBasePath} 
                size="w-48 h-48" 
                rowStyles={rowStyles} 
                showDetails={true}
            />
        </div>
    );
}
