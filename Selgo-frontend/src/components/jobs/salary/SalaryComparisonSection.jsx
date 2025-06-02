"use client";

import ArticleCard from "../ArticleCard";
import GreenInfoCard from "./GreenInfoCard";

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

const greenCards = [
    {
        title: "Anonymously",
        description:
            "Only your annual salary becomes part of the statistics. All other information about your own position and salary will only be visible to you.",
    },
    {
        title: "Easy access",
        description:
            "All salary data is stored in your Job profile on FINN, where you can easily adjust the information you have entered.",
    },
    {
        title: "Real users",
        description:
            "You must be logged in with your FINN user to enter salary data. This ensures that we get real data from real users.",
    },
];

export default function SalaryComparisonSection() {
    return (
        <div className="w-full bg-white text-gray-800">
            {/* Top Section - Banner */}
            <div className="bg-gray-100 p-6 md:p-10">
                <h2 className="font-semibold text-lg md:text-xl mb-2">Check your salary!</h2>
                <p className="mb-1 text-sm md:text-base">Curious about whether you're earning right?</p>
                <p className="mb-4 text-sm md:text-base">
                    FINN's salary calculator gives you an overview of salaries in more than 1,000 different positions.
                </p>
                <button className="bg-teal-600 text-white px-4 py-2 text-sm rounded-md">Compare your salary</button>
            </div>

            {/* Middle Section */}
            <div className="flex flex-col md:flex-row items-start gap-6 px-6 md:px-10 py-10">
                <div className="w-full md:w-1/3 h-48 bg-gray-300 rounded-lg" />
                <div className="w-full md:w-2/3">
                    <h3 className="font-semibold text-lg mb-2">Help us speak louder about wages!</h3>
                    <p className="text-sm md:text-base">
                        Everyone should earn a fair wage, but what exactly is a fair wage? The best way to find out is to just tell them –
                        and you can do that here. The more people who enter what they earn, the better the basis for comparison.
                        Let’s create a more open labor market together!
                    </p>
                </div>
            </div>

            {/* Info Section */}
            <div className="px-6 md:px-10">
                <h4 className="font-semibold text-base md:text-lg mb-1">Completely safe</h4>
                <p className="text-sm mb-6">
                    The salary calculator uses anonymised statistics. It will be impossible to identify a person through the statistics.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mb-10">
                    {greenCards.map((card, index) => (
                        <GreenInfoCard key={index} title={card.title} description={card.description} />
                    ))}
                </div>
            </div>

            {/* Bottom CTA */}
            <div className="px-6 md:px-10 pb-10">
                <h4 className="font-semibold mb-1">Do you have no salary to compare?</h4>
                <p className="mb-4 text-sm">
                    Zero stress! You do not need to provide your own salary data to see the average salary for various positions.
                    Our salary calculator is for everyone!
                </p>
                <button className="bg-teal-600 text-white px-4 py-2 text-sm rounded-md">
                    Compare your salary
                </button>
            </div>

            {/* Useful Articles Section */}
            <h2 className="text-xl font-semibold text-gray-800 mb-4 px-6 md:px-10">Useful articles</h2>
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
        </div>
    );
}