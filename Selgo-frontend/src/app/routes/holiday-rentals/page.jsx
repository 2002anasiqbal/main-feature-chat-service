"use client";
import { useState, useEffect } from 'react';
import { holidayRentalService } from '@/services/holidayRentalService';
import Layout from '@/components/layout/Layout';

const HolidayRentalsPage = () => {
  const [rentals, setRentals] = useState([]);
  const [featuredRentals, setFeaturedRentals] = useState([]);
  const [popularDestinations, setPopularDestinations] = useState([]);
  const [rentalTypes, setRentalTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [selectedDestination, setSelectedDestination] = useState('');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [guestCount, setGuestCount] = useState('');
  const [bedrooms, setBedrooms] = useState('');
  const [checkIn, setCheckIn] = useState('');
  const [checkOut, setCheckOut] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (activeTab === 'all') {
      searchRentals();
    }
  }, [selectedType, selectedDestination, sortBy, sortOrder, activeTab]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [rentalsData, featuredData, destinationsData, typesData] = await Promise.all([
        holidayRentalService.searchHolidayRentals({ page: 1, per_page: 20 }),
        holidayRentalService.getFeaturedRentals(8),
        holidayRentalService.getPopularDestinations(),
        holidayRentalService.getAvailableRentalTypes()
      ]);
      
      setRentals(rentalsData.items || []);
      setFeaturedRentals(featuredData.items || []);
      setPopularDestinations(destinationsData.destinations || []);
      setRentalTypes(typesData.types || []);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchRentals = async () => {
    try {
      setLoading(true);
      const searchParams = {
        query: searchQuery,
        rental_type: selectedType,
        destination: selectedDestination,
        price_from: priceRange.min,
        price_to: priceRange.max,
        guests: guestCount,
        bedrooms: bedrooms,
        check_in: checkIn,
        check_out: checkOut,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: 1,
        per_page: 20
      };

      const response = await holidayRentalService.searchHolidayRentals(searchParams);
      setRentals(response.items || []);
    } catch (error) {
      console.error('Error searching rentals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setActiveTab('all');
    searchRentals();
  };

  const addToWishlist = async (rentalId) => {
    try {
      await holidayRentalService.addToWishlist(rentalId);
      // Update UI to show rental is in wishlist
    } catch (error) {
      console.error('Error adding to wishlist:', error);
    }
  };

  const renderRentalCard = (rental) => (
    <div key={rental.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      <div className="relative aspect-w-16 aspect-h-12 bg-gray-200">
        {rental.images && rental.images.length > 0 ? (
          <img
            src={rental.images[0].image_url}
            alt={rental.title}
            className="w-full h-48 object-cover"
          />
        ) : (
          <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">No Image</span>
          </div>
        )}
        
        {/* Featured Badge */}
        {rental.is_featured && (
          <div className="absolute top-2 left-2">
            <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
              FEATURED
            </span>
          </div>
        )}

        {/* Rating */}
        {rental.average_rating && (
          <div className="absolute top-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-xs flex items-center">
            <svg className="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            {rental.average_rating.toFixed(1)}
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-lg text-gray-900 mb-2 line-clamp-2">
          {rental.title}
        </h3>
        
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-sm text-gray-500">From</span>
            <div className="text-2xl font-bold text-teal-600">
              ${rental.price_per_night}/night
            </div>
          </div>
          <div className="text-right">
            <span className="text-sm text-gray-500">Guests</span>
            <div className="text-lg font-semibold text-gray-900">
              {rental.max_guests}
            </div>
          </div>
        </div>

        <div className="text-sm text-gray-600 mb-3">
          <p className="capitalize">{rental.rental_type} • {rental.bedrooms} bed • {rental.bathrooms} bath</p>
          <p>{rental.location}</p>
          <div className="flex items-center mt-1">
            {rental.amenities && rental.amenities.slice(0, 3).map((amenity, index) => (
              <span key={index} className="inline-block bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded mr-1">
                {amenity}
              </span>
            ))}
            {rental.amenities && rental.amenities.length > 3 && (
              <span className="text-xs text-gray-500">+{rental.amenities.length - 3} more</span>
            )}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center text-xs text-gray-500">
            {rental.review_count > 0 && (
              <span>{rental.review_count} reviews</span>
            )}
          </div>
          <button
            onClick={() => addToWishlist(rental.id)}
            className="text-gray-400 hover:text-red-500 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );

  if (loading && activeTab === 'all') {
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
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Holiday Rentals</h1>
            <p className="text-gray-600">Find the perfect vacation rental for your next getaway</p>
          </div>

          {/* Tabs */}
          <div className="mb-8">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('featured')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'featured'
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Featured Properties
                </button>
                <button
                  onClick={() => setActiveTab('destinations')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'destinations'
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Popular Destinations
                </button>
                <button
                  onClick={() => setActiveTab('all')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'all'
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  All Rentals
                </button>
              </nav>
            </div>
          </div>

          {/* Popular Destinations */}
          {activeTab === 'destinations' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {popularDestinations.map((destination, index) => (
                <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer">
                  <div className="h-32 bg-gradient-to-r from-teal-400 to-blue-500 flex items-center justify-center">
                    <h3 className="text-white text-xl font-bold">{destination.name}</h3>
                  </div>
                  <div className="p-4">
                    <p className="text-gray-600">{destination.property_count} properties</p>
                    <p className="text-sm text-gray-500">From ${destination.avg_price}/night</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Search and Filters - Only show for 'all' tab */}
          {activeTab === 'all' && (
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <form onSubmit={handleSearch} className="space-y-4">
                {/* Search Bar */}
                <div className="flex gap-4">
                  <input
                    type="text"
                    placeholder="Search destinations, property names..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                  />
                  <button
                    type="submit"
                    className="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                  >
                    Search
                  </button>
                </div>

                {/* Filters */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <select
                    value={selectedType}
                    onChange={(e) => setSelectedType(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="">All Property Types</option>
                    {rentalTypes.map((type) => (
                      <option key={type.id} value={type.name}>
                        {type.name}
                      </option>
                    ))}
                  </select>

                  <input
                    type="text"
                    placeholder="Destination"
                    value={selectedDestination}
                    onChange={(e) => setSelectedDestination(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />

                  <select
                    value={guestCount}
                    onChange={(e) => setGuestCount(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="">Any Guests</option>
                    <option value="1">1 Guest</option>
                    <option value="2">2 Guests</option>
                    <option value="4">4 Guests</option>
                    <option value="6">6 Guests</option>
                    <option value="8">8+ Guests</option>
                  </select>

                  <select
                    value={bedrooms}
                    onChange={(e) => setBedrooms(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="">Any Bedrooms</option>
                    <option value="1">1 Bedroom</option>
                    <option value="2">2 Bedrooms</option>
                    <option value="3">3 Bedrooms</option>
                    <option value="4">4+ Bedrooms</option>
                  </select>
                </div>

                {/* Date and Price Range */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Check-in / Check-out</label>
                    <div className="flex gap-2">
                      <input
                        type="date"
                        value={checkIn}
                        onChange={(e) => setCheckIn(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                      <input
                        type="date"
                        value={checkOut}
                        onChange={(e) => setCheckOut(e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Price Range (per night)</label>
                    <div className="flex gap-2">
                      <input
                        type="number"
                        placeholder="Min Price"
                        value={priceRange.min}
                        onChange={(e) => setPriceRange({ ...priceRange, min: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                      <input
                        type="number"
                        placeholder="Max Price"
                        value={priceRange.max}
                        onChange={(e) => setPriceRange({ ...priceRange, max: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Sort By</label>
                    <select
                      value={`${sortBy}-${sortOrder}`}
                      onChange={(e) => {
                        const [field, order] = e.target.value.split('-');
                        setSortBy(field);
                        setSortOrder(order);
                      }}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    >
                      <option value="created_at-desc">Newest First</option>
                      <option value="price_per_night-asc">Price: Low to High</option>
                      <option value="price_per_night-desc">Price: High to Low</option>
                      <option value="average_rating-desc">Highest Rated</option>
                      <option value="review_count-desc">Most Reviewed</option>
                    </select>
                  </div>
                </div>
              </form>
            </div>
          )}

          {/* Results */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {activeTab === 'featured' && featuredRentals.map(renderRentalCard)}
            {activeTab === 'all' && rentals.map(renderRentalCard)}
          </div>

          {/* Empty State */}
          {((activeTab === 'all' && rentals.length === 0) ||
            (activeTab === 'featured' && featuredRentals.length === 0)) && !loading && (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No holiday rentals found</h3>
              <p className="text-gray-600">
                {activeTab === 'all' 
                  ? 'Try adjusting your search criteria or browse featured properties.'
                  : 'Check back later for new featured properties.'
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default HolidayRentalsPage;