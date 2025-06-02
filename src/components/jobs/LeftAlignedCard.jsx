"use client";
import Image from "next/image";

export default function LeftAlignedCard({ icon, label, title, subtitle }) {
  return (
    <div className="bg-white rounded-xl shadow p-4 w-full max-w-md">
      <div className="flex items-center gap-2 mb-2">
        <Image src={icon} alt={label} width={20} height={20} />
        <span className="text-xs font-semibold text-gray-500 uppercase">{label}</span>
      </div>
      <h2 className="text-lg font-bold text-gray-800 mb-1">{title}</h2>
      <p className="text-sm text-gray-600">{subtitle}</p>
    </div>
  );
}