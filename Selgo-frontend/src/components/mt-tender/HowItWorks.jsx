"use client";
import React from "react";

export default function HowItWorks() {
  const steps = [
    {
      icon: "11",
      title: "Describe the project",
      text: "After a short time, you will receive non-binding offers from up to five relevant companies.",
    },
    {
      icon: "12",
      title: "Receive offers",
      text: "Compare the offers you get. Feel free to ask follow-up questions directly to the professionals.",
    },
    {
      icon: "13",
      title: "Get started!",
      text: "Check the offers you have received. Then hire – the job is done, once you’ve chosen a professional!",
    },
  ];

  return (
    <section className="bg-white pb-10">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-8">
          This is how Mittanbud works
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col px-4">
              <div className="flex items-center gap-5">
                <img
                  src={`/assets/my-tender/${step.icon}.svg`}
                  alt={step.title}
                  className="mb-4 w-12 h-12"
                />
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {step.title}
                </h3>
              </div>
              <p className="text-gray-700">{step.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
