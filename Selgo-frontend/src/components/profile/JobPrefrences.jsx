"use client";
import { useState } from "react";

export default function JobPreferences() {
  const [jobTitle, setJobTitle] = useState("");
  const [location, setLocation] = useState("");

  return (
    <div className="py-6 bg-white space-y-4">
      {/* Heading */}
      <h2 className="text-2xl font-semibold text-gray-900">My job preferences</h2>

      {/* Subtitle */}
      <p className="mt-2 font-semibold text-gray-800">What is your dream job?</p>
      <p className="text-gray-700">
        We want to help you find your dream job, so that you don’t have to actively look for it yourself.
        Recommendations we give you are based on{" "}
        <a href="#" className="text-teal-500 underline">companies you follow</a> and your job preferences.
      </p>
      <p className="mt-2 italic text-gray-600">
        Here you can change your settings. You may want to update or add new information periodically 
        so that what you receive will always be relevant and interesting.
      </p>

      {/* Job Title Input */}
      <div className="mt-6">
        <label className="block text-gray-800 font-medium">What do you want to work on?</label>
        <input
          type="text"
          value={jobTitle}
          onChange={(e) => setJobTitle(e.target.value)}
          placeholder="Job title"
          className="mt-2 w-full p-3 text-gray-500 border rounded-md bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
        />
      </div>

      {/* Location Input */}
      <div className="mt-4">
        <label className="block text-gray-800 font-medium">Where do you want to work?</label>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Location"
          className="mt-2 w-full p-3 text-gray-500 border rounded-md bg-gray-100 focus:outline-none focus:ring-2 focus:ring-teal-500"
        />
      </div>
    </div>
  );
}