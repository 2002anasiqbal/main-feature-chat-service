"use client";
import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";

const LocationMap = ({ heading, latitude, longitude, locationName }) => {
  return (
    <div className="w-full max-w-5xl mx-auto py-6">
      <h2 className="text-3xl font-bold text-gray-900 mb-4">{heading}</h2>
      <div className="w-full h-80 rounded-md overflow-hidden border border-gray-300 shadow-md">
        <MapContainer center={[latitude, longitude]} zoom={6} className="w-full h-full">
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          <Marker position={[latitude, longitude]}>
            <Popup>{locationName}</Popup>
          </Marker>
        </MapContainer>
      </div>
    </div>
  );
};

export default LocationMap;