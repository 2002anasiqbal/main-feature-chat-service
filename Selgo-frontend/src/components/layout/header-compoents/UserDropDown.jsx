"use client";
import { useState, useEffect } from "react";
import Image from "next/image";

const UserDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isOpen && !event.target.closest("#user-menu")) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="relative">
      {/* User Icon */}
      <button onClick={() => setIsOpen(!isOpen)}>
        <Image src="/assets/header/user-circle.svg" alt="User" width={32} height={32} />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div
          id="user-menu"
          className="absolute right-0 mt-2 w-40 bg-white shadow-lg rounded-lg p-2"
        >
          <ul className="text-gray-900 text-sm">
            <li className="p-2 hover:bg-gray-100 cursor-pointer">Sign In</li>
            <li className="p-2 hover:bg-gray-100 cursor-pointer">Sign Up</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default UserDropdown;
