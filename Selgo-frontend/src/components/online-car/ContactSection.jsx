"use client";
import React from "react";
import Image from "next/image";

const teamMembers = [
  {
    name: "Harry",
    email: "xyz@gmail.com",
    phone: "33401 111111",
    image: "/assets/online-car/9.svg",
  },
  {
    name: "Harry",
    email: "xyz@gmail.com",
    phone: "33401 111111",
    image: "/assets/online-car/9.svg",
  },
];

const ContactSection = () => {
  return (
    <div className="w-full max-w-lg mx-auto p-5 text-center">
      {/* CTA Button */}
      <button className="w-2/3 py-3 bg-teal-600 text-white font-semibold rounded-md hover:bg-teal-700 transition-all">
        Create a free account to see all cars
      </button>

      {/* Info Text */}
      <p className="text-gray-600 mt-2">
        Requires second-hand trade license and access to autosys
      </p>

      {/* Contact Header */}
      <h2 className="text-xl font-semibold text-gray-900 mt-6">Question? Contact us</h2>

      {/* Contact Cards */}
      <div className="grid text-gray-800 grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
        {teamMembers.map((member, index) => (
          <div
            key={index}
            className="border border-gray-200 rounded-md p-4 shadow-sm flex flex-col items-center text-center"
          >
            <h3 className="text-lg font-medium">{member.name}</h3>
            <Image
              src={member.image}
              alt={member.name}
              width={50}
              height={50}
              className="rounded-full mt-2"
            />
            <p className="text-sm text-gray-600 mt-2">{member.email}</p>
            <p className="text-sm text-gray-600">{member.phone}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ContactSection;