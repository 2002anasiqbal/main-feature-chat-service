"use client"

export default function PopularSearches({ title = "Positions", list = [] }) {
    return (
        <div>
                <div className="bg-teal-700 text-white text-center py-2 rounded-lg font-medium">
                    {title}
                </div>
            <div className="bg-white w-full max-w-xs">
                <ul className=" pt-5 space-y-2">
                    {list.map((item, index) => (
                        <li key={index} className="text-gray-500 text-sm">
                            {item}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}
