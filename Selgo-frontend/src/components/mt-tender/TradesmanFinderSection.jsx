"use client";
import React from 'react';
import Image from 'next/image';

const TradesmanFinderSection = () => {
  const features = [
    {
      icon: '26.svg',
      title: 'Reviews you can trust',
      description: 'See real customer reviews on Mittanbud. Only companies that have completed a job are rated.',
      buttonText: 'Learn More'
    },
    {
      icon: '27.svg',
      title: 'Check the company\'s qualifications',
      description: 'Find certifications and qualifications on the company\'s profile.',
      buttonText: 'Learn More'
    },
    {
      icon: '28.svg',
      title: 'Easy to get started',
      description: 'Post your job on Mittanbud and get a quick overview of companies that can do the job for you.',
      buttonText: 'Learn More'
    }
  ];

  return (
    <div className="w-full max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">
          An efficient and safe way to find a tradesman
        </h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Mittanbud regularly checks the companies on the service. In addition, we have made it easier for you to check whether you have chosen the right company for your project:
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-8">
        {features.map((feature, index) => (
          <div 
            key={index} 
            className="flex flex-col text-left space-y-10 p-6 bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 w-full relative"
          >
            <div className="w-10 h-10 flex items-center justify-start mb-2">
              <Image 
                src={`/assets/my-tender/${feature.icon}`} 
                alt={feature.title} 
                width={30} 
                height={30}
                className="object-contain"
              />
            </div>
            <div className="flex-grow">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-gray-600 mb-3">
                {feature.description}
              </p>
            </div>
            <div className="absolute bottom-6 left-6">
              <button className="px-4 py-1.5 text-sm bg-teal-500 text-white rounded-md hover:bg-teal-600 transition-colors duration-300">
                {feature.buttonText}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TradesmanFinderSection;