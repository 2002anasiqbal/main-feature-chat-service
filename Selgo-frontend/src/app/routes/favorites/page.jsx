"use client";
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import { FavoritesList, useFavorites } from '@/components/favorites/FavoritesManager';
import useAuthStore from '@/store/store';

const FavoritesPage = () => {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();
  const { getAllFavorites, getFavoritesByCategory, clearAllFavorites, getFavoritesCount } = useFavorites();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showClearConfirm, setShowClearConfirm] = useState(false);

  const categories = [
    { key: 'all', label: 'All Favorites', count: getFavoritesCount() },
    { key: 'cars', label: 'Cars', count: getFavoritesCount('cars') },
    { key: 'properties', label: 'Properties', count: getFavoritesCount('properties') },
    { key: 'jobs', label: 'Jobs', count: getFavoritesCount('jobs') },
    { key: 'travel', label: 'Travel', count: getFavoritesCount('travel') },
    { key: 'electronics', label: 'Electronics', count: getFavoritesCount('electronics') },
    { key: 'boats', label: 'Boats', count: getFavoritesCount('boats') },
    { key: 'motorcycles', label: 'Motorcycles', count: getFavoritesCount('motorcycles') },
    { key: 'commercialVehicles', label: 'Commercial Vehicles', count: getFavoritesCount('commercialVehicles') },
    { key: 'carAuctions', label: 'Car Auctions', count: getFavoritesCount('carAuctions') },
    { key: 'holidayRentals', label: 'Holiday Rentals', count: getFavoritesCount('holidayRentals') }
  ];

  const handleItemClick = (item) => {
    const routeMap = {
      cars: '/routes/cars',
      properties: '/routes/property',
      jobs: '/routes/jobs',
      travel: '/routes/travel',
      electronics: '/routes/electronics',
      boats: '/routes/boat',
      motorcycles: '/routes/motor-cycle',
      commercialVehicles: '/routes/commercial-vehicles',
      carAuctions: '/routes/car-auctions',
      holidayRentals: '/routes/holiday-rentals'
    };
    
    const basePath = routeMap[item.category || item.type] || '/routes';
    router.push(`${basePath}/${item.id}`);
  };

  const handleClearAll = async () => {
    const success = await clearAllFavorites();
    if (success) {
      setShowClearConfirm(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <Layout>
        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Please log in to view favorites</h3>
              <p className="text-gray-600 mb-6">You need to be logged in to save and view your favorite items.</p>
              <button
                onClick={() => router.push('/routes/auth/login')}
                className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
              >
                Log In
              </button>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-4">My Favorites</h1>
                <p className="text-gray-600">
                  {getFavoritesCount() > 0 
                    ? `You have ${getFavoritesCount()} favorite items`
                    : 'No favorite items yet'
                  }
                </p>
              </div>
              {getFavoritesCount() > 0 && (
                <button
                  onClick={() => setShowClearConfirm(true)}
                  className="px-4 py-2 text-red-600 border border-red-300 rounded-lg hover:bg-red-50 transition-colors"
                >
                  Clear All
                </button>
              )}
            </div>
          </div>

          {/* Category Tabs */}
          <div className="mb-8">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8 overflow-x-auto">
                {categories.map((category) => (
                  <button
                    key={category.key}
                    onClick={() => setSelectedCategory(category.key)}
                    className={`py-2 px-1 border-b-2 font-medium text-sm whitespace-nowrap ${
                      selectedCategory === category.key
                        ? 'border-teal-500 text-teal-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    {category.label}
                    {category.count > 0 && (
                      <span className="ml-2 bg-gray-100 text-gray-600 py-0.5 px-2 rounded-full text-xs">
                        {category.count}
                      </span>
                    )}
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Favorites List */}
          <FavoritesList 
            category={selectedCategory === 'all' ? null : selectedCategory}
            onItemClick={handleItemClick}
          />

          {/* Clear All Confirmation Modal */}
          {showClearConfirm && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Clear All Favorites</h3>
                <p className="text-gray-600 mb-6">
                  Are you sure you want to remove all items from your favorites? This action cannot be undone.
                </p>
                <div className="flex justify-end space-x-4">
                  <button
                    onClick={() => setShowClearConfirm(false)}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleClearAll}
                    className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    Clear All
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default FavoritesPage;