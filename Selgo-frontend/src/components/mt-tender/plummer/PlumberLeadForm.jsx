import Image from "next/image";

export default function PlumberLeadForm() {
  return (
    <div className="w-full bg-teal-100 grid md:grid-cols-2 min-h-[500px] my-10">
      {/* Left Info Section */}
      <div className="bg-[#e5f3f3] p-8 flex flex-col justify-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Do you need a plumber?
        </h2>
        <p className="text-gray-700 mb-4">
          Do you need a plumber for a planned project, repairs, improvements or
          upgrades? At Mittanbud, skilled plumbers will compete for your
          assignment!
        </p>
        <ul className="text-gray-800 space-y-3">
          <li className="flex items-start gap-2">
            <span className="text-teal-600 font-bold text-xl">✓</span>
            Post the job completely free of charge
          </li>
          <li className="flex items-start gap-2">
            <span className="text-teal-600 font-bold text-xl">✓</span>
            Receive non-binding offers from companies
          </li>
          <li className="flex items-start gap-2">
            <span className="text-teal-600 font-bold text-xl">✓</span>
            Choose the offer that suits you best
          </li>
        </ul>
      </div>

      {/* Right Form Section */}
      <div
        className="bg-cover bg-center flex flex-col justify-center p-8"
        style={{ backgroundImage: "url('/assets/my-tender/hero.svg')" }}
      >
        <div className="bg-white bg-opacity-90 rounded-lg p-6 shadow-md">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Get offers from quality-assured companies
          </h2>

          <input
            type="text"
            placeholder="Title of the project"
            className="w-full mb-4 border border-gray-300 rounded-md px-4 py-2 focus:outline-teal-600"
          />
          <textarea
            rows={5}
            placeholder="Describe"
            className="w-full mb-4 border border-gray-300 rounded-md px-4 py-2 focus:outline-teal-600"
          ></textarea>

          <button className="w-full bg-teal-700 text-white font-medium py-3 rounded-md hover:bg-teal-800 transition">
            Post a Job and get an Offer
          </button>
        </div>
      </div>
    </div>
  );
}
