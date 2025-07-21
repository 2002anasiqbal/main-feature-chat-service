"use client";
import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Sidebar from "@/components/general/Sidebar";
import Page from "@/components/GenerateCard";
import SearchBar from "@/components/root/SearchBar";
import ButtonWithIcon from "@/components/root/ButtonWithIcon";
import { LiaMapMarkedAltSolid } from "react-icons/lia";
import { useRouter } from "next/navigation";
import motorcycleService from "@/services/motorcycleService";

export default function TwoColumnLayoutPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [motorcycles, setMotorcycles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentCategory, setCurrentCategory] = useState("All Motorcycles");
  const [searchValue, setSearchValue] = useState(""); // Track search input value

  // const navigateToMap = () => {
  //   router.push("/routes/motor-cycle/map");
  // };

  // NEW: Track the current category filter
  const [categoryFilter, setCategoryFilter] = useState(null);

  const navigateToMap = () => {
    router.push("/routes/motor-cycle/map");
  };

  // Load motorcycles based on filters
  const loadMotorcycles = async (filters = null) => {
    try {
      setLoading(true);
      
      // Get category from URL if present
      const categoryFromUrl = searchParams.get('category');
      console.log("🔄 Loading motorcycles with filters:", filters, "category from URL:", categoryFromUrl);
      
      let searchFilters = {};
      
      if (categoryFromUrl && !filters?.search_term) {
        // If we have a category from URL and no search term, use category
        searchFilters.category_name = categoryFromUrl;
         setCategoryFilter(categoryFromUrl);
        setCurrentCategory(categoryFromUrl);
      }
      
      if (filters) {
        // Merge any additional filters
        searchFilters = { ...searchFilters, ...filters };
        
          if (filters.search_term && categoryFromUrl) {
          searchFilters.category_name = categoryFromUrl; // Ensure category is maintained
          setCurrentCategory(`Search in ${categoryFromUrl}: ${filters.search_term}`);
        } else if (filters.search_term) {
          setCurrentCategory(`Search: ${filters.search_term}`);
        }
      }
      
      if (!categoryFromUrl && !filters) {
        setCurrentCategory("All Motorcycles");
      }
      
      console.log("🔍 Final search filters:", searchFilters);
      
      const response = await motorcycleService.searchMotorcycles(searchFilters, 1, 30);
      
      console.log("📊 Response received:", response);
      
      if (response && response.items) {
        setMotorcycles(response.items);
        console.log(`✅ Loaded ${response.items.length} motorcycles out of ${response.total} total`);
      } else {
        console.log("⚠️ No items in response");
        setMotorcycles([]);
      }
    } catch (error) {
      console.error("❌ Error loading motorcycles:", error);
      setMotorcycles([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle search input changes
  const handleSearchChange = (e) => {
    const searchTerm = e.target.value;
    setSearchValue(searchTerm); // Update the input value

    // Clear any existing timeout
    if (window.searchTimeout) {
      clearTimeout(window.searchTimeout);
    }
    
    // Debounce the search
    window.searchTimeout = setTimeout(() => {
      if (searchTerm.trim()) {
         const searchFilters = { search_term: searchTerm.trim() };
        
        // If we're in a specific category, maintain that category in the search
        if (categoryFilter) {
          searchFilters.category_name = categoryFilter;
          console.log(`🔍 Searching within category "${categoryFilter}" for: "${searchTerm}"`);
        } else {
          console.log(`🔍 Searching across all categories for: "${searchTerm}"`);
        }
        
        loadMotorcycles(searchFilters);
      } else {
        // FIXED: When search is cleared, restore to category or all
        console.log("🔄 Search cleared, restoring to category filter");
        const categoryFromUrl = searchParams.get('category');
        if (categoryFromUrl) {
          setCurrentCategory(categoryFromUrl);
          loadMotorcycles(); // This will load the category due to useEffect
        } else {
          setCurrentCategory("All Motorcycles");
          loadMotorcycles(); // This will load all motorcycles
        }
      }
    }, 300);  // 300ms debounce
  };

  // Handle filter changes from sidebar
  const handleFilterChange = (filters) => {
    console.log("🔍 Filters received from sidebar:", filters);
  // FIXED: Maintain category when applying sidebar filters
    if (categoryFilter) {
      filters.category_name = categoryFilter;
      console.log(`🔍 Applying sidebar filters within category "${categoryFilter}"`);
    }
    
    // Clear search input when using sidebar filters
    setSearchValue("");
    loadMotorcycles(filters);
  };

  // Load initial motorcycles
  useEffect(() => {
    loadMotorcycles();
  }, [searchParams]);

  return (
    <>
      <style jsx>{`
        .hide-scrollbar::-webkit-scrollbar {
          display: none;
        }
        .hide-scrollbar {
          -ms-overflow-style: none;
          scrollbar-width: none;
        }
      `}</style>

      <div className="min-h-screen flex flex-col">
        <div className="w-full bg-white py-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="w-full md:w-auto flex-1">
            <SearchBar 
              placeholder="Search motorcycles" 
              value={searchValue}
              onChange={handleSearchChange}
            />
          </div>
          <div className="w-full md:w-auto md:ml-4">
            <ButtonWithIcon
              icon={LiaMapMarkedAltSolid}
              label="Map"
              onClick={navigateToMap}
              className="bg-blue-600 text-white hover:bg-blue-700 px-4 py-2 rounded-md w-full md:w-auto"
            />
          </div>
        </div>

        <div className="flex flex-1 relative">
          <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
            <Sidebar onFilterChange={handleFilterChange} />
          </div>

          <div className="flex-1 bg-white p-6 max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
            <h1 className="font-bold text-3xl text-gray-800 mb-6">
              {currentCategory} ({motorcycles.length} found)
            </h1>
            
            {loading ? (
              <div className="flex justify-center items-center h-64">
                <div className="text-lg text-gray-600">Loading motorcycles...</div>
              </div>
            ) : (
              <Page 
                columns={3} 
                route="/routes/motor-cycle/category" 
                cards={motorcycles}
                disableAutoFetch={true}
              />
            )}
          </div>
        </div>
      </div>
    </>
  );
}