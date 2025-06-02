"use client"
import PriceGrid from "@/components/property/PriceGrid";
import LocationMap from "@/components/general/LocationMap";
import Image from "next/image";
import FeedbackForm from "@/components/general/FeedbackForm";
const backendData = [
    { title: "Bergen", value: "NOK 541235", description: "On average per advertisement in last 30 days" },
    { title: "Oslo", value: "NOK 620000", description: "On average per advertisement in last 30 days" },
    { title: "Stavanger", value: "NOK 495000", description: "On average per advertisement in last 30 days" },
    { title: "Trondheim", value: "NOK 560000", description: "On average per advertisement in last 30 days" },
    { title: "Drammen", value: "NOK 480000", description: "On average per advertisement in last 30 days" },
    { title: "Kristiansand", value: "NOK 510000", description: "On average per advertisement in last 30 days" },
];

export default function SellPage() {
      // Handle feedback submission
      const handleFeedbackSubmit = (message) => {
        console.log("Feedback received:", message);
        // Here, you can send feedback to an API, store in the database, etc.
    };
    return (
        <div>
            <LocationMap heading="Check what price homes in your area have sold for" />
            <button className=" block mx-auto bg-teal-600 hover:bg-teal-800 h-15 px-10 border rounded-lg text-white font-semiboldbold">See Sale Price</button>
            <div className="bg-white">
                <PriceGrid data={backendData} />
            </div>
            <div className="mt-10 flex flex-col md:flex-row items-center justify-between gap-8">
                {/* Text Content (Left Side) */}
                <div className="w-full md:w-2/3">
                    <h3 className="text-2xl font-bold text-gray-900">Are you going to sell a home?</h3>
                    <p className="text-gray-600 mt-2 leading-relaxed">
                        Selling a home can be both time-consuming, exciting and perhaps a little scary?<br/>
                        We have put together a number of tips and tricks that can be nice to think about when you are selling a property.
                    </p>

                    {/* Buttons */}
                    <div className="flex flex-wrap sm:flex-nowrap gap-4 mt-4">
                        <button className="px-10 py-2 bg-teal-600 text-white font-semibold rounded-md hover:bg-teal-700 transition">
                            Checkout tips and tricks here
                        </button>
                    </div>
                </div>

                {/* Notepad Image (Right Side) */}
                <div className="w-full md:w-1/3 flex justify-end">
                    <Image
                        src="/assets/property/8.svg"
                        alt="Notepad"
                        width={230}
                        height={230}
                        className="object-contain"
                    />
                </div>
            </div>
            <h3 className="my-10 text-2xl font-bold text-gray-900">Are you wondering about something, or are you missing something on this page?</h3>            
            <FeedbackForm onSubmit={handleFeedbackSubmit} />
        </div>
    );
}
