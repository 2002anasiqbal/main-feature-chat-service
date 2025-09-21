"use client";
import { useRouter } from "next/navigation";
import React, { useState } from "react";

export default function ContactUs() {
  const router = useRouter();

  // State for form inputs
  const [formData, setFormData] = useState({
    message: "",
    phone: "",
  });

  // Handle input changes
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Go back function
  const handleBack = () => {
    router.back(); // Navigates to the previous page
  };

  return (
    <div className=" py-10">
      {/* Back Button */}
      <button onClick={handleBack} className="text-gray-900 flex items-center mb-6 hover:underline">
        ← Back
      </button>

      {/* Page Title */}
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact us</h2>

      {/* Message Input */}
      <div className="mb-4">
        <label className="block text-gray-700 text-sm font-medium">Message to the advertiser</label>
        <textarea
          name="message"
          value={formData.message}
          onChange={handleChange}
          placeholder="Message"
          className="w-full border border-gray-300 p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
          rows="3"
        ></textarea>
        <p className="text-xs text-gray-500 mt-1">We have the rights to check and stop messages</p>
      </div>

      {/* Phone Number Input */}
      <div className="mb-6">
        <label className="block text-gray-700 text-sm font-medium">Phone No</label>
        <input
          type="text"
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          placeholder="92"
          className="w-full border border-gray-300 p-3 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
        />
      </div>

      {/* Info Box */}
      <div className="bg-gray-100 p-4 rounded-md mb-6">
        <p className="text-sm text-gray-700">Message will be sent as an email to the advertiser</p>
        <p className="text-sm text-gray-700 mt-1">Email address</p>
        <p className="text-sm font-medium text-gray-900">xyz@gmail.com</p>
      </div>

      {/* Buttons */}
      <div className="flex gap-4">
        <button className="px-6 py-2 bg-teal-500 text-white font-semibold rounded-md hover:bg-teal-600 transition">
          Send message
        </button>
        <button className="px-6 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-100 transition">
          Cancel
        </button>
      </div>
    </div>
  );
}