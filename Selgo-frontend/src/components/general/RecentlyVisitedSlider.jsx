"use client";
import React, { useRef, useEffect, useState } from "react";
import { Swiper, SwiperSlide } from "swiper/react";
import { Navigation, Pagination, EffectCoverflow } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";
import "swiper/css/effect-coverflow";
import Image from "next/image";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

// Default images if none provided
const defaultImages = [
  "https://picsum.photos/800/500?random=1",
  "https://picsum.photos/800/500?random=2",
  "https://picsum.photos/800/500?random=3",
  "https://picsum.photos/800/500?random=4",
  "https://picsum.photos/800/500?random=5",
];

const RecentlyVisitedSlider = ({
  images = [],
  loop = true,
  heading = "Recently Visited Property"
}) => {
  const imageList = images.length ? images : defaultImages;
  const swiperRef = useRef(null);
  const [slidesPerView, setSlidesPerView] = useState(3);
  
  // Update slides per view based on screen size
  useEffect(() => {
    const handleResize = () => {
      if (window.innerWidth < 640) {
        setSlidesPerView(1);
      } else if (window.innerWidth < 1024) {
        setSlidesPerView(2);
      } else {
        setSlidesPerView(3);
      }
    };
    
    // Set initial value
    handleResize();
    
    // Add resize listener
    window.addEventListener('resize', handleResize);
    
    // Clean up
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  // Create duplicate slides if there are fewer than slidesPerView*2+1 images
  const getExtendedImageList = () => {
    if (imageList.length >= slidesPerView * 2 + 1) {
      return imageList;
    }
    return [...imageList, ...imageList, ...imageList];
  };
  
  const extendedImageList = getExtendedImageList();
  
  useEffect(() => {
    if (swiperRef.current && swiperRef.current.swiper) {
      const swiper = swiperRef.current.swiper;
      swiper.update();
      if (loop) {
        swiper.loopCreate();
      }
    }
  }, [loop, slidesPerView]);
  
  // No type assertion needed since we're using plain JavaScript.
  const SwiperComponent = Swiper;
  
  return (
    <div className="w-full">
      {/* Title */}
      <h2 className="text-lg md:text-xl font-semibold mb-2 md:mb-4 text-gray-800 px-2">
        {heading}
      </h2>
      
      <div className="relative slider-container">
        {/* Swiper Container */}
        <SwiperComponent
          ref={swiperRef}
          modules={[Navigation, Pagination, EffectCoverflow]}
          effect="coverflow"
          grabCursor={true}
          centeredSlides={true}
          slidesPerView={slidesPerView}
          initialSlide={Math.floor(extendedImageList.length / 4)}
          coverflowEffect={{
            rotate: 0,
            stretch: 0,
            depth: 100,
            modifier: 2.5,
            slideShadows: false,
          }}
          spaceBetween={15}
          loop={loop}
          loopAdditionalSlides={slidesPerView * 2}
          navigation={{
            nextEl: ".next-btn",
            prevEl: ".prev-btn",
          }}
          pagination={{
            el: ".swiper-pagination",
            clickable: true,
          }}
          className="stepped-swiper"
          onSlideChange={() => {
            setTimeout(() => {
              const activeSlides = document.querySelectorAll(
                ".swiper-slide-active img, .swiper-slide-prev img, .swiper-slide-next img"
              );
              activeSlides.forEach((slide) => {
                slide.style.borderRadius = "12px";
              });
            }, 10);
          }}
          breakpoints={{
            320: { slidesPerView: 1, spaceBetween: 10 },
            640: { slidesPerView: 2, spaceBetween: 15 },
            1024: { slidesPerView: 3, spaceBetween: 20 },
            1280: { slidesPerView: 3, spaceBetween: 30 },
          }}
        >
          {extendedImageList.map((imgUrl, index) => (
            <SwiperSlide key={index} className="rounded-xl overflow-hidden">
              <div className="slide-content rounded-xl overflow-hidden">
                <Image
                  src={imgUrl}
                  alt={`Visited property ${index + 1}`}
                  width={500}
                  height={240}
                  style={{
                    width: "100%",
                    height: "180px",
                    objectFit: "cover",
                    borderRadius: "12px",
                  }}
                  className="slide-image rounded-xl"
                />
              </div>
            </SwiperSlide>
          ))}
        </SwiperComponent>
        
        {/* Navigation Arrows - Hidden on mobile */}
        <button className="prev-btn absolute top-1/2 left-1 md:left-4 -translate-y-1/2 bg-white text-gray-800 p-1 md:p-2 rounded-full shadow-md hover:bg-gray-100 z-20 hidden sm:block">
          <FaChevronLeft size={16} className="md:text-lg" />
        </button>
        <button className="next-btn absolute top-1/2 right-1 md:right-4 -translate-y-1/2 bg-white text-gray-800 p-1 md:p-2 rounded-full shadow-md hover:bg-gray-100 z-20 hidden sm:block">
          <FaChevronRight size={16} className="md:text-lg" />
        </button>
        
        {/* Pagination Dots */}
        <div className="swiper-pagination flex justify-center mt-4 md:mt-8" />
      </div>
      
      <style jsx global>{`
        .slider-container {
          padding: 20px 0;
          overflow: hidden;
        }
        
        .swiper-slide {
          transition: all 0.3s ease;
          height: 180px;
          border-radius: 12px !important;
          overflow: hidden;
        }
        
        .slide-content {
          width: 100%;
          height: 100%;
          border-radius: 12px !important;
          overflow: hidden;
        }
        
        .slide-image {
          border-radius: 12px !important;
        }
        
        .swiper-slide-active {
          transform: translateY(0) scale(1);
          z-index: 3;
        }
        
        .swiper-slide-prev,
        .swiper-slide-next {
          transform: translateY(10px) scale(0.9);
          opacity: 1;
          z-index: 2;
        }
        
        .swiper-slide:not(.swiper-slide-active):not(.swiper-slide-prev):not(.swiper-slide-next) {
          transform: translateY(20px) scale(0.85);
          opacity: 1;
          z-index: 1;
        }
        
        .swiper-pagination {
          position: relative !important;
          bottom: 0 !important;
          margin-top: 20px;
        }
        
        .swiper-pagination-bullet {
          width: 6px;
          height: 6px;
          background-color: #ccc;
          opacity: 1;
          display: inline-block;
          border-radius: 50%;
          margin: 0 4px;
        }
        
        .swiper-pagination-bullet-active {
          background-color: #6366f1;
          width: 8px;
          height: 8px;
        }
        
        @media (min-width: 768px) {
          .swiper-slide {
            height: 200px;
          }
          
          .slide-image {
            height: 200px !important;
          }
          
          .swiper-pagination-bullet {
            width: 8px;
            height: 8px;
          }
          
          .swiper-pagination-bullet-active {
            width: 10px;
            height: 10px;
          }
        }
        
        @media (min-width: 1024px) {
          .swiper-slide {
            height: 220px;
          }
          
          .slide-image {
            height: 220px !important;
          }
          
          .swiper-slide-prev,
          .swiper-slide-next {
            transform: translateY(15px) scale(0.9);
          }
          
          .swiper-slide:not(.swiper-slide-active):not(.swiper-slide-prev):not(.swiper-slide-next) {
            transform: translateY(30px) scale(0.85);
          }
        }
        
        @media (min-width: 1280px) {
          .swiper-slide {
            height: 240px;
          }
          
          .slide-image {
            height: 240px !important;
          }
        }
      `}</style>
    </div>
  );
};

export default RecentlyVisitedSlider;