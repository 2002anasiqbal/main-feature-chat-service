"use client";
import React from 'react';
import GenericCardCollection from '@/components/GenericCardCollection';

const cardData = [
  {
    items: [
      { tag: 'Plumber', icon: '14.svg', route: '/routes/plumber' },
      { tag: 'Electrician', icon: '15.svg', route: '/routes/electrician' },
      { tag: 'Carpenter', icon: '16.svg', route: '/routes/carpenter' },
      { tag: 'Cleaning', icon: '17.svg', route: '/routes/cleaning' },
      { tag: 'Renovator', icon: '18.svg', route: '/routes/renovator' },
      { tag: 'Car washer', icon: '19.svg', route: '/routes/car-washer' }
    ]
  },
  {
    items: [
      { tag: 'Contractor', icon: '20.svg', route: '/routes/contractor' },
      { tag: 'Painter', icon: '21.svg', route: '/routes/painter' },
      { tag: 'Moving agency', icon: '22.svg', route: '/routes/moving-agency' },
      { tag: 'Housing association', icon: '23.svg', route: '/routes/housing-association' },
      { tag: 'Large project', icon: '24.svg', route: '/routes/large-project' },
      { tag: 'All categories', icon: '25.svg', route: '/routes/all-categories' }
    ]
  }
];

const rowStyles = {
  0: {
    gridCols: 'grid-cols-2 xs:grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6',
    gap: 'gap-3 xs:gap-4 sm:gap-5',
    marginBottom: 'mb-4'
  },
  1: {
    gridCols: 'grid-cols-2 xs:grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-6',
    gap: 'gap-3 xs:gap-4 sm:gap-5'
  }
};

export default function PopularProjects() {
  return (
    <div className="w-full max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Projects</h2>
      <GenericCardCollection 
        rows={cardData} 
        rowStyles={rowStyles} 
        imageBasePath="/assets/my-tender/" 
        size="h-16 w-16 xs:h-20 xs:w-20 sm:h-24 sm:w-24 md:h-28 md:w-28 lg:h-32 lg:w-32"
      />
    </div>
  );
}