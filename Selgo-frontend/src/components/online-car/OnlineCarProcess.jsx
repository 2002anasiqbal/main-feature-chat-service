"use client";
import React from "react";
import Image from "next/image";
import OnlineCarSquare from "./OnlineCarSquare"; // Ensure this is imported
import Link from "next/link";

const featureCards = [
    {
        icon: "/assets/online-car/11.svg",
        title: "Use little time and effort",
        description: "Nettbil helps you with sales, from A to Z. You can spend more time on your business, and less time on car sales.",
    },
    {
        icon: "/assets/online-car/11.svg",
        title: "Sell more cars",
        description: "Nettbil’s adviser helps you plan the sale, and we can arrange the transport of the car if necessary.",
    },
    {
        icon: "/assets/online-car/11.svg",
        title: "Best price from dealer",
        description: "Nettbil allows dealers to bid on your car, based on an independent test from NAF or Viking Kontroll. Your company gets the best price from the dealer.",
    },
];

const processSteps = [
    {
        title: "The adviser will contact you",
        description: "You get a plan adapted to your needs, and an estimated price per car.",
    },
    {
        title: "Tests are carried out at NAF or Viking Kontroll",
        description: "The car can be delivered at the test centre, or Nettbil can arrange transport if necessary. Nettbil can also order a car wash upon delivery.",
    },
    {
        title: "Bidding round",
        description: "Your car is advertised to more than 2,400 dealers who are vying to buy it. Whether they are allowed to buy it is up to you.",
    },
    {
        title: "Car sold and money in account",
        description: "Your car is sold on the day and you receive money in your account shortly afterwards.",
    },
];

const OnlineCarProcess = () => {
    return (
        <div className="w-full my-12">
            {/* Hero Section */}
            <div className="flex flex-col md:flex-row items-center gap-6">
                {/* Left Side */}
                <div className="md:w-1/2">
                    <p className="text-teal-600 font-medium">Online car company</p>
                    <h1 className="text-3xl font-bold text-gray-900">
                        Nettbil helps you get the best price from the dealer. <br />
                        <span className="text-gray-800">Fast, easy and safe.</span>
                    </h1>
                    <p className="text-gray-600 mt-2">
                        Leave your contact information, and an adviser with us will contact you to discuss and plan the sale.
                    </p>
                    <Link href="/routes/online-car/registration">
                        <button className="mt-4 px-6 py-3 bg-teal-600 text-white rounded-md font-semibold hover:bg-teal-700 transition-all">
                            Contact Me
                        </button>
                    </Link>
                </div>

                {/* Right Side (Car Image) */}
                <div className="md:w-1/2 flex justify-center">
                    <Image src="/assets/online-car/car.svg" alt="Car" width={400} height={250} />
                </div>
            </div>

            {/* Features Section */}
            <div className="mt-12 flex justify-center">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {featureCards.map((feature, index) => (
                        <OnlineCarSquare
                            key={index}
                            icon={feature.icon}
                            title={feature.title}
                            description={feature.description}
                            size={220}
                            iconSize={30}
                        />
                    ))}
                </div>
            </div>

            {/* Process Section */}
            <div className="mt-12">
                <h2 className="text-2xl font-semibold text-gray-900">
                    Nettbil ensures a quick and easy sale for your company
                </h2>
                <div className="mt-6 space-y-6">
                    {processSteps.map((step, index) => (
                        <div key={index} className="flex items-start space-x-4">
                            <span className="text-teal-600 font-bold text-lg">{index + 1}.</span>
                            <div>
                                <h3 className="text-lg font-semibold text-teal-600">{step.title}</h3>
                                <p className="text-gray-600">{step.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default OnlineCarProcess;