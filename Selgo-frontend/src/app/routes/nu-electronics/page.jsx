// components/Navigation.jsx
import { Babylonica } from 'next/font/google'

const babylonica = Babylonica({
    weight: '400',
    subsets: ['latin'],
})
import Link from 'next/link';
// import { ShoppingCart } from 'lucide-react';
import { IoCart } from 'react-icons/io5';
import RecentlyVisitedSlider from '@/components/general/RecentlyVisitedSlider';
import WarrantyBanner from '@/components/nu-electronics/WarrantyBanner';
import Page from '@/components/GenerateCard';
import UsedProductInfo from '@/components/nu-electronics/UsedProductInfo';

const Navigation = () => {
    const categories = [
        { name: 'Tablet', href: '/category/tablet' },
        { name: 'Smartwatch', href: '/category/smartwatch' },
        { name: 'Iphone', href: '/category/iphone' },
        { name: 'Ipad', href: '/category/ipad' },
        { name: 'Airpods', href: '/category/airpods' },
        { name: 'Samsung', href: '/category/samsung' },
        { name: 'Macbook', href: '/category/macbook' },
        { name: 'Mobile', href: '/category/mobile' }
    ];

    return (
        <div className="w-full">
            {/* Header with logo and cart icon */}
            <div className="bg-teal-700 text-white p-4 flex px-20 py-10 justify-between items-center">
                <div className="text-xl italic font-light">
                    <span className={`text-6xl ${babylonica.className}`}>
                        Now used with warranty
                    </span>

                </div>
                <Link href="/routes/nu-electronics/cart">
                    <button className="text-white">
                        <IoCart className='text-3xl cursor-pointer' />
                    </button>
                </Link>
            </div>

            {/* Category navigation */}
            <div className="flex flex-wrap justify-center gap-2 py-4 px-8 ">
                {categories.map((category) => (
                    <Link key={category.name} href={category.href}>
                        <button className="bg-teal-500 hover:bg-teal-600 text-white py-2 px-4 rounded transition-colors duration-200 min-w-[100px]">
                            {category.name}
                        </button>
                    </Link>
                ))}
            </div>
            <RecentlyVisitedSlider heading='' />
            <WarrantyBanner />

            <h2 className="text-lg md:text-xl font-semibold mb-2 md:mb-4 text-gray-800 px-2">
                Popular Models
            </h2>
            <Page />
            <UsedProductInfo />
        </div>
    );
};

export default Navigation;