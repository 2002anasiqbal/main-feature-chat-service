import Image from "next/image";

export default function AreYouAContractor() {
  return (
    <div className="bg-teal-800 text-white rounded-lg overflow-hidden w-full max-w-xs">
      {/* Image Top */}
      <Image
        src="/assets/my-tender/38.svg"
        alt="Contractor measuring"
        width={215}
        height={120}
        className="w-full h-auto object-cover"
      />

      {/* Text Content */}
      <div className="p-4 space-y-2">
        <h2 className="text-lg font-semibold">Er du en håndverker?</h2>
        <p className="text-sm">
          Mittanbud får årlig inn over 220 000 jobber til håndverkere. Vi trenger flere bedrifter som kan ta disse unna!
        </p>

        <a
          href="#"
          className="text-sm text-teal-300 font-medium underline flex items-center gap-1"
        >
          Registrer bedrift →
        </a>
      </div>
    </div>
  );
}
