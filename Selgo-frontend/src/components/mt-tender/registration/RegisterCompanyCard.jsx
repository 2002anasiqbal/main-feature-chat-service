export default function RegisterCompanyCard() {
    return (
      <div className="bg-[#e6f2f2] py-10 px-4 md:px-10">
        {/* Top Section */}
        <div className="max-w-2xl mx-auto text-center mb-8">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900">
            Get new customers and attractive jobs
          </h2>
          <p className="text-sm text-gray-700 mt-2">
            Thousands of new missions every week. Create a free test profile now
            and see all the jobs near you.
          </p>
  
          {/* Input Fields */}
          <div className="mt-6 space-y-4 text-gray-500">
            <input
              type="text"
              placeholder="Company Name"
              className="w-full border border-purple-500 rounded-md p-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
            <input
              type="text"
              placeholder="Phone No."
              className="w-full border border-purple-500 rounded-md p-2 text-sm outline-none focus:ring-2 focus:ring-purple-400"
            />
          </div>
  
          {/* Submit Button */}
          <button className="bg-teal-600 hover:bg-teal-700 text-white font-semibold px-6 py-2 mt-4 rounded-md">
            Continue
          </button>
  
          {/* Terms and Login */}
          <p className="text-xs text-gray-700 mt-4">
            By continuing the registration, you accept the terms of use for
            Mittanbud. You can read more about the processing of personal data{" "}
            <a href="#" className="text-blue-700 underline">
              here
            </a>
            . Already a user?{" "}
            <a href="#" className="text-gray-900 font-medium">
              Log in here
            </a>
          </p>
        </div>
  
        {/* Divider */}
        <hr className="my-6 w-3/4 mx-auto" />
  
        {/* Bottom Section */}
        <div className="max-w-5xl mx-auto flex flex-col md:flex-row items-center gap-6 mt-10">
          <div className="bg-gray-200 w-full h-40 md:w-1/2 md:h-48 rounded-md" />
          <div className="text-left text-sm md:w-1/2">
            <h3 className="text-lg font-semibold mb-2">Get started right now</h3>
            <ul className="list-disc list-inside space-y-1 text-gray-800">
              <li>Register the company</li>
              <li>
                Enter your company name and phone number and we&apos;ll help you
                set up a free test profile.
              </li>
              <li>Get access to relevant jobs near you</li>
              <li>
                Get access to all the jobs within your industry and within the
                areas you want.
              </li>
              <li>Win jobs and get good evaluations</li>
              <li>
                Contact customers, win jobs and get good evaluations that will be
                visible on your company&apos;s profile page.
              </li>
            </ul>
          </div>
        </div>
      </div>
    );
  }  