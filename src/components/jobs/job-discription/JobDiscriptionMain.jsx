"use client";
import ArticleCard from '../ArticleCard';

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
// This placeholder data simulates what would later come from your backend
const jobPlaceholderData = {
    title: "Cleaner",
    company: "Adecco",
    deadline: "01.12.2024",
    employmentType: "Substitute",
    description: "Looking for a skilled cleaner - become part of our team!",
    mainDescription: [
        "Do you like to leave a place clean and tidy? We are looking for skilled and service-oriented cleaners in the Romerike area!",
        "Due to an increasing amount of assignments from our customers, we are now looking for committed and conscientious employees who like to work with cleaning.",
        "It is desirable that you have experience in cleaning and are available throughout the week. Working hours are between 06.00 and 15.00.",
        "This job does not require a fixed assignment - work at short notice. The people we are looking for are flexible and reliable, and everyday life will be varied with different types of customers. Great if you are used to working independently, but also enjoy working in a team. We are looking for someone who always gives their best and emphasizes quality.",
        "If you also have experience with the food profession and serving, that is an absolute plus.",
        "If you have a car, it is preferable, but as long as you can find your way around and can navigate using public transport to various locations, it will be fine."
    ],
    tasks: [
        "Varied tasks within daily cleaning",
        "Cleaning of common rooms, toilets, stairs etc",
        "Customer care"
    ],
    qualifications: [
        "Preferably with experience in cleaning, minimum 6 months",
        "Preferably with knowledge of INSTA 800",
        "You must be able to speak and understand Norwegian",
        "Immaculate character"
    ],
    personalCharacteristics: [
        "Be efficient and accurate in the execution of the work",
        "Must be punctual, reliable and committed to quality",
        "Act as a positive representative of the company"
    ],
    whyCompany: [
        "As they deliver services to several municipalities in Romerike as well as other private companies in the area, we have good access to assignments. There will be good opportunities to work as much as you want!",
        "At Adecco people feel attractive regardless of the way forward. That's why we offer intro courses, courses after starting and professional top-up every month! We have a benefits program: https://www.adecco.no/medarbeider/fordeler/fordeler",
        "Among other things, after 150 hours worked, you get up to NOK 500 per year in support for physical activity - you choose which.",
        "With a family is also room for flexibility, we can adapt your working weeks to your wishes.",
        "It is easy to accept assignments and register hours via the app."
    ],
    aboutEmployer: [
        "Adecco is one of Norway's leading staffing companies. On the client list, we have attractive companies that need competent employees for exciting assignments. To stay hard at 'various tentacles' the network you get the opportunity to build can be worth its weight in gold when one day you perhaps land your dream job.",
        "All work experience is also good experience. Use us as a discussion partner, we are happy to share advice that can speed up your career."
    ],
    networks: ["Network: Facebook", "LinkedIn", "&"],
    sector: "Private",
    companyRepresentative: "Act as a positive representative of the company",
    keywords: ["cleaning", "cleaning", "cleaner", "cleaning assistant"],
    finnCode: "380035993",
    lastModified: "11/11/2024, 14:42",
    contact: {
        person: "Julia Kyte Feien",
        telephone: "84 84 68 60"
    }
};

const JobDescriptionMain = ({ jobData = jobPlaceholderData }) => {
    return (
        <div>
            <div className="flex flex-col md:flex-row text-gray-800 py-4 gap-6 my-10">
                {/* Main content column */}
                <div className="w-full md:w-2/3">
                    <h1 className="text-3xl font-bold mb-2">{jobData.title}</h1>
                    <div className="mb-4">
                        <p className="font-medium">{jobData.company}</p>
                        <div className="flex gap-4 text-sm">
                            <p>Deadline: {jobData.deadline}</p>
                            <p>Form of employment: {jobData.employmentType}</p>
                        </div>
                    </div>

                    <h2 className="text-xl font-bold mb-2">{jobData.description}</h2>

                    {jobData.mainDescription.map((paragraph, index) => (
                        <p key={`desc-${index}`} className="mb-3">{paragraph}</p>
                    ))}

                    <div className="mt-4">
                        <h3 className="font-bold">Tasks:</h3>
                        <ul className="list-disc pl-5 mb-4">
                            {jobData.tasks.map((task, index) => (
                                <li key={`task-${index}`}>{task}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="mt-4">
                        <h3 className="font-bold">Qualifications:</h3>
                        <ul className="list-disc pl-5 mb-4">
                            {jobData.qualifications.map((qualification, index) => (
                                <li key={`qual-${index}`}>{qualification}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="mt-4">
                        <h3 className="font-bold">Personal characteristics:</h3>
                        <ul className="list-disc pl-5 mb-4">
                            {jobData.personalCharacteristics.map((characteristic, index) => (
                                <li key={`char-${index}`}>{characteristic}</li>
                            ))}
                        </ul>
                    </div>

                    <div className="mt-4">
                        <h3 className="font-bold">Why {jobData.company}?</h3>
                        {jobData.whyCompany.map((paragraph, index) => (
                            <p key={`why-${index}`} className="mb-3">{paragraph}</p>
                        ))}
                    </div>

                    <div className="mt-4">
                        <h3 className="font-bold">About the employer</h3>
                        {jobData.aboutEmployer.map((paragraph, index) => (
                            <p key={`about-${index}`} className="mb-3">{paragraph}</p>
                        ))}
                    </div>

                    <div className="mt-4">
                        <p>{jobData.networks.join(" | ")}</p>
                        <p>Sector: {jobData.sector}</p>
                        <p>{jobData.companyRepresentative}</p>
                    </div>

                    <div className="mt-4">
                        <p>Keywords: {jobData.keywords.join(", ")}</p>
                        <p>FINN code: {jobData.finnCode}</p>
                        <p>Last modified: {jobData.lastModified}</p>
                    </div>
                </div>

                {/* Sidebar column */}
                <div className="w-full md:w-1/3">
                    <div className="bg-white p-4 mb-4 rounded border">
                        <h3 className="font-bold mb-2">Questions about the position</h3>
                        <p>Contact person: {jobData.contact.person}</p>
                        <p>Telephone: {jobData.contact.telephone}</p>
                        <button className="w-full bg-teal-500 text-white py-2 px-4 rounded mt-4">
                            search here
                        </button>
                    </div>

                    <div className="bg-white p-4 mb-4 rounded border">
                        <h3 className="font-bold mb-2">Get to know Norway</h3>
                        <p>Homepage</p>
                        <p>More options</p>
                        <button className="w-full bg-teal-500 text-white py-2 px-4 rounded mt-4">
                            search here
                        </button>
                    </div>

                    <div className="bg-white p-4 rounded border">
                        <h3 className="font-bold mb-2">Check your salary!</h3>
                        <p className="mb-4">
                            Curious about whether you're earning right? FINN's salary calculator gives you an overview of salaries in more than 1,000 different positions.
                        </p>
                        <button className="w-full bg-teal-500 text-white py-2 px-4 rounded">
                            Compare salaries
                        </button>
                    </div>
                </div>
            </div>
            {/* Useful Articles Section */}
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Similar Ads</h2>
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
        </div>
    );
};

export default JobDescriptionMain;