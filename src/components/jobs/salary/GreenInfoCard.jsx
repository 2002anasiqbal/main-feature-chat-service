"use client";

export default function GreenInfoCard({ title, description }) {
  return (
    <div className="bg-teal-700 text-white p-4 rounded-lg shadow-sm w-full max-w-xs">
      <h3 className="text-base font-semibold mb-2">{title}</h3>
      <p className="text-sm leading-snug">{description}</p>
    </div>
  );
}