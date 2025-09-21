"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Property() {
    const router = useRouter();

    useEffect(() => {
        router.replace("/routes/property/purchase"); // ✅ Automatically redirects to Purchase
    }, []);

    return null; // Don't render anything, just redirect
}
