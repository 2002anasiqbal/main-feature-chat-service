import FAQ from "@/components/general/FAQ";
export default function HousingAssociationTips() {
  const cards = Array(4).fill({
    title: "Typical projects in Housing Associations",
  });

  return (
    <section className="bg-white pt-12 pb-20 px-4">
      <div className="max-w-6xl mx-auto text-center space-y-4">
        <h2 className="text-xl sm:text-2xl font-semibold text-gray-900">
          Find craftsmen for small and large projects in the housing association
        </h2>
        <p className="text-sm text-gray-700">
          Whether you need to change all the windows, or just change the lamp in the hallway – you will find the solid professionals at Mittanbud!
        </p>

        <button className="bg-teal-600 hover:bg-teal-700 text-white font-medium px-6 py-2 rounded mt-4">
          Describe the Job
        </button>
      </div>

      <div className="bg-teal-100 mt-16 py-10 px-4">
        <div className="max-w-5xl mx-auto text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Get tips and advice for your project in the housing association or housing association
          </h2>
          <p className="text-sm text-gray-700 mb-8">
            Here you will find useful information for projects in housing associations and condominiums
          </p>

        </div>
      </div>
      <div className="py-10 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <div key={i} className="text-left">
            <div className="bg-gray-300 rounded-md h-64 w-full" />
            <p className="font-semibold text-sm mt-3 text-gray-900">
              {card.title}
            </p>
          </div>
        ))}
      </div>
      <div className="max-w-5xl mx-auto px-4 mt-16">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-900">
            Frequently asked questions
          </h3>
          <p className="text-sm text-gray-700">
            Here we answer the most common questions about assignments in housing associations.
          </p>
        </div>
        <FAQ />
      </div>
    </section>
  );
}
