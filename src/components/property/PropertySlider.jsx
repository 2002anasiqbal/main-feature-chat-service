"use client";
import React, { useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import Image from "next/image";
import { FaChevronLeft } from "react-icons/fa";
import Link from "next/link";

const PropertySlider = ({
  images = [], // Dynamic images
  height = "h-[300px] md:h-[500px]", // Default height
  width = "w-full max-w-4xl", // Default width
  loop = true,
  returnUrl = "/", // Where the back button should link to
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);

  // Use placeholder images if none provided
  const defaultImages = [
    "https://picsum.photos/800/500?random=1",
    "https://picsum.photos/800/500?random=2",
    "https://picsum.photos/800/500?random=3",
    "https://picsum.photos/800/500?random=4",
    "https://picsum.photos/800/500?random=5",
  ];

  const imageList = images.length > 0 ? images : defaultImages;
  const totalImages = imageList.length;
  const currentIndexFormatted = String(currentIndex + 1).padStart(2, "0");
  const totalImagesFormatted = String(totalImages).padStart(2, "0");

  return (
    <div className="relative w-full">
      {/* Header with back button and counter */}
      <div className="flex justify-between items-center p-4">
        <Link href={returnUrl} className="text-gray-800">
          <FaChevronLeft size={24} />
        </Link>
        <div className="text-gray-800 font-medium">
          <span className="font-bold text-xl">{currentIndexFormatted}</span>
          <span className="text-gray-400 text-xl"> / {totalImagesFormatted}</span>
        </div>
      </div>

      {/* Swiper Slider */}
      <Swiper
        modules={[Navigation, Pagination]}
        slidesPerView={1}
        loop={loop}
        pagination={{
          clickable: true,
          el: '.swiper-pagination',
          bulletClass: 'swiper-pagination-bullet',
          bulletActiveClass: 'swiper-pagination-bullet-active'
        }}
        onSlideChange={(swiper) => setCurrentIndex(swiper.realIndex)}
        className="relative w-full overflow-hidden"
      >
        {imageList.map((image, index) => (
          <SwiperSlide key={index}>
            <div className={`relative w-full ${height}`}>
              <Image 
                src={image} 
                alt={`Property Image ${index + 1}`} 
                layout="fill" 
                objectFit="cover" 
              />
            </div>
          </SwiperSlide>
        ))}
      </Swiper>

      {/* Custom pagination dots */}
      <div className="swiper-pagination flex justify-center gap-2 mt-4"></div>

      {/* Custom styles for pagination dots */}
      <style jsx global>{`
        .swiper-pagination {
          position: relative;
          bottom: 0;
          margin-top: 12px;
        }
        .swiper-pagination-bullet {
          width: 8px;
          height: 8px;
          background-color: #ccc;
          opacity: 1;
          display: inline-block;
          border-radius: 50%;
          margin: 0 4px;
        }
        .swiper-pagination-bullet-active {
          background-color: #009688;
          width: 8px;
          height: 8px;
        }
      `}</style>
    </div>
  );
};

export default PropertySlider;