"use client"

import ProfileBar from "@/components/profile/ProfileBar";
import ProfileCards from "@/components/profile/ProfileCards";

export default function ProfilePage() {
    return (
        <div className="bg-white min-h-screen flex flex-col items-center py-10">
            {/* Profile Bar */}
            <div className="w-full mb-10">
                <ProfileBar />
            </div>
  
            {/* Profile Cards */}
            <div className="w-full">
                <ProfileCards />
            </div>
        </div>
    );
}