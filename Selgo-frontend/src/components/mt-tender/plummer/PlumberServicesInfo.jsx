export default function PlumberServicesInfo() {
    return (
      <section className="bg-white py-12 space-y-8">
        {/* Top Section */}
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            What can a plumber do for you?
          </h2>
          <p className="text-gray-700">
            Plumbers perform many different services, ranging from opening
            clogged pipes to major renovation projects for wet rooms. A plumber
            can take on small jobs such as pipe renewal and drain maintenance, or
            extensive jobs such as total renovations where many different
            professional areas are involved.
          </p>
        </div>
  
        {/* Highlighted Box */}
        <div className="bg-[#e5f3f3] p-6 rounded-md text-gray-900">
          <p className="mb-4">
            Depending on what you need help with, plumbers at Mittanbud can help you with:
          </p>
          <ul className="list-disc list-inside space-y-2 text-gray-800">
            <li>Maintenance, rehabilitation and renewal of water and drainage pipes</li>
            <li>Flushing and repairing clogged pipes</li>
            <li>Pipe defrosting</li>
            <li>Pipe welding and repair of cracked water pipes</li>
            <li>Refurbishment and total renovation of wet rooms</li>
            <li>Plumber on duty</li>
          </ul>
        </div>
      </section>
    );
  }
  