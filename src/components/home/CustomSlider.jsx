"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";

const images = Array.from({ length: 8 }, (_, i) => `/assets/swiper/${i + 1}.jpg`);

const CustomSlider = () => {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  // Parent container style
  const outerContainerStyle = {
    position: "relative",
    width: "100%",
    height: "50vh",
    overflow: "hidden"
  };
  
  // Actual slider container
  const sliderContainerStyle = {
    width: "100%",
    height: "100%",
    position: "relative"
  };
  
  // Bottom concave mask
  const bottomConcaveMaskStyle = {
    position: "absolute",
    bottom: "-25%",
    left: "0",
    width: "100%",
    height: "50%",
    backgroundColor: "white", // Match your page background color
    borderTopLeftRadius: "50%",
    borderTopRightRadius: "50%",
    zIndex: "10"
  };
  
  // Top concave mask
  const topConcaveMaskStyle = {
    position: "absolute",
    top: "-25%",
    left: "0",
    width: "100%",
    height: "50%",
    backgroundColor: "white", // Match your page background color
    borderBottomLeftRadius: "50%",
    borderBottomRightRadius: "50%",
    zIndex: "10"
  };

  return (
    <div style={outerContainerStyle}>
      <div style={sliderContainerStyle}>
        <div
          className="flex transition-transform duration-500 ease-in-out"
          style={{ transform: `translateX(-${currentIndex * 25}%)` }}
        >
          {images.concat(images).map((src, index) => (
            <div key={index} className="w-1/4 h-[50vh] flex-shrink-0">
              <Image
                src={src}
                alt={`Slide ${index + 1}`}
                width={500}
                height={500}
                className="w-full h-full object-cover"
              />
            </div>
          ))}
        </div>
        
        {/* Bottom concave mask */}
        <div style={bottomConcaveMaskStyle}></div>
        
        {/* Top concave mask */}
        <div style={topConcaveMaskStyle}></div>
      </div>
    </div>
  );
};

export default CustomSlider;