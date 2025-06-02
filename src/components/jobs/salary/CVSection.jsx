"use client";
import FAQ from "@/components/general/FAQ";
import ArticleCard from "../ArticleCard";
import GreenInfoCard from "./GreenInfoCard";
const greenCards = [
    {
        title: "Safe CV storage",
        description:
            "Say goodbye to static Word documents stored on your computer. We offer safe and digital storage of your CV at FINN.no",
    },
    {
        title: "Easy access",
        description:
            "You have access to your CV from anywhere on either a mobile phone, tablet or computer, whatever suits you best.",
    },
    {
        title: "Hassle-free editing",
        description:
            "Make changes anytime, anywhere and share your CV with potential employers from any device.",
    },
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

const faqsData = [
    {
        question: "1. Why do I have to be logged in to use the CV builder?",
        answer: "Because the information in your CV is stored in your Job profile on FINN for easy access, you need to be logged in before creating your CV.",
    },
    {
        question: "2. Why do I have to be logged in to use the CV builder?",
        answer: "Because the information in your CV is stored in your Job profile on FINN for easy access, you need to be logged in before creating your CV.",
    }
];

export default function CVSection() {
    return (
        <div className="w-full bg-white text-gray-800">
            {/* Top CTA */}
            <div className="bg-gray-100 p-6 md:p-10">
                <h2 className="font-semibold text-lg md:text-xl mb-2">FIND CV template</h2>
                <p className="text-sm md:text-base mb-1">Curious about whether you're earning right?</p>
                <p className="text-sm md:text-base mb-4">
                    With this tool you can easily create a professional and modern CV! The CV is saved and can be updated in your Job Profile – so it is always ready when you apply for a job here at FINN. Doesn't that sound smart, then? You can of course also download your new CV as a PDF.
                </p>
                <button className="bg-teal-600 text-white px-4 py-2 text-sm rounded-md">
                    create cv
                </button>
            </div>

            {/* Resume Builder Section */}
            <div className="flex flex-col md:flex-row items-start gap-6 py-10">
                <div className="w-full md:w-1/3 h-48 bg-gray-300 rounded-lg" />
                <div className="w-full md:w-2/3">
                    <h3 className="font-semibold text-lg mb-2">Free resume builder</h3>
                    <p className="text-sm md:text-base mb-4">
                        With the CV builder from FINN, you don't need any other CV templates! Here you get help with the layout of your CV, so that everything is "correct" and looks professional. We store it here with us, so you can easily use it when looking for jobs!
                    </p>
                    <button className="bg-teal-600 text-white px-4 py-2 text-sm rounded-md">
                        Get started
                    </button>
                </div>
            </div>

            {/* Safety Section */}
            <div className=" pb-10">
                <h4 className="font-semibold mb-1">Say goodbye to local documents</h4>
                <p className="text-sm mb-6">
                    The salary calculator uses anonymised statistics. It will be impossible to identify a person through the statistics.
                </p>

                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
                    {greenCards.map((card, index) => (
                        <GreenInfoCard key={index} title={card.title} description={card.description} />
                    ))}
                </div>
            </div>
            {/* Useful Articles Section */}
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Useful articles</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 w-full mb-8 sm:mb-10">
                {articles.map((article, index) => (
                    <ArticleCard
                        key={index}
                        imageUrl={article.imageUrl}
                        title={article.title}
                        onClick={() => { }}
                    />
                ))}
            </div>
            <div className="w-full mb-10">
                <FAQ faqs={faqsData} />
            </div>
        </div>
    );
}
