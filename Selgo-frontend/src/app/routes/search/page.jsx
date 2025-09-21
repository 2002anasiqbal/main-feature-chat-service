"use client";
import { useState, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Layout from '@/components/layout/Layout';
import AdvancedSearch from '@/components/search/AdvancedSearch';
import MapView from '@/components/map/MapView';
import { FavoriteButton } from '@/components/favorites/FavoritesManager';

// Import all services
import  carService  from '@/services/carService';
import  propertyService  from '@/services/propertyService';
import  jobService  from '@/services/jobService';
import  travelService  from '@/services/travelService';
import  electronicsService  from '@/services/electronicsService';
import  boatService  from '@/services/boatService';
import  motorcycleService  from '@/services/motorcycleService';
import  commercialVehicleService  from '@/services/commercialVehicleService';
import  carAuctionService  from '@/services/carAuctionService';
import  holidayRentalService  from '@/services/holidayRentalService';

const SearchResultsContent = () => {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid'); // 'grid', 'list', 'map'
  const [totalResults, setTotalResults] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [filters, setFilters] = useState({});

  // Extract search parameters
  useEffect(() => {
    const params = {};
    searchParams.forEach((value, key) => {
      params[key] = value;
    });
    setFilters(params);
    setCurrentPage(1);
    performSearch(params);
  }, [searchParams]);

  const performSearch = async (searchFilters, page = 1) => {
    setLoading(true);
    try {
      const searchPromises = [];
      const services = [
        { service: carService, method: 'searchCars', category: 'cars' },
        { service: propertyService, method: 'searchProperties', category: 'properties' },
        { service: jobService, method: 'searchJobs', category: 'jobs' },
        { service: travelService, method: 'searchTravelListings', category: 'travel' },
        { service: electronicsService, method: 'searchElectronics', category: 'electronics' },
        { service: boatService, method: 'searchBoats', category: 'boats' },
        { service: motorcycleService, method: 'searchMotorcycles', category: 'motorcycles' },
        { service: commercialVehicleService, method: 'searchCommercialVehicles', category: 'commercialVehicles' },
        { service: carAuctionService, method: 'searchAuctions', category: 'carAuctions' },
        { service: holidayRentalService, method: 'searchHolidayRentals', category: 'holidayRentals' }
      ];

      // If category is specified, only search that category
      const categoriesToSearch = searchFilters.category && searchFilters.category !== 'All Categories'
        ? services.filter(s => s.category === getCategoryKey(searchFilters.category))
        : services;

      const searchResults = await Promise.allSettled(
        categoriesToSearch.map(async ({ service, method, category }) => {
          try {
            const params = {
              ...searchFilters,
              page,
              per_page: 20
            };
            const result = await service[method](params);
            return {
              category,
              items: result.items || result.results || [],
              total: result.total || 0
            };
          } catch (error) {
            console.error(`Error searching ${category}:`, error);
            return { category, items: [], total: 0 };
          }
        })
      );

      // Combine all results
      const allResults = [];
      let totalCount = 0;

      searchResults.forEach((result) => {
        if (result.status === 'fulfilled') {
          const { category, items, total } = result.value;
          allResults.push(...items.map(item => ({ ...item, type: category })));
          totalCount += total;
        }
      });

      // Sort results by relevance/date
      allResults.sort((a, b) => {
        if (searchFilters.sortBy === 'price_asc') return (a.price || 0) - (b.price || 0);
        if (searchFilters.sortBy === 'price_desc') return (b.price || 0) - (a.price || 0);
        if (searchFilters.sortBy === 'oldest') return new Date(a.created_at) - new Date(b.created_at);
        return new Date(b.created_at) - new Date(a.created_at); // newest first by default
      });

      setResults(allResults);
      setTotalResults(totalCount);
    } catch (error) {
      console.error('Error performing search:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryKey = (categoryName) => {
    const categoryMap = {
      'Cars': 'cars',
      'Property': 'properties',
      'Jobs': 'jobs',
      'Travel': 'travel',
      'Electronics': 'electronics',
      'Boats': 'boats',
      'Motorcycles': 'motorcycles',
      'Commercial Vehicles': 'commercialVehicles',
      'Car Auctions': 'carAuctions',
      'Holiday Rentals': 'holidayRentals'
    };
    return categoryMap[categoryName] || categoryName.toLowerCase();
  };

  const handleSearch = (newFilters) => {
    const searchParams = new URLSearchParams(newFilters);
    router.push(`/routes/search?${searchParams.toString()}`);
  };

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
    
    const basePath = routeMap[item.type] || '/routes';
    router.push(`${basePath}/${item.id}`);
  };

  const renderGridView = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {results.map((item, index) => (
        <div 
          key={`${item.type}-${item.id}-${index}`}
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => handleItemClick(item)}
        >
          {/* Image */}
          <div className="relative aspect-w-16 aspect-h-12 bg-gray-200">
            {item.images && item.images.length > 0 ? (
              <img
                src={item.images[0].image_url}
                alt={item.title}
                className="w-full h-48 object-cover"
              />
            ) : (
              <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
                <span className="text-gray-400">No Image</span>
              </div>
            )}
            
            {/* Category Badge */}
            <div className="absolute top-2 left-2">
              <span className="px-2 py-1 text-xs font-semibold rounded-full bg-teal-100 text-teal-800 capitalize">
                {item.type}
              </span>
            </div>

            {/* Favorite Button */}
            <div className="absolute top-2 right-2">
              <FavoriteButton 
                item={item} 
                category={item.type}
                size="sm"
                className="bg-white bg-opacity-75 rounded-full"
              />
            </div>
          </div>

          {/* Content */}
          <div className="p-4">
            <h3 className="font-semibold text-lg text-gray-900 mb-2 line-clamp-2">
              {item.title}
            </h3>
            
            <div className="flex items-center justify-between mb-2">
              <span className="text-xl font-bold text-teal-600">
                ${item.price?.toLocaleString() || 'N/A'}
              </span>
            </div>

            <div className="text-sm text-gray-600 mb-2">
              <p>{item.location}</p>
              {item.description && (
                <p className="line-clamp-2 mt-1">{item.description}</p>
              )}
            </div>

            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>{new Date(item.created_at).toLocaleDateString()}</span>
              {item.views && <span>{item.views} views</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  const renderListView = () => (
    <div className="space-y-4">
      {results.map((item, index) => (
        <div 
          key={`${item.type}-${item.id}-${index}`}
          className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
          onClick={() => handleItemClick(item)}
        >
          <div className="flex">
            {/* Image */}
            <div className="w-48 h-32 bg-gray-200 flex-shrink-0">
              {item.images && item.images.length > 0 ? (
                <img
                  src={item.images[0].image_url}
                  alt={item.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                  <span className="text-gray-400">No Image</span>
                </div>
              )}
            </div>

            {/* Content */}
            <div className="flex-1 p-4">
              <div className="flex justify-between items-start mb-2">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-lg text-gray-900">
                      {item.title}
                    </h3>
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-teal-100 text-teal-800 capitalize">
                      {item.type}
                    </span>
                  </div>
                  <p className="text-xl font-bold text-teal-600 mb-2">
                    ${item.price?.toLocaleString() || 'N/A'}
                  </p>
                </div>
                <FavoriteButton 
                  item={item} 
                  category={item.type}
                  size="sm"
                />
              </div>

              <div className="text-sm text-gray-600 mb-2">
                <p>{item.location}</p>
                {item.description && (
                  <p className="line-clamp-2 mt-1">{item.description}</p>
                )}
              </div>

              <div className="flex items-center justify-between text-xs text-gray-500">
                <span>{new Date(item.created_at).toLocaleDateString()}</span>
                {item.views && <span>{item.views} views</span>}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  if (loading) {
    return (
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-teal-500"></div>
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
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Search Results</h1>
            <p className="text-gray-600">
              {totalResults > 0 
                ? `Found ${totalResults.toLocaleString()} results`
                : 'No results found'
              }
            </p>
          </div>

          {/* Search Bar */}
          <div className="mb-8">
            <AdvancedSearch 
              onSearch={handleSearch}
              initialFilters={filters}
            />
          </div>

          {/* View Mode Toggle */}
          <div className="flex justify-between items-center mb-6">
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium text-gray-700">View:</span>
              <div className="flex rounded-lg border border-gray-300">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-2 text-sm font-medium rounded-l-lg ${
                    viewMode === 'grid'
                      ? 'bg-teal-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Grid
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3 py-2 text-sm font-medium ${
                    viewMode === 'list'
                      ? 'bg-teal-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  List
                </button>
                <button
                  onClick={() => setViewMode('map')}
                  className={`px-3 py-2 text-sm font-medium rounded-r-lg ${
                    viewMode === 'map'
                      ? 'bg-teal-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  Map
                </button>
              </div>
            </div>
          </div>

          {/* Results */}
          {results.length > 0 ? (
            <>
              {viewMode === 'grid' && renderGridView()}
              {viewMode === 'list' && renderListView()}
              {viewMode === 'map' && (
                <MapView 
                  items={results.filter(item => item.latitude && item.longitude)}
                  height="600px"
                  onMarkerClick={handleItemClick}
                />
              )}
            </>
          ) : (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
              <p className="text-gray-600">Try adjusting your search criteria or browse categories.</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

const SearchResultsPage = () => {
  return (
    <Suspense fallback={
      <Layout>
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-teal-500"></div>
        </div>
      </Layout>
    }>
      <SearchResultsContent />
    </Suspense>
  );
};

export default SearchResultsPage;