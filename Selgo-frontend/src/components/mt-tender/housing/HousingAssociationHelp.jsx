"use client";

export default function HousingAssociationHelp() {
  const supervisors = [
    {
      name: "Emilie Syvertsen",
      title: "Project supervisor",
      image: "/assets/supervisors/emilie.png", // Placeholder
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
    <div className="bg-white pb-20">
      {/* Supervisor Cards */}
      <div className="max-w-7xl mx-auto px-6 pt-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
        {supervisors.map((sup, i) => (
          <div key={i} className="text-center">
            <div className="bg-gray-300 aspect-square rounded" />
            <p className="mt-2 font-semibold text-sm text-gray-900">{sup.name}</p>
            <p className="text-sm text-gray-700">{sup.title}</p>
          </div>
        ))}
        {/* Right-side question box */}
        <div className="bg-gray-200 p-4 text-sm rounded flex flex-col justify-center">
          <p className="font-semibold text-gray-800">Do you have questions?</p>
          <p className="text-gray-700 mt-1">
            Are you wondering about Mittanbud XL? Do not hesitate to contact us!
          </p>
          <p className="mt-2 font-bold text-gray-900">xl@mittanbud.no</p>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center mt-12 px-4">
        <h2 className="text-xl sm:text-2xl font-semibold text-gray-900">
          Are you planning a project for the housing association or condominium?
        </h2>
        <p className="mt-2 text-gray-700">
          Have a no-obligation chat with one of our project supervisors, and we’ll help you get started!
        </p>
        <button className="mt-6 px-6 py-2 bg-teal-600 text-white rounded hover:bg-teal-700 transition">
          Fill in your contact information
        </button>
      </div>

      {/* Quality Section */}
      <div className="mt-16 grid grid-cols-1 md:grid-cols-2 gap-4 bg-[#e3f1f1] px-6 py-12">
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            This is how we ensure the companies' quality
          </h3>
          <ul className="list-disc text-sm text-gray-800 space-y-2 pl-6">
            <li>
              Companies that cooperate with Mittanbud XL must have at least 2 years' experience, be a registered limited company or similar, be VAT registered and have liability insurance.
            </li>
            <li>
              We require at least one of the following three approvals: Master’s certificate, Centrally approved, Approved wet room company.
            </li>
            <li>
              We use the credit rating system Experian to ensure the companies have solid creditworthiness.
            </li>
            <li>
              Companies cannot have bad evaluations, references or feedback.
            </li>
          </ul>
        </div>
        <div className="bg-gray-300 rounded h-[250px] md:h-auto" />
      </div>
    </div>
  );
}
