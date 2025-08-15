"use client";
export default function PlumberPricingInfo() {
    return (
      <section className="bg-white pb-12 space-y-12">
        {/* Section 1 */}
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            What affects the cost of a plumber?
          </h2>
          <p className="text-gray-700 mb-4">
            Projects involving plumbers are often more expensive than other
            remodeling projects, and the biggest expenses are related to the type
            of projects they work on. Common price drivers for projects carried
            out by plumbers are:
          </p>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>If the job requires special tools/equipment</li>
            <li>Procurement of materials and equipment for water and sewage</li>
            <li>If the job requires the laying of a membrane</li>
            <li>Moving, rehabilitating or changing water and drainage pipes</li>
            <li>
              Piping for new buildings, additions and extensions and laying of
              new pipes
            </li>
            <li>Whether heating cables are to be taken into account</li>
            <li>Tiling or other surface treatments</li>
            <li>
              Acquisition and installation of bathroom or kitchen fittings
            </li>
          </ul>
        </div>
  
        {/* Section 2 */}
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Why is the hourly rate for plumbers higher than other craftsmen?
          </h2>
          <p className="text-gray-700 mb-4">
            The hourly rate for a plumber will often be slightly higher than for
            other types of craftsman. This is because the plumber must have
            additional insurance in case something goes wrong.
          </p>
          <p className="text-gray-700">
            Repairing a leak is not necessarily something a plumber earns a lot
            from doing, but should the repair not last and the damage first
            occurs – then this will be a far greater cost than what they earned on
            the job. To ensure that plumbers can cover such cases without having
            to put a mortgage on their own home, plumbers therefore have
            additional insurance that must be covered through the jobs they carry
            out.
          </p>
        </div>
  
        {/* CTA */}
        <div className="bg-[#e5f3f3] p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between rounded-md">
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              Find skilled plumbers
            </h3>
            <p className="text-sm text-gray-600">
              Register the job with Mittanbud
            </p>
          </div>
          <button className="mt-4 sm:mt-0 bg-teal-700 text-white px-6 py-2 rounded-md hover:bg-teal-800 transition">
            Get started here
          </button>
        </div>
      </section>
    );
  }
  