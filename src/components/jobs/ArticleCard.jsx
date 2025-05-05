"use client";
import Image from "next/image";

export default function ArticleCard({ imageUrl, title, onClick }) {
  return (
    <div
      onClick={onClick}
      className="flex items-center gap-4 cursor-pointer hover:bg-gray-50 p-2 rounded-lg transition"
    >
      <div className="min-w-[60px] min-h-[60px] relative rounded-lg overflow-hidden">
        <Image
          src={imageUrl}
          alt={title}
          fill
          className="object-cover"
        />
      </div>
      <p className="text-gray-700 text-sm font-medium">{title}</p>
    </div>
  );
}