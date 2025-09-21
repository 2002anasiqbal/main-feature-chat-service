"use client";
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

const AdvancedSearch = ({ 
  searchType = 'all', 
  onSearch, 
  initialFilters = {},
  showLocationFilter = true,
  showPriceFilter = true,
  showCategoryFilter = true 
}) => {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [filters, setFilters] = useState({
    query: '',
    location: '',
    category: '',
    priceMin: '',
    priceMax: '',
    sortBy: 'relevance',
    ...initialFilters
  });

  const categories = {
    all: ['All Categories', 'Cars', 'Property', 'Jobs', 'Travel', 'Electronics', 'Boats', 'Motorcycles'],
    cars: ['All Cars', 'Sedan', 'SUV', 'Hatchback', 'Coupe', 'Convertible', 'Wagon', 'Pickup'],
    property: ['All Property', 'Houses', 'Apartments', 'Commercial', 'Land', 'Holiday Rentals'],
    jobs: ['All Jobs', 'Full-time', 'Part-time', 'Contract', 'Freelance', 'Internship'],
    travel: ['All Travel', 'Flights', 'Hotels', 'Car Rentals', 'Packages', 'Activities'],
    electronics: ['All Electronics', 'Phones', 'Computers', 'TVs', 'Audio', 'Gaming', 'Cameras'],
    boats: ['All Boats', 'Sailboats', 'Motor Boats', 'Yachts', 'Fishing Boats', 'Jet Skis'],
    motorcycles: ['All Motorcycles', 'Sport', 'Cruiser', 'Touring', 'Off-road', 'Scooter']
  };

  const locations = [
    'All Locations', 'Oslo', 'Bergen', 'Trondheim', 'Stavanger', 'Kristiansand', 
    'Fredrikstad', 'Sandnes', 'Tromsø', 'Sarpsborg', 'Skien'
  ];

  const sortOptions = [
    { value: 'relevance', label: 'Most Relevant' },
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'price_asc', label: 'Price: Low to High' },
    { value: 'price_desc', label: 'Price: High to Low' },
    { value: 'distance', label: 'Distance' }
  ];

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    
    // Clean up empty filters
    const cleanFilters = Object.entries(filters).reduce((acc, [key, value]) => {
      if (value && value !== '' && value !== 'All Categories' && value !== 'All Locations') {
        acc[key] = value;
      }
      return acc;
    }, {});

    if (onSearch) {
      onSearch(cleanFilters);
    } else {
      // Default behavior: navigate to search results
      const searchParams = new URLSearchParams(cleanFilters);
      router.push(`/routes/search?${searchParams.toString()}`);
    }
  };

  const clearFilters = () => {
    setFilters({
      query: '',
      location: '',
      category: '',
      priceMin: '',
      priceMax: '',
      sortBy: 'relevance'
    });
  };

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Basic Search Bar */}
      <form onSubmit={handleSearch} className="p-4">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="What are you looking for?"
              value={filters.query}
              onChange={(e) => handleFilterChange('query', e.target.value)}
              className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent text-lg"
            />
            <button
              type="button"
              onClick={() => setIsOpen(!isOpen)}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-teal-600"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
              </svg>
            </button>
          </div>
          <button
            type="submit"
            className="px-8 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors font-medium"
          >
            Search
          </button>
        </div>
      </form>

      {/* Advanced Filters */}
      {isOpen && (
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            {/* Location Filter */}
            {showLocationFilter && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Location</label>
                <select
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                >
                  {locations.map((location) => (
                    <option key={location} value={location}>
                      {location}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Category Filter */}
            {showCategoryFilter && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Category</label>
                <select
                  value={filters.category}
                  onChange={(e) => handleFilterChange('category', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                >
                  {(categories[searchType] || categories.all).map((category) => (
                    <option key={category} value={category}>
                      {category}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Price Range */}
            {showPriceFilter && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Price Range</label>
                <div className="flex gap-2">
                  <input
                    type="number"
                    placeholder="Min"
                    value={filters.priceMin}
                    onChange={(e) => handleFilterChange('priceMin', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />
                  <input
                    type="number"
                    placeholder="Max"
                    value={filters.priceMax}
                    onChange={(e) => handleFilterChange('priceMax', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                  />
                </div>
              </div>
            )}

            {/* Sort By */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
              <select
                value={filters.sortBy}
                onChange={(e) => handleFilterChange('sortBy', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
              >
                {sortOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between items-center">
            <button
              type="button"
              onClick={clearFilters}
              className="text-sm text-gray-600 hover:text-gray-800"
            >
              Clear all filters
            </button>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={handleSearch}
                className="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
              >
                Apply Filters
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedSearch;