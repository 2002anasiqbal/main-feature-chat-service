"use client";
import React, { useState } from "react";

const OnlineCarRegForm = () => {
    const [formData, setFormData] = useState({
        name: "",
        mobile: "+92",
        email: "",
        postalCode: "",
        acceptTerms: false,
        subscribeNewsletter: false,
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
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
        <div className="mx-auto p-6 border border-gray-300 rounded-lg shadow-md bg-white">
            {/* Title */}
            <h2 className="text-xl font-semibold text-center text-gray-900 mb-4">
                Complete the registration and get a price estimate for your car
            </h2>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4 ">
                {/* Name */}
                <div className="w-2/3 mx-auto space-y-4">
                    <div>
                        <label className="pb-2 block text-lg text-gray-700">Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleChange}
                            placeholder="name"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 focus:ring focus:ring-teal-300"
                            required
                        />
                    </div>

                    {/* Mobile No */}
                    <div>
                        <label className="pb-2 block text-lg text-gray-700">Mobile No</label>
                        <input
                            type="text"
                            name="mobile"
                            value={formData.mobile}
                            onChange={handleChange}
                            placeholder="+92"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 focus:ring focus:ring-teal-300"
                            required
                        />
                    </div>

                    {/* Email */}
                    <div>
                        <label className="pb-2 block text-lg text-gray-700">Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            placeholder="email"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 focus:ring focus:ring-teal-300"
                            required
                        />
                    </div>

                    {/* Postal Code */}
                    <div>
                        <label className="pb-2 block text-lg text-gray-700">Postal code</label>
                        <input
                            type="text"
                            name="postalCode"
                            value={formData.postalCode}
                            onChange={handleChange}
                            placeholder="3430"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-gray-900 focus:ring focus:ring-teal-300"
                            required
                        />
                    </div>
                </div>

                {/* Checkboxes */}
                <div className="flex items-center justify-center space-x-2 mt-2">
                    <input
                        type="checkbox"
                        name="acceptTerms"
                        checked={formData.acceptTerms}
                        onChange={handleChange}
                        className="text-teal-600 focus:ring focus:ring-teal-300"
                        required
                    />
                    <label className="pb-2 text-lg text-gray-700">
                        Accept <a href="#" className="text-teal-600 underline">the terms</a> and that Nettbil can contact me regarding the sale of my car.
                    </label>
                </div>

                <div className="flex items-center justify-center space-x-2">
                    <input
                        type="checkbox"
                        name="subscribeNewsletter"
                        checked={formData.subscribeNewsletter}
                        onChange={handleChange}
                        className="text-teal-600 focus:ring focus:ring-teal-300"
                    />
                    <label className="pb-2 text-lg text-gray-700">
                        Yes, I would like to subscribe to Nettbil's newsletter.
                    </label>
                </div>

                {/* Submit Button */}
                <div className="flex justify-center">
                    <button
                        type="submit"
                        className="w-36 h-16 py-2 mt-4 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all"
                    >
                        Continue
                    </button>
                </div>
            </form>
        </div>
    );
};

export default OnlineCarRegForm;