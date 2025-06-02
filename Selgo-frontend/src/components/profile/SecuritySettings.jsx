"use client";

export default function SecuritySection({
  title,
  description,
  buttonText,
  items = [],
}) {
  return (
    <div className="bg-white py-6 space-y-4">
      {/* Title */}
      <h2 className="text-2xl font-bold text-gray-800 mb-2">{title}</h2>
      <p className="text-gray-600 mb-4">{description}</p>

      {/* Main Button */}
      {buttonText && (
        <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600 transition">
          {buttonText}
        </button>
      )}

      {/* Security Items */}
      <div className="mt-6 space-y-10">
        {items.map((item, index) => (
          <div key={index} className="flex justify-between items-center ">
            {/* Left Side: Security Info */}
            <div className="space-y-2">
              <h3 className="text-lg font-semibold text-gray-800 ">
                {item.title}
              </h3>
              <p className="text-gray-600">{item.description}</p>
              <p className="text-gray-600">
                <strong>Status:</strong> {item.status}
              </p>
            </div>

            {/* Right Side: Action Button */}
            <button className="bg-teal-500 text-white px-5 py-2 rounded-md hover:bg-teal-600 transition">
              {item.buttonText}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
