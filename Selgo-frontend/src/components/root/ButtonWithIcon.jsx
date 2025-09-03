"use client";
import React from "react";

const ButtonWithIcon = ({ icon: Icon = null, label, onClick }) => {
  return (
    <button
      onClick={onClick} // Call the onClick function directly
      className="flex bg-white items-center gap-2 px-4 py-2 border border-gray-300 rounded-md shadow-sm hover:shadow-md transition-all text-gray-700 hover:bg-gray-100 cursor-pointer"
    >
      {Icon && <Icon className="text-teal-600 text-xl" />}
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
};

export default ButtonWithIcon;
