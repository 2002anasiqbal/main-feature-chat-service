import Image from "next/image";

export default function ForHousingAssociations() {
  return (
    <div className="bg-[#e5f3f3] rounded-lg overflow-hidden w-full max-w-xs text-gray-900">
      {/* Top Image */}
      <Image
        src="/assets/my-tender/37.svg"
        alt="Modern housing"
        width={500}
        height={150}
        className="w-full object-cover h-auto"
      />

      {/* Content */}
      <div className="p-4 space-y-3">
        <h2 className="text-lg font-semibold leading-tight">
          Også for borettslag og sameier
        </h2>
        <p className="text-sm">
          Mittanbud kan hjelpe borettslag og sameier med å finne dyktige
          håndverkere for små og store prosjekter!
        </p>
        <a
          href="#"
          className="text-sm text-teal-700 font-medium underline"
        >
          Les hvordan vi kan hjelpe borettslag og sameier her
        </a>
      </div>
    </div>
  );
}