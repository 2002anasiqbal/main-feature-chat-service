"use client";
import React from "react";
import { FaCalculator, FaSuitcase, FaTag } from "react-icons/fa";
import { FiChevronRight } from "react-icons/fi";

const cardData = [
  {
    title: "Currency calculator",
    description: "Find exchange rates",
    icon: <FaCalculator size={24} />,
    link: "#",
  },
  {
    title: "Package Tours",
    description: "Find cheap package holidays",
    icon: <FaSuitcase size={24} />,
    link: "#",
  },
  {
    title: "Remaining Places",
    description: "Find cheap remaining seats from all travel agencies.",
    icon: <FaTag size={24} />,
    link: "#",
  },
];

const InfoSection = () => {
  return (
    <div className="w-full py-10 mx-auto bg-teal-700 text-white p-6 rounded-lg">
      <div className="grid grid-cols-1 sm:grid-cols-3 sm:gap-20 md:gap-10 gap-5 text-left">
        {cardData.map((item, index) => (
          <a
            key={index}
            href={item.link}
            className="flex items-center sm:items-start space-x-4 hover:opacity-80 transition"
          >
            <div className="text-white">{item.icon}</div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold flex items-center justify-between">
                {item.title}
                <FiChevronRight className="text-white" />
              </h3>
              <p className="text-gray-200 text-sm">{item.description}</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default InfoSection;
