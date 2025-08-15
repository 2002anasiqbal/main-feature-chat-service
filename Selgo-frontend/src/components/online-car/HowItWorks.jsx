"use client";
import React from "react";
import OnlineCarSquare from "./OnlineCarSquare";

const steps = [
  {
    icon: "/assets/online-car/1.svg",
    title: "Tell us about your car",
    description: "We give you a price estimate and set up a free, non-binding test of the car.",
  },
  {
    icon: "/assets/online-car/2.svg",
    title: "Deliver your car",
    description: "Or let us pick it up. We test and take pictures of the car, then put it out for bids.",
  },
  {
    icon: "/assets/online-car/3.svg",
    title: "Accept the highest bid",
    description: "The money is in your account within a few days, and we take responsibility for any complaints.",
  },
];

const safeAndEasy = [
  {
    icon: "/assets/online-car/4.svg",
    title: "Release liability for complaints",
    description: "We take responsibility when the car is sold.",
  },
  {
    icon: "/assets/online-car/5.svg",
    title: "Deliver your car throughout the country",
    description: "We cover the whole of Norway.",
  },
  {
    icon: "/assets/online-car/6.svg",
    title: "Free of charge",
    description: "No costs for you as a seller.",
  },
  {
    icon: "/assets/online-car/7.svg",
    title: "Sell the car quickly",
    description: "After the bidding round, your car is sold in 1 day if you accept the highest bid.",
  },
];

const testimonials = [
  {
    icon: "/assets/online-car/8.svg",
    title: `"Nettbil are safe, reliable, and serious. And they seem genuinely concerned that I, as a customer, should be satisfied."`,
    description: "André Kristianslund",
  },
  {
    icon: "/assets/online-car/9.svg",
    title: `"Nettbil worked perfectly. Very good service, communication, and logistics."`,
    description: "Anita Paus",
  },
  {
    icon: "/assets/online-car/10.svg",
    title: `"Nettbil worked perfectly. Very good service, communication, and logistics."`,
    description: "Asbjørn Medhus",
  },
];

const HowItWorks = () => {
  return (
    <div className="w-full my-12">
      {/* SECTION: "This is how it works" */}
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 text-left">This is how it works</h2>
        <p className="text-gray-600 text-left">
          Sell the car in 1-2-3 steps. Nettbil is simple, safe, and completely non-binding. You have full control over the entire sales process.
        </p>
      </div>

      {/* Steps Section (Centered) */}
      <div className="flex justify-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-20">
          {steps.map((step) => (
            <OnlineCarSquare
              key={step.title}
              icon={step.icon}
              title={step.title}
              description={step.description}
              size={220}
              iconSize={30}
            />
          ))}
        </div>
      </div>

      {/* SECTION: "Safe and Easy" */}
      <div className="my-12">
        <h2 className="text-2xl font-semibold text-gray-900 text-left">Safe and Easy</h2>
      </div>

      {/* Safe & Easy Section (Centered) */}
      <div className="flex justify-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
          {safeAndEasy.map((item) => (
            <OnlineCarSquare
              key={item.title}
              icon={item.icon}
              title={item.title}
              description={item.description}
              size={200}
              iconSize={30}
            />
          ))}
        </div>
      </div>

      {/* SECTION: Testimonials */}
      <div className="my-12">
        <h2 className="text-2xl font-semibold text-gray-900 text-left">
          So far, 67,582 people have sold a car with Nettbil
        </h2>
      </div>

      {/* Testimonials Section (Centered) */}
      <div className="flex justify-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {testimonials.map((testimonial) => (
            <OnlineCarSquare
              key={testimonial.description}
              icon={testimonial.icon}
              title={testimonial.title}
              description={testimonial.description}
              size={250}
              iconSize={50}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default HowItWorks;