"use client";
import { useState, useEffect } from 'react';
import { commercialVehicleService } from '@/services/commercialVehicleService';
import Layout from '@/components/layout/Layout';

const CommercialVehiclesPage = () => {
  const [vehicles, setVehicles] = useState([]);
  const [vehicleTypes, setVehicleTypes] = useState([]);
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [yearRange, setYearRange] = useState({ min: '', max: '' });
  const [mileageRange, setMileageRange] = useState({ min: '', max: '' });
  const [fuelType, setFuelType] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    searchVehicles();
  }, [selectedType, selectedBrand, fuelType, sortBy, sortOrder]);

  const loadInitialData = async () => {
    try {
      setLoading(true);
      const [vehiclesData, typesData, brandsData] = await Promise.all([
        commercialVehicleService.searchCommercialVehicles({ page: 1, per_page: 20 }),
        commercialVehicleService.getVehicleTypes(),
        commercialVehicleService.getBrands()
      ]);
      
      setVehicles(vehiclesData.items || []);
      setVehicleTypes(typesData.types || []);
      setBrands(brandsData.brands || []);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchVehicles = async () => {
    try {
      setLoading(true);
      const searchParams = {
        query: searchQuery,
        vehicle_type: selectedType,
        brand: selectedBrand,
        price_from: priceRange.min,
        price_to: priceRange.max,
        year_from: yearRange.min,
        year_to: yearRange.max,
        mileage_from: mileageRange.min,
        mileage_to: mileageRange.max,
        fuel_type: fuelType,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: 1,
        per_page: 20
      };

      const response = await commercialVehicleService.searchCommercialVehicles(searchParams);
      setVehicles(response.items || []);
    } catch (error) {
      console.error('Error searching vehicles:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    searchVehicles();
  };

  const addToFavorites = async (vehicleId) => {
    try {
      await commercialVehicleService.addToFavorites(vehicleId);
      // Update UI to show item is favorited
    } catch (error) {
      console.error('Error adding to favorites:', error);
    }
  };

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
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Commercial Vehicles</h1>
            <p className="text-gray-600">Find trucks, vans, construction equipment, and other commercial vehicles</p>
          </div>

          {/* Search and Filters */}
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <form onSubmit={handleSearch} className="space-y-4">
              {/* Search Bar */}
              <div className="flex gap-4">
                <input
                  type="text"
                  placeholder="Search commercial vehicles..."
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
                  <option value="">All Vehicle Types</option>
                  {vehicleTypes.map((type) => (
                    <option key={type.id} value={type.name}>
                      {type.name}
                    </option>
                  ))}
                </select>

                <select
                  value={selectedBrand}
                  onChange={(e) => setSelectedBrand(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                >
                  <option value="">All Brands</option>
                  {brands.map((brand) => (
                    <option key={brand.id} value={brand.name}>
                      {brand.name}
                    </option>
                  ))}
                </select>

                <select
                  value={fuelType}
                  onChange={(e) => setFuelType(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                >
                  <option value="">Any Fuel Type</option>
                  <option value="diesel">Diesel</option>
                  <option value="gasoline">Gasoline</option>
                  <option value="electric">Electric</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="cng">CNG</option>
                  <option value="lpg">LPG</option>
                </select>

                <select
                  value={`${sortBy}-${sortOrder}`}
                  onChange={(e) => {
                    const [field, order] = e.target.value.split('-');
                    setSortBy(field);
                    setSortOrder(order);
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                >
                  <option value="created_at-desc">Newest First</option>
                  <option value="created_at-asc">Oldest First</option>
                  <option value="price-asc">Price: Low to High</option>
                  <option value="price-desc">Price: High to Low</option>
                  <option value="year-desc">Year: Newest First</option>
                  <option value="year-asc">Year: Oldest First</option>
                  <option value="mileage-asc">Mileage: Low to High</option>
                </select>
              </div>

              {/* Advanced Filters */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
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

                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700">Mileage Range (km)</label>
                  <div className="flex gap-2">
                    <input
                      type="number"
                      placeholder="Min Mileage"
                      value={mileageRange.min}
                      onChange={(e) => setMileageRange({ ...mileageRange, min: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    />
                    <input
                      type="number"
                      placeholder="Max Mileage"
                      value={mileageRange.max}
                      onChange={(e) => setMileageRange({ ...mileageRange, max: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500"
                    />
                  </div>
                </div>
              </div>
            </form>
          </div>

          {/* Results */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {vehicles.map((vehicle) => (
              <div key={vehicle.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                {/* Image */}
                <div className="aspect-w-16 aspect-h-12 bg-gray-200">
                  {vehicle.images && vehicle.images.length > 0 ? (
                    <img
                      src={vehicle.images[0].image_url}
                      alt={vehicle.title}
                      className="w-full h-48 object-cover"
                    />
                  ) : (
                    <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
                      <span className="text-gray-400">No Image</span>
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="p-4">
                  <h3 className="font-semibold text-lg text-gray-900 mb-2 line-clamp-2">
                    {vehicle.title}
                  </h3>
                  
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-2xl font-bold text-teal-600">
                      ${vehicle.price?.toLocaleString()}
                    </span>
                    <span className="text-sm text-gray-500">
                      {vehicle.year}
                    </span>
                  </div>

                  <div className="text-sm text-gray-600 mb-2">
                    <p>{vehicle.brand} • {vehicle.vehicle_type}</p>
                    <p>{vehicle.mileage?.toLocaleString()} km • {vehicle.fuel_type}</p>
                    <p>{vehicle.location}</p>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">
                      {new Date(vehicle.created_at).toLocaleDateString()}
                    </span>
                    <button
                      onClick={() => addToFavorites(vehicle.id)}
                      className="text-gray-400 hover:text-red-500 transition-colors"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Empty State */}
          {vehicles.length === 0 && !loading && (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0a2 2 0 01-2-2v-5a2 2 0 00-2-2H8z" />
                </svg>
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No commercial vehicles found</h3>
              <p className="text-gray-600">Try adjusting your search criteria or browse all vehicle types.</p>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
};

export default CommercialVehiclesPage;