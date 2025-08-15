// pages/plummer.js

import FAQ from "@/components/general/FAQ";
import AreYouAContractor from "@/components/mt-tender/plummer/AreYouAContractor";
import EvaluationCard from "@/components/mt-tender/plummer/EvaluationCard";
import ForHousingAssociations from "@/components/mt-tender/plummer/ForHousingAssociations";
import JobCard from "@/components/mt-tender/plummer/JobCard";
import PlumberCostBox from "@/components/mt-tender/plummer/PlumberCostBox";
import PlumberLeadForm from "@/components/mt-tender/plummer/PlumberLeadForm";
import PlumberPricingInfo from "@/components/mt-tender/plummer/PlumberPricingInfo";
import PlumberServicesInfo from "@/components/mt-tender/plummer/PlumberServicesInfo";
import RecommendationCard from "@/components/mt-tender/plummer/RecommendationCard";
import RegionTabs from "@/components/mt-tender/plummer/RegionTabs";
import WhenNeedPlumber from "@/components/mt-tender/plummer/WhenNeedPlumber";

// Example recommendation data
export const recommendationData = [
    {
        id: 1,
        companyName: "Scanflis AS",
        logoUrl: "/images/scanflis.png",
        promoted: true,
        rating: 4.9,
        totalReviews: 110,
        jobsCount: 134,
        location: "Viken, Oslo",
        reviewHeadline: "Top rated",
        review: {
            author: "Leo",
            date: "15. okt",
            text: "Nice guys who know what they are doing. Scanflis can be trusted..."
        }
    },
    {
        id: 2,
        companyName: "AllTiles Group",
        logoUrl: "/images/alltiles.png",
        promoted: false,
        rating: 4.7,
        totalReviews: 85,
        jobsCount: 90,
        location: "Bergen",
        reviewHeadline: "Solid craftsmanship",
        review: {
            author: "Emma",
            date: "10. sep",
            text: "They were very organized and delivered the tiling work on time..."
        }
    },
    {
        id: 3,
        companyName: "RenovatePro",
        logoUrl: "/images/renovatepro.png",
        promoted: false,
        rating: 4.8,
        totalReviews: 132,
        jobsCount: 200,
        location: "Trondheim",
        reviewHeadline: "Professional team",
        review: {
            author: "Oskar",
            date: "2. jun",
            text: "Great attention to detail and very efficient..."
        }
    },
    {
        id: 4,
        companyName: "Nordic Home Improvement",
        logoUrl: "/images/nordic-home.png",
        promoted: true,
        rating: 4.9,
        totalReviews: 150,
        jobsCount: 170,
        location: "Oslo",
        reviewHeadline: "Would hire again",
        review: {
            author: "Mia",
            date: "20. aug",
            text: "The team communicated well throughout the process..."
        }
    },
    {
        id: 5,
        companyName: "BuildSmart AS",
        logoUrl: "/images/buildsmart.png",
        promoted: false,
        rating: 4.6,
        totalReviews: 67,
        jobsCount: 75,
        location: "Stavanger",
        reviewHeadline: "Great value",
        review: {
            author: "Jonas",
            date: "5. mai",
            text: "BuildSmart AS stayed on budget and offered good suggestions..."
        }
    }
];

// Example job data
const jobData = {
    title: "Latest plumbing jobs posted on Mittanbud",
    location: "1470 LØRENSKOG",
    description:
        "I unscrewed the plastic pipe due to a slight smell and leak to remove dirt and grime...",
    mapEmbedUrl: "https://www.google.com/maps/embed?pb=..." // replace with your map link
};

// Mock evaluation data
export const evaluationData = [
    {
        id: 1,
        rating: 4,
        title: "Replace stop tap and water heater",
        text: "Good and professionally done job. Pleasant professional. Somewhat disappointed with documentation work.",
        date: "Nov. 2024",
        author: "Einar",
        company: "Rørlegger Kongsvold AS",
        location: "Mjøndalen"
    },
    {
        id: 2,
        rating: 4,
        title: "Replace stop tap and water heater",
        text: "Good and professionally done job. Pleasant professional. Somewhat disappointed with documentation work.",
        date: "Nov. 2024",
        author: "Einar",
        company: "Rørlegger Kongsvold AS",
        location: "Mjøndalen"
    },
    {
        id: 3,
        rating: 4,
        title: "Replace stop tap and water heater",
        text: "Good and professionally done job. Pleasant professional. Somewhat disappointed with documentation work.",
        date: "Nov. 2024",
        author: "Einar",
        company: "Rørlegger Kongsvold AS",
        location: "Mjøndalen"
    },
    {
        id: 4,
        rating: 4,
        title: "Replace stop tap and water heater",
        text: "Good and professionally done job. Pleasant professional. Somewhat disappointed with documentation work.",
        date: "Nov. 2024",
        author: "Einar",
        company: "Rørlegger Kongsvold AS",
        location: "Mjøndalen"
    }
];

export default function PlummerPage() {
    return (
        <div className="bg-white py-10">
            <PlumberLeadForm />


            {/* =========================
          Top Section
          Recommendation + Job Cards
         ========================= */}
            <div className="grid grid-cols-5 gap-4">
                {/* Left 3 columns */}
                <div className="col-span-4 space-y-6">
                    <PlumberServicesInfo />
                </div>
                <div className="col-span-1 space-y-20" >
                    <PlumberCostBox />
                </div>

                <div className="col-span-4 space-y-6">
                    <WhenNeedPlumber />
                </div>
                <div className="col-span-1 space-y-20" >
                    <ForHousingAssociations />
                    <AreYouAContractor />
                </div>
                <div className="col-span-3 space-y-6">
                    <PlumberPricingInfo />
                </div>
                <div className="col-span-3 space-y-6">
                    {/* Recommendation Cards */}
                    <div className="space-y-4">
                        {recommendationData.map((item) => (
                            <RecommendationCard key={item.id} data={item} />
                        ))}
                    </div>

                    {/* Job Cards, 2 columns, minimal gap */}
                    <div className="grid grid-cols-2 gap-2">
                        {[...Array(6)].map((_, i) => (
                            <JobCard key={i} job={jobData} />
                        ))}
                    </div>
                </div>

                {/* Right 2 columns: empty */}
                <div className="col-span-2" />

            </div>


            {/* =========================
          Bottom Section
          Evaluation Cards
         ========================= */}
            <div className="grid grid-cols-5 gap-4 mt-8">
                {/* Left 3 columns */}
                <div className="col-span-3 space-y-6 ">
                    <h1 className="text-2xl font-bold text-gray-900">Latest Evaluations</h1>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 ">
                        {evaluationData.map((item) => (
                            <EvaluationCard key={item.id} data={item} />
                        ))}
                    </div>
                </div>
                <div className="col-span-5 space-y-6 ">
                    <FAQ />
                </div>
                {/* Right 2 columns: empty */}
            </div>
            <RegionTabs />
        </div>
    );
}
