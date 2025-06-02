"use client";

export default function XLProjectSupervisors() {
    const supervisors = [
        {
            name: "Emilie Syvertsen",
            title: "Project supervisor",
            image: "/assets/supervisors/emilie.png", // Replace with real paths
        },
        {
            name: "Emilie Syvertsen",
            title: "Project supervisor",
            image: "/assets/supervisors/emilie.png",
        },
        {
            name: "Emilie Syvertsen",
            title: "Project supervisor",
            image: "/assets/supervisors/emilie.png",
        },
    ];

    return (
        <div className="bg-[#e3f1f1] pt-12 pb-16">
            {/* Top Section */}
            <div className="max-w-4xl mx-auto text-center px-4">
                <h2 className="text-3xl sm:text-4xl font-bold text-gray-900">
                    Meet the project supervisors at Mittanbud XL
                </h2>
                <p className="mt-4 text-gray-700">
                    Are you planning to refurbish the bathrooms in the block, build balconies, replace windows or renew the facade?
                </p>
                <p className="mt-2 text-gray-700">
                    Mittanbud XL takes care of large projects that require extra help and guidance. Our project supervisors give you
                    advice and support from start to finish in the project.
                </p>
                <button className="mt-6 bg-teal-600 text-white px-5 py-2 rounded hover:bg-teal-700 transition">
                    Post a Job on XL
                </button>
            </div>
        </div>
    );
}
