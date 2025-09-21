"use client";
import React, { useState } from "react";
import { IoIosArrowDown } from "react-icons/io";
const faqsData = [
    {
      question: "What is the difference between car sales through Nettbil and Selgo?",
      answer: "Nettbil focuses on auctions, while Selgo offers direct sales with flexible pricing.",
    },
    {
      question: "How soon do I have to decide if I want to sell?",
      answer: "You usually have up to 7 days to make a final decision after receiving an offer.",
    },
    {
      question: "How does Selgo ensure secure transactions?",
      answer: "Selgo partners with verified buyers and uses escrow services to ensure secure transactions.",
    },
  ];

const FAQ = ({ faqs = faqsData }) => {
  const [openIndex, setOpenIndex] = useState(null);

  const toggleFAQ = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="w-full">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">Frequently Asked Questions</h2>
      <div className="space-y-2">
        {faqs.map((faq, index) => (
          <div key={index} className="border rounded-md">
            <button
              className="flex justify-between items-center w-full p-4 text-left text-gray-800 font-medium hover:bg-gray-100"
              onClick={() => toggleFAQ(index)}
            >
              {faq.question}
              <IoIosArrowDown
                className={`transition-transform duration-300 ${
                  openIndex === index ? "rotate-180" : ""
                }`}
              />
            </button>
            {openIndex === index && (
              <div className="p-4 text-gray-600 border-t bg-gray-50">{faq.answer}</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default FAQ;