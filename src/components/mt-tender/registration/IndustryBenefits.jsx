export default function IndustryBenefits() {
    return (
      <div className="bg-[#e6f2f2] px-6 py-12">
        {/* Title & Input */}
        <div className="text-center max-w-3xl mx-auto">
          <h2 className="text-2xl md:text-3xl font-semibold text-gray-900">
            Great demand for good people
          </h2>
          <p className="mt-2 text-sm text-gray-700">
            Every week, thousands of customers post jobs that need answers from
            several skilled companies. Select your industry below and see why your
            company should join Mittanbud
          </p>
  
          <input
            type="text"
            placeholder="Select industry"
            className="mt-6 w-full border text-gray-600 border-purple-500 p-2 rounded-md outline-none focus:ring-2 focus:ring-purple-400"
          />
        </div>
  
        {/* Stats Section */}
        <div className="grid grid-cols-3 text-center mt-10 gap-4 max-w-3xl mx-auto">
          <div>
            <p className="text-2xl font-bold text-gray-900">211,000</p>
            <p className="text-sm text-gray-600">Working last year</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">4</p>
            <p className="text-sm text-gray-600">Average response per year</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-gray-900">32,000</p>
            <p className="text-sm text-gray-600">Average price per job</p>
          </div>
        </div>
  
        {/* Advantages */}
        <div className="mt-12 text-center max-w-4xl mx-auto">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">
            Many advantages with Mittanbud
          </h3>
          <ul className="list-disc list-inside text-left text-gray-800 space-y-2 text-sm">
            <li>
              <b>Access to jobs:</b> Join Mittanbud and get relevant jobs for your
              company.
            </li>
            <li>
              <b>Customers make direct contact:</b> Your company becomes visible in
              searches, and customers can make direct contact via your profile
              page.
            </li>
            <li>
              <b>We showcase your company:</b> With Mittanbud's profile page and
              homepage, you can display your logo, employees, photos and much more.
              Then it will be easy to create a good first impression.
            </li>
          </ul>
  
          <h4 className="text-lg font-bold mt-6 text-gray-900">
            See experiences from satisfied companies
          </h4>
        </div>
  
        {/* Placeholder Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6 max-w-6xl mx-auto">
          {[...Array(3)].map((_, idx) => (
            <div
              key={idx}
              className="bg-gray-200 h-44 md:h-40 rounded-md shadow-sm"
            />
          ))}
        </div>
      </div>
    );
  }
  