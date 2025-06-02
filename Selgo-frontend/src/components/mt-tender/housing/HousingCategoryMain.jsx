"use client";
import Link from "next/link";
import GenericCardCollection from "@/components/GenericCardCollection";

const housingCardData = [
    {
        items: [
            { tag: "Roof", icon: "1.svg", route: "#" },
            { tag: "Window and door", icon: "2.svg", route: "#" },
            { tag: "Car charger", icon: "3.svg", route: "#" },
            { tag: "Facade", icon: "4.svg", route: "#" },
        ],
    },
    {
        items: [
            { tag: "Tube", icon: "5.svg", route: "#" },
            { tag: "Garage", icon: "6.svg", route: "#" },
            { tag: "Clothing", icon: "7.svg", route: "#" },
            { tag: "Clothing", icon: "8.svg", route: "#" },
        ],
    },
    {
        items: [
            { tag: "Renovate bathroom", icon: "9.svg", route: "#" },
            { tag: "Measure", icon: "10.svg", route: "#" },
            { tag: "Isolate", icon: "11.svg", route: "#" },
            { tag: "Others", icon: "12.svg", route: "#" },
        ],
    },
];

const rowStyles = {
    0: {
        gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4",
        gap: "gap-6",
        marginBottom: "mb-6",
    },
    1: {
        gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4",
        gap: "gap-6",
        marginBottom: "mb-6",
    },
    2: {
        gridCols: "grid-cols-2 sm:grid-cols-4 lg:grid-cols-4",
        gap: "gap-6",
        centered: true,
    },
};

export default function HousingCategoryMain() {
    return (
        <div className="bg-white pb-12">
            <div className="bg-[#dff0f0] py-12 ">
                <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    {/* Left Text Section */}
                    <div>
                        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
                            Mittenbud makes projects in housing associations and condominiums easier!
                        </h2>
                        <p className="text-gray-700 mb-6">
                            Are you on the board of a housing association or condominium? We help you find solid craft companies for both small and large projects
                        </p>
                        <Link
                            href="/routes/my-tender/category"
                            className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700 transition"
                        >
                            Post a Job
                        </Link>
                    </div>

                    {/* Right Image Placeholder */}
                    <div className="bg-gray-300 w-full h-64 rounded-lg" />
                    {/* To use a real image instead, replace with:
        <Image src="/assets/my-tender/housing/your-image.svg" alt="Housing visual" width={500} height={300} className="rounded-lg" />
        */}
                </div>
            </div>
            <div className="max-w-6xl mx-auto px-6 pt-10 text-gray-800">
                <h2 className="text-xl sm:text-2xl font-semibold text-center mb-2">
                    Get help for your next project in the housing association
                </h2>
                <p className="text-sm text-center text-gray-700 mb-6 max-w-2xl mx-auto">
                    Choose a category, describe the job and get non-binding offers from several companies near you – completely free of charge.
                </p>

                <GenericCardCollection
                    rows={housingCardData}
                    rowStyles={rowStyles}
                    imageBasePath="/assets/my-tender/housing/"
                    size="h-28 w-40"
                />
            </div>
            <div className="bg-[#dff0f0] py-12 ">
                <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
                    {/* Right Image Placeholder */}
                    <div className="bg-gray-300 w-full h-64 rounded-lg" />
                    {/* To use a real image instead, replace with:
        <Image src="/assets/my-tender/housing/your-image.svg" alt="Housing visual" width={500} height={300} className="rounded-lg" />
        */}
                    {/* Left Text Section */}
                    <div>
                        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-4">
                            Big projects in the housing association? My tender
                            XL helps you
                        </h2>
                        <p className="text-gray-700 mb-6">
                            Are you planning to refurbish the bathrooms in the block, build balconies, replace windows or renew the facade?
                            <br/>
                            <br/>
                            Mittanbud XL takes care of large projects that require extra help and guidance. Our project supervisors give you advice and support from start to finish in the project.
                        </p>
                        <Link
                            href="/routes/my-tender/category"
                            className="bg-teal-600 text-white px-4 py-2 rounded hover:bg-teal-700 transition"
                        >
                            Post a Job
                        </Link>
                    </div>


                </div>
            </div>
        </div>
    );
}