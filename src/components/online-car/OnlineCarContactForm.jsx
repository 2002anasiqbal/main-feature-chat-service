"use client";
import React, { useState } from "react";
import Image from "next/image";

const OnlineCarContactForm = () => {
    const [formData, setFormData] = useState({
        name: "",
        phone: "",
        email: "",
        company: "",
        consent1: false,
        consent2: false,
    });

    const handleChange = (e) => {
        const { name, type, checked, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: type === "checkbox" ? checked : value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Form Submitted:", formData);
    };

    return (
        <div className="relative w-full h-screen">
            {/* Background Image */}
            <Image
                src="/assets/online-car/carBg.svg"
                alt="Car Background"
                layout="fill"
                objectFit="cover"
                className="absolute inset-0"
            />

            {/* Overlay Form Container */}
            <div className="absolute inset-0 flex items-center justify-center bg-black/60">
                <div className="w-full max-w-lg bg-black text-white p-8 rounded-lg shadow-lg">
                    {/* Title */}
                    <h2 className="text-2xl font-semibold text-center">Fill in your contact information</h2>
                    <p className="text-gray-300 text-center mt-1">
                        Fill in the form and one of our advisors will contact you shortly.
                    </p>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="mt-6 space-y-4">
                        <div className="w-2/3 space-y-4 mx-auto">
                            {/* Input Fields */}
                            <input
                                type="text"
                                name="name"
                                placeholder="Name"
                                value={formData.name}
                                onChange={handleChange}
                                className="w-full p-3 rounded-md text-black border border-gray-400 bg-white focus:ring focus:ring-teal-500"
                                required
                            />
                            <input
                                type="text"
                                name="phone"
                                placeholder="Phone No"
                                value={formData.phone}
                                onChange={handleChange}
                                className="w-full p-3 rounded-md text-black border border-gray-400 bg-white focus:ring focus:ring-teal-500"
                                required
                            />
                            <input
                                type="email"
                                name="email"
                                placeholder="Email"
                                value={formData.email}
                                onChange={handleChange}
                                className="w-full p-3 rounded-md text-black border border-gray-400 bg-white focus:ring focus:ring-teal-500"
                                required
                            />
                            <input
                                type="text"
                                name="company"
                                placeholder="Company"
                                value={formData.company}
                                onChange={handleChange}
                                className="w-full p-3 rounded-md text-black border border-gray-400 bg-white focus:ring focus:ring-teal-500"
                                required
                            />
                        </div>
                        {/* Consent Section */}
                        <p className="text-center text-gray-300 mt-4">We need your consent</p>

                        <div className="flex items-start space-x-2">
                            <input
                                type="checkbox"
                                name="consent1"
                                checked={formData.consent1}
                                onChange={handleChange}
                                className="mt-1"
                                required
                            />
                            <label className="text-sm text-gray-300">
                                I allow Nettbil AS to store and process my information and to contact me in connection with the sale of cars.
                            </label>
                        </div>

                        <div className="flex items-start space-x-2">
                            <input
                                type="checkbox"
                                name="consent2"
                                checked={formData.consent2}
                                onChange={handleChange}
                                className="mt-1"
                            />
                            <label className="text-sm text-gray-300">
                                I allow Nettbil AS to store and process my information and to contact me in connection with receiving information and news via email.
                            </label>
                        </div>

                        {/* Submit Button */}
                        <div className="flex justify-center mt-4">
                            <button
                                type="submit"
                                className="w-36 h-12 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all"
                            >
                                Contact Me
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default OnlineCarContactForm;
