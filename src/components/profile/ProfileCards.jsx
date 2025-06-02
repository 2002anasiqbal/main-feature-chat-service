"use client";
import GenericCardCollection from "../GenericCardCollection";

export default function ProfileCards() {
    const imageBasePath = "/assets/profile/";
    const rows = [
        {
            items: [
                { tag: "My account", icon: "User.svg", route: "/routes/profile/my-accounts" },
                { tag: "Favorites", icon: "Heart.svg", route: "/routes/profile/favorites" },
                { tag: "My ads", icon: "Plus circle.svg", route: "/routes/profile/my-ads" },
                { tag: "Fix finished", icon: "Heart-1.svg", route: "/routes/profile/fix-finished" },
            ],
        },
        {
            items: [
                { tag: "Saved searches", icon: "Search.svg", route: "/routes/profile/saved-searches" },
                { tag: "Payments", icon: "Dollar sign.svg", route: "/routes/profile/payments" },
                { tag: "Job universe", icon: "Briefcase.svg", route: "/routes/profile/job-universe" },
                { tag: "Security", icon: "Heart-2.svg", route: "/routes/profile/security" },
            ],
        },
        {
            items: [
                { tag: "Privacy", icon: "Heart-3.svg", route: "/routes/profile/privacy" },
                { tag: "Notifications", icon: "Info.svg", route: "/routes/profile/notifications" },
                { tag: "For business", icon: "Slack.svg", route: "/routes/profile/for-business" },
                { tag: "Holiday Homes", icon: "Home.svg", route: "/routes/profile/holiday-homes" },
            ],
        },
    ];

    // Add rowStyles like in CarCaravanMain
    const rowStyles = {
        0: {
            gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", 
            gap: "gap-6",
            marginBottom: "mb-6",
            centered: true,
        },
        1: {
            gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", 
            gap: "gap-6",
            marginBottom: "mb-6",
            centered: true,
        },
        2: {
            gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4", 
            gap: "gap-6",
            centered: true,
        },
    };

    return (
        <div className="w-full">
            <GenericCardCollection 
                rows={rows} 
                imageBasePath={imageBasePath} 
                size="w-44 h-32" 
                rowStyles={rowStyles}
                showDetails={true} 
            />
        </div>
    );
}