"use client";
import AdviceInspiration from '@/components/mt-tender/AdviceInspiration';
// import LatestEvaluationCard from '@/components/mt-tender/LatestEvaluationCard';
import MyTenderHero from '@/components/mt-tender/MyTenderHero';
import PopularProjects from '@/components/mt-tender/PopularProjects';
import TradesmanFinderSection from '@/components/mt-tender/TradesmanFinderSection';
import React, { useRef } from 'react';
// import { FaChevronLeft } from 'react-icons/fa';
// import { FaChevronRight } from 'react-icons/fa';
import HeroAndCategories from './HeroAndCategories';
import HowItWorks from './HowItWorks';
import LatestEvaluations from './LatestEvaluations';
// const evaluations = [
//     {
//         name: 'John Doe',
//         rating: 4.8,
//         review: 'Excellent service, quick turnaround!',
//         job: 'Bathroom renovation',
//         location: 'Oslo',
//         avatar: '/assets/my-tender/user1.jpg',
//     },
//     {
//         name: 'Anna Smith',
//         rating: 5.0,
//         review: 'Very professional and polite.',
//         job: 'Kitchen remodeling',
//         location: 'Bergen',
//         avatar: '/assets/my-tender/user2.jpg',
//     },
//     {
//         name: 'Mikkel Hansen',
//         rating: 4.5,
//         review: 'Happy with the work done.',
//         job: 'Flooring installation',
//         location: 'Trondheim',
//         avatar: '/assets/my-tender/user3.jpg',
//     },
//     {
//         name: 'Emma Larsen',
//         rating: 4.9,
//         review: 'Great communication and quality.',
//         job: 'Painting exterior',
//         location: 'Stavanger',
//         avatar: '/assets/my-tender/user4.jpg',
//     },
// ];

export default function MyTenderMain() {
    const scrollRef = useRef();

    const scrollLeft = () => {
        scrollRef.current.scrollBy({ left: -350, behavior: 'smooth' });
    };

    const scrollRight = () => {
        scrollRef.current.scrollBy({ left: 350, behavior: 'smooth' });
    };
    return (
        <div className="w-full">
            <HeroAndCategories />
            <HowItWorks />
            <LatestEvaluations />
            <PopularProjects />
            <TradesmanFinderSection />
            <MyTenderHero />
            <AdviceInspiration />
        </div>
    );
}
