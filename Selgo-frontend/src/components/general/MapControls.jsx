"use client";
import { useMap } from "react-leaflet";

export default function MapControls() {
  const map = useMap();

  return (
    <div className="absolute top-2 right-2 flex flex-col gap-2">
      <button
        onClick={() => map.zoomIn()}
        className="p-2 bg-white border rounded-md shadow-md"
      >
        ➕
      </button>
      <button
        onClick={() => map.zoomOut()}
        className="p-2 bg-white border rounded-md shadow-md"
      >
        ➖
      </button>
    </div>
  );
}
