export default function RegisterInterestBox() {
    return (
      <section className="bg-[#e6f2f2] px-4 py-12 text-center">
        {/* Heading */}
        <h2 className="text-xl sm:text-2xl font-semibold text-gray-900">
          Want to try us?
        </h2>
        <p className="text-sm text-gray-700 mt-1 max-w-md mx-auto">
          Thousands of new missions every week. Create a free test profile now and see all the jobs near you.
        </p>
  
        {/* Form Fields */}
        <div className="max-w-md mx-auto mt-6 space-y-4 text-gray-600">
          <div className="text-left">
            <label htmlFor="companyName" className="text-xs font-medium text-purple-700">
              Company Name
            </label>
            <input
              id="companyName"
              type="text"
              placeholder=""
              className="w-full p-2 border border-purple-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
            />
          </div>
  
          <div className="text-left">
            <label htmlFor="companyEmail" className="text-xs font-medium text-purple-700">
              Company email
            </label>
            <input
              id="companyEmail"
              type="email"
              placeholder=""
              className="w-full p-2 border border-purple-600 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-400"
            />
          </div>
        </div>
  
        {/* Continue Button */}
        <div className="mt-6">
          <button className="bg-teal-600 text-white px-6 py-2 rounded hover:bg-teal-700 transition">
            Continue
          </button>
        </div>
  
        {/* Terms Notice */}
        <p className="text-xs text-gray-700 mt-4 max-w-xl mx-auto px-4">
          By continuing the registration, you accept the terms of use for Mittanbud.
          You can read more about the processing of personal data <a href="#" className="underline text-gray-900">here</a>.
          Already a user? <a href="/routes/my-tender/login" className="underline text-gray-900">Log in here</a>
        </p>
  
        {/* Horizontal line (optional if needed) */}
        <div className="border-t mt-6 w-full max-w-xl mx-auto"></div>
      </section>
    );
  }
  