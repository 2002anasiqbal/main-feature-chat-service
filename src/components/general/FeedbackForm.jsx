"use client";
import React, { useState } from "react";

const FeedbackForm = ({ onSubmit }) => {
    const [feedback, setFeedback] = useState("");

    // Handle Input Change
    const handleChange = (e) => {
        setFeedback(e.target.value);
    };

    // Handle Form Submission
    const handleSubmit = (e) => {
        e.preventDefault();
        if (feedback.trim() === "") return;

        onSubmit(feedback); // ✅ Call function from props

        setFeedback(""); // Reset input
    };

    return (
        <div className="w-full max-w-lg mx-auto py-6">
            <h2 className="text-lg font-light text-gray-800 mb-2">
                Give us feedback in the form below!
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Feedback Input */}
                <input
                    type="text"
                    placeholder="Feedback"
                    value={feedback}
                    onChange={handleChange}
                    className="w-full text-gray-500 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
                />

                {/* Send Button */}
                <button
                    type="submit"
                    className="px-6 py-2 bg-teal-500 text-white font-semibold rounded-md hover:bg-teal-800 transition"
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default FeedbackForm;