import EvaluationCard from "@/components/mt-tender/plummer/EvaluationCard";

const housingEvalData = Array(12).fill({
  id: Math.random(),
  rating: 4,
  title: "Replace stop tap and water heater",
  text: "Good and professionally done job. Pleasant professional. Somewhat disappointed with documentation work.",
  date: "Nov. 2024",
  author: "Knut S.",
  company: "—", // Optional if not shown
  location: "Oslo"
});

export default function HousingEvaluationsSection() {
  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <h2 className="text-center text-xl md:text-2xl font-semibold text-gray-900">
          Work carried out in a housing association at Mittanbud
        </h2>
        <p className="text-center text-sm md:text-base text-gray-700 mt-1 mb-10">
          See previously completed jobs in housing associations and condominiums
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {housingEvalData.map((item, idx) => (
            <EvaluationCard key={idx} data={item} />
          ))}
        </div>
      </div>
    </section>
  );
}