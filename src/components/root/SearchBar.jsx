"use client";
import { CiSearch } from "react-icons/ci";
import React from "react";

const SearchBar = ({ placeholder, onChange }) => {
  return (
    <div className="flex bg-white gap-3 items-center border border-gray-300 rounded-md px-4 py-2 shadow-sm focus-within:border-teal-500 focus-within:ring-1 focus-within:ring-teal-500 w-full">
      <CiSearch className="text-teal-600 text-xl mr-2" />
      <input
        type="text"
        className="w-full outline-none bg-transparent text-gray-700 placeholder-gray-400"
        placeholder={placeholder || "Search..."}
        onChange={onChange}
      />
    </div>
  );
};

export default SearchBar;