"use client";
import React from "react";
import { CiSearch } from "react-icons/ci";

export default function SearchBar({ 
  placeholder = "Search...", 
  value = "", 
  onChange, 
  className = "" 
}) {
  return (
    <div className={`flex bg-white gap-3 items-center border border-gray-300 rounded-md px-4 py-2 shadow-sm focus-within:border-teal-500 focus-within:ring-1 focus-within:ring-teal-500 w-full ${className}`}>
      <CiSearch className="text-teal-600 text-xl mr-2" />
      <input
        type="text"
        className="w-full outline-none bg-transparent text-gray-700 placeholder-gray-400"
        placeholder={placeholder}
        value={value}
        onChange={onChange}
      />
      <button 
        type="submit" 
        className="bg-teal-600 hover:bg-teal-700 text-white font-medium rounded-md text-sm px-4 py-1"
      >
        Search
      </button>
    </div>
  );
}