"use client";
import { useState, useEffect } from "react";
import { useParams } from "next/navigation";
import BoatGrid from "@/components/boat/BoatGrid";
import SearchBar from "@/components/root/SearchBar";
import Sidebar from "@/components/general/Sidebar"; 
import boatService from "@/services/boatService";

export default function BoatCategoryPage() {
  const params = useParams();
  const categoryId = params.id;
  const [boats, setBoats] = useState([]);
  const [category, setCategory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [totalResults, setTotalResults] = useState(0);
  
  // Filter state with defaults
  const [filters, setFilters] = useState({
    category_id: parseInt(categoryId, 10),
    limit: 20,
    offset: 0
  });

  useEffect(() => {
    // Update category_id when URL param changes
    setFilters(prev => ({...prev, category_id: parseInt(categoryId, 10)}));
    
    // Ensure we're fetching with the correct category ID
    console.log(`Fetching boats for category ID: ${categoryId}`);
    fetchBoatsByCategory();
    
    // Get category details
    fetchCategoryDetails();
  }, [categoryId]);

  // This will be triggered by the Sidebar component
  const handleFilterChange = (newFilters) => {
    console.log("⭐ Category page received filters:", JSON.stringify(newFilters, null, 2));
    
    const updatedFilters = {
      ...newFilters,
      category_id: parseInt(categoryId, 10),
      limit: 20,
      offset: 0
    };
    
    console.log("⭐ Merged filters to be sent to API:", JSON.stringify(updatedFilters, null, 2));
    
    setFilters(updatedFilters);
    
    // Always use filter endpoint
    fetchBoatsByFilters(updatedFilters);
  };

  const fetchBoatsByCategory = async () => {
    try {
      setLoading(true);
      
      // Create a clean filter object with just the category ID
      const categoryFilter = {
        category_id: parseInt(categoryId, 10),
        limit: 20,
        offset: 0
      };
      
      console.log(`🔍 Category Page: Fetching boats for category ${categoryId} with filter:`, categoryFilter);
      
      const response = await boatService.filterBoats(categoryFilter);
      console.log(`🔍 Category Page: Received response with ${response.items?.length || 0} boats`);
      
      if (response.items && response.items.length > 0) {
        console.log("First boat in results:", response.items[0]);
      }
      
      setBoats(response.items || []);
      setTotalResults(response.total || 0);
    } catch (error) {
      console.error("Error fetching boats by category:", error);
      setBoats([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchBoatsByFilters = async (filterParams) => {
    try {
      setLoading(true);
      console.log("🔍 Fetching boats with filter params:", JSON.stringify(filterParams, null, 2));
      
      // Use the filterBoats method directly
      const response = await boatService.filterBoats(filterParams);
      console.log("🔍 Filter API response:", response);
      
      setBoats(response.items || []);
      setTotalResults(response.total || 0);
    } catch (error) {
      console.error("❌ Error fetching boats with filters:", error);
      setBoats([]);
    } finally {
      setLoading(false);
    }
  };

  const fetchCategoryDetails = async () => {
    try {
      console.log(`Fetching category details for ID ${categoryId}`);
      const categories = await boatService.getCategories();
      const foundCategory = categories.find(cat => cat.id === parseInt(categoryId, 10));
      setCategory(foundCategory);
    } catch (error) {
      console.error("Error fetching category details:", error);
    }
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    // Add search term to current filters and search
    const searchFilters = {
      ...filters,
      search_term: searchTerm
    };
    
    fetchBoatsByFilters(searchFilters);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Hide scrollbars on all screens */}
      <style jsx>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none; /* IE and Edge */
          scrollbar-width: none;    /* Firefox */
        }
      `}</style>

      {/* Header Section */}
      <div className="w-full bg-white py-4 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="w-full md:w-auto flex-1">
          <form onSubmit={handleSearchSubmit}>
            <SearchBar 
              placeholder="Search within this category..." 
              value={searchTerm}
              onChange={handleSearch} 
            />
          </form>
        </div>
      </div>

      {/* Category Header */}
      <div className="bg-white p-4 border-b">
        <h1 className="text-3xl font-bold">
          {category ? category.label : "Loading..."}
        </h1>
        <p className="text-gray-600">
          {loading ? "Loading boats..." : `${totalResults} boats found`}
        </p>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 relative">
        {/* Sidebar - Pass the filter change handler */}
        <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
          <Sidebar onFilterChange={handleFilterChange} />
        </div>

        {/* Main Page Content */}
        <div className="flex-1 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar p-4">
          {loading ? (
            <div className="flex justify-center items-center py-10">
              <p>Loading boats...</p>
            </div>
          ) : boats.length > 0 ? (
            <BoatGrid 
              boats={boats}
              columns={3} 
              route="/routes/boat" 
            />
          ) : (
            <div className="text-center py-10">
              <h2 className="text-xl font-semibold">No boats found</h2>
              <p className="mt-2 text-gray-600">
                Try adjusting your search terms or filters.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}