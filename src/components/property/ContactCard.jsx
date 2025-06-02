"use client";
import React from "react";
import Image from "next/image";

const ContactCard = ({
    profileImage = "https://picsum.photos/80?random", // Default placeholder
    name = "John Doe",
    description = "Verified with BankID\nOn FINN since 2007",
    buttonLabel = "Send Message",
    onButtonClick = () => alert("Message Sent!"),
}) => {
    return (
        <div className="bg-white border border-gray-300 rounded-lg p-6 shadow-md w-full max-w-xs text-center">
            {/* Profile Image */}

            <div className="flex justify-center gap-10 space-y-5 ">
                <Image
                    src={profileImage}
                    alt={name}
                    width={80}
                    height={80}
                    className="rounded-full"
                />

                <div>

                    {/* Name */}
                    <h2 className="text-gray-900 text-lg font-semibold">{name}</h2>

                    {/* Description */}
                    <p className="text-gray-600 text-sm mt-1 whitespace-pre-line">
                        {description}
                    </p>
                </div>
            </div>

            {/* Button */}
            <button
                className="mt-4 h-15 px-5 py-2 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all w-full"
                onClick={onButtonClick}
            >
                {buttonLabel}
            </button>
        </div>
    );
};

export default ContactCard;