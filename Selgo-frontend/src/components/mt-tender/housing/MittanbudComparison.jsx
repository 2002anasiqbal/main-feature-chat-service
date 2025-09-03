"use client";

export default function MittanbudComparison() {
    return (
        <div className="bg-white py-12 px-4 max-w-6xl mx-auto">
            <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
                What is the difference between Mittanbud XL and Mittanbud's ordinary service?
            </h2>
            <p className="text-gray-700 mb-8">
                With Mittanbud XL, you get the help of our project supervisors throughout the entire project!
            </p>

            <div className="border border-gray-300 rounded-md overflow-hidden">
                <div className="overflow-x-auto">
                    <div className="min-w-[800px] w-full">
                        <div className="grid grid-cols-5 bg-gray-50 text-center font-semibold text-gray-900 text-sm">
                            <div className="col-span-3 text-left px-4 py-3"> </div>
                            <div className="px-4 py-3">My Tender</div>
                            <div className="px-4 py-3">My Tender XL</div>
                        </div>

                        {/* Row */}
                        <div className="grid grid-cols-5 border-t text-sm">
                            <div className="col-span-3 px-4 py-5">
                                <p className="font-semibold text-gray-900">Non-binding offer</p>
                                <p className="text-gray-700">
                                    Register the job for free, and receive non-binding offers from selected relevant companies
                                </p>
                            </div>
                            <div className="flex items-center justify-center text-teal-700">✓</div>
                            <div className="flex items-center justify-center text-teal-700">✓</div>
                        </div>

                        {/* Repeat similar rows */}
                        <div className="grid grid-cols-5 border-t text-sm">
                            <div className="col-span-3 px-4 py-5">
                                <p className="font-semibold text-gray-900">Eligible companies</p>
                                <p className="text-gray-700">
                                    Choose between qualified craft companies with experience from similar projects
                                </p>
                            </div>
                            <div className="flex items-center justify-center text-teal-700">✓</div>
                            <div className="flex items-center justify-center text-teal-700">✓</div>
                        </div>

                        <div className="grid grid-cols-5 border-t border-b text-sm">
                            <div className="col-span-3 px-4 py-5">
                                <p className="font-semibold text-gray-900">Follow-up and support</p>
                                <p className="text-gray-700">
                                    Get follow-up and support throughout the project period from your own supervisor
                                </p>
                            </div>
                            <div className="flex items-center justify-center text-teal-700"> </div>
                            <div className="flex items-center justify-center text-teal-700">✓</div>
                        </div>
                    </div>
                </div>

            </div>

            <div className="mt-6 text-center text-sm text-gray-600">
                Do you have questions about XL or need help? Contact us by e-mail:{" "}
                <a href="mailto:xl@mittanbud.no" className="underline">
                    xl@mittanbud.no
                </a>
                . Already a user?{" "}
                <a href="#" className="underline">
                    Log in here
                </a>
            </div>

            <div className="mt-6 flex flex-col sm:flex-row justify-center gap-4">
                <button className="px-4 py-2 border border-gray-600 text-gray-800 rounded hover:bg-gray-100 transition">
                    What is mittanbud xl
                </button>
                <button className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700 transition">
                    Register your Project
                </button>
            </div>
        </div>
    );
}
