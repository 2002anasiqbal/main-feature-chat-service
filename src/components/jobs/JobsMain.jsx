"use client";

import SearchBar from "../root/SearchBar";
import LeftAlignedCard from "./LeftAlignedCard";
import Image from "next/image";
import ArticleCard from "./ArticleCard";
import PopularSearches from "./PopularSearches";
import RecommendationJobCard from "./RecommendationJobCard";

const jobRecommendations = [
    {
        imageUrl: "/assets/jobs/5.svg",
        jobTitle: "Mechanical PREs",
        companyName: "Head Energy Consulting AS",
        description: "We are looking for Mechanical PREs",
        location: "Stavanger",
    },
    {
        imageUrl: "/assets/jobs/1.svg",
        jobTitle: "Nurse",
        companyName: "Akershus University Hospital",
        description: "Sykepleier med videreutdanning",
        location: "Lørenskog",
    },
    {
        imageUrl: "/assets/jobs/2.svg",
        jobTitle: "Library Intern",
        companyName: "OsloMet",
        description: "Stipendiat i informasjon, bibliotek- og arkivstudier",
        location: "Oslo",
    },
    {
        imageUrl: "/assets/jobs/3.svg",
        jobTitle: "Senior Advisor",
        companyName: "Oslo Politidistrikt",
        description: "Vi søker rådgiver til spennende samfunnsoppdrag",
        location: "Oslo",
    },
];

// Separate card data
const cardData = [
    {
        icon: "/assets/jobs/1.svg",
        label: "Your Job Profile",
        title: "Find your dream job",
        subtitle: "There are 43,486 positions on FINN.no right now."
    },
    {
        icon: "/assets/jobs/2.svg",
        label: "Wages",
        title: "Compare your salary",
        subtitle: "Compare your salary with other peoples."
    },
    {
        icon: "/assets/jobs/3.svg",
        label: "Resume",
        title: "Create a brand new CV",
        subtitle: "Create a brand new and updated CV quickly and easily"
    }
];

const articles = [
    {
        imageUrl: "/assets/jobs/7.svg",
        title: "Top 5 in demand occupation right now",
    },
    {
        imageUrl: "/assets/jobs/8.svg",
        title: "Part time job is full of opportunities",
    },
    {
        imageUrl: "/assets/jobs/6.svg",
        title: "How to write a good job application",
    },
];

const searches = [
    {
        title: "Positions",
        list: [
            "Nurse",
            "Engineer",
            "Social worker and environmental therapist",
            "Teacher and principal",
            "IT development",
        ],
    },
    {
        title: "Places",
        list: ["Oslo", "Bergen", "Trondhim", "Stavangar", "Tromsø"],
    },
    {
        title: "Articles",
        list: ["Tips and advice", "Job applications", "Tip and cv", "CV templates", "Wages"],
    },
];

export default function JobMain() {
    return (
        <div className="min-h-screen bg-white">
            <div className="my-10 w-full">
                <SearchBar />
            </div>
            {/* Top Banner */}
            <div className="bg-teal-700 text-white py-6 sm:py-8 text-center px-4">
                <h1 className="text-xl sm:text-2xl font-semibold mb-2">Is Monday coming a little too soon?</h1>
                <p>Do something about it, at FINN we have 43,486 vacancies</p>
            </div>

            {/* Main Card Section */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 py-6 sm:py-8">
                {cardData.map((card, index) => (
                    <LeftAlignedCard
                        key={index}
                        icon={card.icon}
                        label={card.label}
                        title={card.title}
                        subtitle={card.subtitle}
                    />
                ))}
            </div>

            {/* Last Viewed Section */}
            <div className="mb-8 sm:mb-10">
                <h2 className="text-lg font-semibold text-gray-800 mb-1 flex items-center gap-2">
                    <Image src="/assets/jobs/4.svg" alt="clock" width={18} height={18} />
                    Last viewed
                </h2>
                <p className="text-sm text-gray-500 mb-2">Continue where you last left off</p>
                <div className="h-24 sm:h-28 border rounded-md flex items-center justify-center gap-3 sm:gap-5 text-gray-400 text-xs sm:text-sm px-4 text-center">
                    <Image src="/assets/jobs/5.svg" alt="clock" width={60} height={60} className="hidden sm:block" />
                    <Image src="/assets/jobs/5.svg" alt="clock" width={40} height={40} className="sm:hidden" />
                    Your most recently placed ads will appear here
                </div>
            </div>

            <div className="mb-8 sm:mb-10">
                {/* Heading */}
                <h2 className="text-lg font-semibold text-gray-800 mb-1 flex items-center gap-2">
                    <Image src="/assets/jobs/6.svg" alt="heart" width={18} height={18} />
                    Recommendations for you
                </h2>
                <p className="text-sm text-gray-500 mb-4">
                    Based on your preferences, these may suit you
                </p>

                {/* Grid */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Left Recommendation Intro Card */}
                    <div className="border rounded-md p-4 sm:p-6 flex flex-col justify-between items-center text-center bg-white shadow-sm h-full">
                        <div className="flex flex-col items-center justify-center flex-1">
                            <Image src="/assets/jobs/7.svg" alt="rec" width={60} height={60} className="sm:w-[70px] sm:h-[70px]" />
                            <p className="font-medium mt-3 sm:mt-4 text-gray-800">Your recommendations</p>
                            <p className="text-xs sm:text-sm text-gray-500 mt-2">
                                In order to show you personalized recommendations, we need to know a little more about you and your skills
                            </p>
                        </div>
                        <button className="bg-teal-600 text-white px-4 py-2 rounded-md w-full text-sm mt-4 sm:mt-6">
                            Start
                        </button>
                    </div>

                    {/* Job Cards in 2x2 format */}
                    <div className="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
                        {jobRecommendations.map((job, idx) => (
                            <RecommendationJobCard key={idx} {...job} />
                        ))}
                    </div>
                </div>
            </div>

            {/* Salary Banner */}
            <div className="bg-teal-700 text-white p-4 sm:p-6 flex flex-col sm:flex-row justify-between items-center rounded-md">
                <div className="flex flex-col sm:flex-row px-3 sm:px-5 py-4 sm:py-0 sm:h-24 rounded-sm justify-center w-full mx-auto bg-white items-center gap-3 mb-4 sm:mb-0">
                    <Image src="/assets/jobs/2.svg" alt="compare" width={50} height={50} className="sm:w-[60px] sm:h-[60px]" />
                    <div className="text-center sm:text-left">
                        <p className="font-medium text-gray-900">Compare your salary</p>
                        <p className="text-xs sm:text-sm text-gray-600">Are you getting what you deserve in your current position?</p>
                    </div>
                    <button className="text-white bg-teal-700 px-4 py-2 rounded-md font-semibold text-sm mt-3 sm:mt-0">Compare salaries</button>
                </div>
            </div>

            <div className="w-full py-10">
                {/* Useful Articles Section */}
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Useful articles</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 w-full max-w-5xl mx-auto mb-8 sm:mb-10">
                    {articles.map((article, index) => (
                        <ArticleCard
                            key={index}
                            imageUrl={article.imageUrl}
                            title={article.title}
                            onClick={() => { }}
                        />
                    ))}
                </div>

                {/* Popular Searches Section */}
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Popular searches</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 sm:gap-16 lg:gap-28">
                    {searches.map((search, index) => (
                        <PopularSearches key={index} title={search.title} list={search.list} />
                    ))}
                </div>
            </div>
        </div>
    );
}