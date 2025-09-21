"use client";
import { useState, useEffect } from 'react';
import { carAuctionService } from '@/services/carAuctionService';
import Layout from '@/components/layout/Layout';

const CarAuctionsPage = () => {
  const [auctions, setAuctions] = useState([]);
  const [featuredAuctions, setFeaturedAuctions] = useState([]);
  const [endingSoonAuctions, setEndingSoonAuctions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedMake, setSelectedMake] = useState('');
  const [selectedModel, setSelectedModel] = useState('');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [yearRange, setYearRange] = useState({ min: '', max: '' });
  const [auctionStatus, setAuctionStatus] = useState(['active']);
  const [sortBy, setSortBy] = useState('end_time');
  const [sortOrder, setSortOrder] = useState('asc');
  const [activeTab, setActiveTab] = useState('all');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    if (activeTab === 'all') {
      searchAuctions();
    }
  }, [selectedMake, selectedModel, auctionStatus, sortBy, sortOrder, activeTab]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [auctionsData, featuredData, endingSoonData] = await Promise.all([
        carAuctionService.searchAuctions({ page: 1, per_page: 20, status_filter: ['active'] }),
        carAuctionService.getFeaturedAuctions(8),
        carAuctionService.getEndingSoonAuctions(6)
      ]);
      
      setAuctions(auctionsData.items || []);
      setFeaturedAuctions(featuredData.items || []);
      setEndingSoonAuctions(endingSoonData.items || []);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchAuctions = async () => {
    try {
      setLoading(true);
      const searchParams = {
        query: searchQuery,
        make: selectedMake,
        model: selectedModel,
        price_from: priceRange.min,
        price_to: priceRange.max,
        year_from: yearRange.min,
        year_to: yearRange.max,
        status_filter: auctionStatus,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: 1,
        per_page: 20
      };

      const response = await carAuctionService.searchAuctions(searchParams);
      setAuctions(response.items || []);
    } catch (error) {
      console.error('Error searching auctions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setActiveTab('all');
    searchAuctions();
  };

  const watchAuction = async (auctionId) => {
    try {
      await carAuctionService.watchAuction({ auction_id: auctionId });
      // Update UI to show auction is watched
    } catch (error) {
      console.error('Error watching auction:', error);
    }
  };

  const formatTimeRemaining = (endTime) => {
    const now = new Date();
    const end = new Date(endTime);
    const diff = end - now;
    
    if (diff <= 0) return 'Ended';
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (days > 0) return `${days}d ${hours}h`;
    if (hours > 0) return `${hours}h ${minutes}m`;
    return `${minutes}m`;
  };

  const renderAuctionCard = (auction) => (
    <div key={auction.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      <div className="relative aspect-w-16 aspect-h-12 bg-gray-200">
        {auction.images && auction.images.length > 0 ? (
          <img
            src={auction.images[0].image_url}
            alt={auction.title}
            className="w-full h-48 object-cover"
          />
        ) : (
          <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
            <span className="text-gray-400">No Image</span>
          </div>
        )}
        
        {/* Status Badge */}
        <div className="absolute top-2 left-2">
          <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
            auction.status === 'active' ? 'bg-green-100 text-green-800' :
            auction.status === 'ended' ? 'bg-gray-100 text-gray-800' :
            'bg-yellow-100 text-yellow-800'
          }`}>
            {auction.status.toUpperCase()}
          </span>
        </div>

        {/* Time Remaining */}
        <div className="absolute top-2 right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-xs">
          {formatTimeRemaining(auction.end_time)}
        </div>
      </div>

      {/* Content */}
      <div className="p-4">
        <h3 className="font-semibold text-lg text-gray-900 mb-2 line-clamp-2">
          {auction.title}
        </h3>
        
        <div className="flex items-center justify-between mb-2">
          <div>
            <span className="text-sm text-gray-500">Current Bid</span>
            <div className="text-2xl font-bold text-teal-600">
              ${auction.current_bid?.toLocaleString() || auction.starting_bid?.toLocaleString()}
            </div>
          </div>
          <div className="text-right">
            <span className="text-sm text-gray-500">Bids</span>
            <div className="text-lg font-semibold text-gray-900">
              {auction.bid_count || 0}
            </div>
          </div>
        </div>

        <div className="text-sm text-gray-600 mb-3">
          <p>{auction.make} {auction.model} • {auction.year}</p>
          <p>{auction.mileage?.toLocaleString()} km • {auction.location}</p>
          {auction.reserve_price && !auction.reserve_met && (
            <p className="text-orange-600">Reserve not met</p>
          )}
          {!auction.reserve_price && (
            <p className="text-green-600">No Reserve</p>
          )}
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">
            Ends: {new Date(auction.end_time).toLocaleDateString()}
          </span>
          <button
            onClick={() => watchAuction(auction.id)}
            className="text-gray-400 hover:text-blue-500 transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
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
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Car Auctions</h1>
            <p className="text-gray-600">Bid on cars and find great deals at online auctions</p>
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
                  Featured Auctions
                </button>
                <button
                  onClick={() => setActiveTab('ending-soon')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'ending-soon'
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Ending Soon
                </button>
                <button
                  onClick={() => setActiveTab('all')}
                  className={`py-2 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'all'
                      ? 'border-teal-500 text-teal-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  All Auctions
                </button>
              </nav>
            </div>
          </div>

          {/* Search and Filters - Only show for 'all' tab */}
          {activeTab === 'all' && (
            <div className="bg-white rounded-lg shadow-md p-6 mb-8">
              <form onSubmit={handleSearch} className="space-y-4">
                {/* Search Bar */}
                <div className="flex gap-4">
                  <input
                    type="text"
                    placeholder="Search auctions..."
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
                  <input
                    type="text"
                    placeholder="Make (e.g., BMW, Mercedes)"
                    value={selectedMake}
                    onChange={(e) => setSelectedMake(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />

                  <input
                    type="text"
                    placeholder="Model"
                    value={selectedModel}
                    onChange={(e) => setSelectedModel(e.target.value)}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />

                  <select
                    value={`${sortBy}-${sortOrder}`}
                    onChange={(e) => {
                      const [field, order] = e.target.value.split('-');
                      setSortBy(field);
                      setSortOrder(order);
                    }}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="end_time-asc">Ending Soon</option>
                    <option value="end_time-desc">Ending Later</option>
                    <option value="current_bid-desc">Highest Bid</option>
                    <option value="current_bid-asc">Lowest Bid</option>
                    <option value="created_at-desc">Newest First</option>
                  </select>

                  <select
                    multiple
                    value={auctionStatus}
                    onChange={(e) => {
                      const values = Array.from(e.target.selectedOptions, option => option.value);
                      setAuctionStatus(values);
                    }}
                    className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  >
                    <option value="active">Active</option>
                    <option value="ended">Ended</option>
                    <option value="cancelled">Cancelled</option>
                  </select>
                </div>

                {/* Price and Year Range */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-700">Price Range</label>
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
                    <label className="text-sm font-medium text-gray-700">Year Range</label>
                    <div className="flex gap-2">
                      <input
                        type="number"
                        placeholder="Min Year"
                        value={yearRange.min}
                        onChange={(e) => setYearRange({ ...yearRange, min: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                      <input
                        type="number"
                        placeholder="Max Year"
                        value={yearRange.max}
                        onChange={(e) => setYearRange({ ...yearRange, max: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                      />
                    </div>
                  </div>
                </div>
              </form>
            </div>
          )}

          {/* Results */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {activeTab === 'featured' && featuredAuctions.map(renderAuctionCard)}
            {activeTab === 'ending-soon' && endingSoonAuctions.map(renderAuctionCard)}
            {activeTab === 'all' && auctions.map(renderAuctionCard)}
          </div>

          {/* Empty State */}
          {((activeTab === 'all' && auctions.length === 0) ||
            (activeTab === 'featured' && featuredAuctions.length === 0) ||
            (activeTab === 'ending-soon' && endingSoonAuctions.length === 0)) && !loading && (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No auctions found</h3>
              <p className="text-gray-600">
                {activeTab === 'all' 
                  ? 'Try adjusting your search criteria or browse featured auctions.'
                  : 'Check back later for new auctions.'
                }
              </p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default CarAuctionsPage;