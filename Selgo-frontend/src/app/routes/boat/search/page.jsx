// "use client";
// import { useState, useEffect } from "react";
// import { useSearchParams, useRouter } from "next/navigation";
// import Page from "@/components/GenerateCard";
// import SearchBar from "@/components/root/SearchBar";
// import Sidebar from "@/components/general/Sidebar";
// import boatService from "@/services/boatService";

// export default function BoatSearchPage() {
//   const searchParams = useSearchParams();
//   const router = useRouter();
//   const query = searchParams.get("q") || "";
//   const [boats, setBoats] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [searchTerm, setSearchTerm] = useState(query);
//   const [totalResults, setTotalResults] = useState(0);
//   const [currentFilters, setCurrentFilters] = useState({
//     search_term: query,
//     limit: 20,
//     offset: 0
//   });

//   useEffect(() => {
//     // Set the search term when the query parameter changes
//     setSearchTerm(query);
    
//     // Search for boats when the query changes
//     if (query) {
//       const initialFilters = {
//         search_term: query,
//         limit: 20,
//         offset: 0
//       };
//       setCurrentFilters(initialFilters);
//       searchBoats(initialFilters);
//     } else {
//       // If there's no query, reset the boats list
//       setBoats([]);
//       setTotalResults(0);
//       setLoading(false);
//     }
//   }, [query]);

//   const searchBoats = async (filters) => {
//     try {
//       setLoading(true);
//       const response = await boatService.filterBoats(filters);
//       setBoats(response.items || []);
//       setTotalResults(response.total || 0);
//     } catch (error) {
//       console.error("Error searching boats:", error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleSearch = (event) => {
//     setSearchTerm(event.target.value);
//   };

//   const handleSearchSubmit = (e) => {
//     e.preventDefault();
    
//     // Update URL with new search term
//     router.push(`/routes/boat/search?q=${encodeURIComponent(searchTerm)}`);
//   };

//   // This will be called when the sidebar filters change
//   const handleFilterChange = (newFilters) => {
//     // Merge the new sidebar filters with the search term
//     const updatedFilters = {
//       ...newFilters,
//       search_term: searchTerm,
//       limit: 20,
//       offset: 0
//     };
    
//     setCurrentFilters(updatedFilters);
//     searchBoats(updatedFilters);
//   };

//   return (
//     <div className="min-h-screen">
//       {/* Search Header */}
//       <div className="bg-white p-6 border-b">
//         <form onSubmit={handleSearchSubmit}>
//           <SearchBar 
//             placeholder="Search boats..." 
//             value={searchTerm}
//             onChange={handleSearch} 
//           />
//         </form>
        
//         <div className="mt-4">
//           <h1 className="text-2xl font-bold">
//             {query ? `Search results for "${query}"` : "Search Boats"}
//           </h1>
//           <p className="text-gray-600">
//             {loading ? "Searching..." : `${totalResults} results found`}
//           </p>
//         </div>
//       </div>

//       {/* Results with Sidebar */}
//       <div className="flex flex-1 relative">
//         {/* Sidebar - with filter functionality */}
//         <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
//           <Sidebar onFilterChange={handleFilterChange} />
//         </div>

//         {/* Results Area */}
//         <div className="flex-1 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
//           <div className="container mx-auto px-4 py-8">
//             {loading ? (
//               <div className="flex justify-center items-center py-10">
//                 <p>Loading results...</p>
//               </div>
//             ) : boats.length > 0 ? (
//               <Page columns={3} cards={boats} route="/routes/boat" />
//             ) : (
//               <div className="text-center py-10">
//                 <h2 className="text-xl font-semibold">No boats found</h2>
//                 <p className="mt-2 text-gray-600">
//                   Try adjusting your search terms or browse categories instead.
//                 </p>
//               </div>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

"use client";
import { useState, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import BoatGrid from "@/components/boat/BoatGrid"; // Import BoatGrid
import SearchBar from "@/components/root/SearchBar";
import Sidebar from "@/components/general/Sidebar";
import boatService from "@/services/boatService";

export default function BoatSearchPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const query = searchParams.get("q") || "";
  const [boats, setBoats] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState(query);
  const [totalResults, setTotalResults] = useState(0);
  const [currentFilters, setCurrentFilters] = useState({
    search_term: query,
    limit: 20,
    offset: 0
  });

  useEffect(() => {
    // Set the search term when the query parameter changes
    setSearchTerm(query);
    
    // Search for boats when the query changes
    if (query) {
      const initialFilters = {
        search_term: query,
        limit: 20,
        offset: 0
      };
      setCurrentFilters(initialFilters);
      searchBoats(initialFilters);
    } else {
      // If there's no query, reset the boats list
      setBoats([]);
      setTotalResults(0);
      setLoading(false);
    }
  }, [query]);

  const searchBoats = async (filters) => {
    try {
      setLoading(true);
      const response = await boatService.filterBoats(filters);
      setBoats(response.items || []);
      setTotalResults(response.total || 0);
    } catch (error) {
      console.error("Error searching boats:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    
    // Update URL with new search term
    router.push(`/routes/boat/search?q=${encodeURIComponent(searchTerm)}`);
  };

  // This will be called when the sidebar filters change
  const handleFilterChange = (newFilters) => {
    // Merge the new sidebar filters with the search term
    const updatedFilters = {
      ...newFilters,
      search_term: searchTerm,
      limit: 20,
      offset: 0
    };
    
    setCurrentFilters(updatedFilters);
    searchBoats(updatedFilters);
  };

  return (
    <div className="min-h-screen">
      {/* Search Header */}
      <div className="bg-white p-6 border-b">
        <form onSubmit={handleSearchSubmit}>
          <SearchBar 
            placeholder="Search boats..." 
            value={searchTerm}
            onChange={handleSearch} 
          />
        </form>
        
        <div className="mt-4">
          <h1 className="text-2xl font-bold">
            {query ? `Search results for "${query}"` : "Search Boats"}
          </h1>
          <p className="text-gray-600">
            {loading ? "Searching..." : `${totalResults} results found`}
          </p>
        </div>
      </div>

      {/* Results with Sidebar */}
      <div className="flex flex-1 relative">
        {/* Sidebar - with filter functionality */}
        <div className="md:w-1/4 z-10 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
          <Sidebar onFilterChange={handleFilterChange} />
        </div>

        {/* Results Area */}
        <div className="flex-1 bg-white max-h-[calc(100vh-4rem)] overflow-y-auto hide-scrollbar">
          <div className="container mx-auto px-4 py-8">
            {loading ? (
              <div className="flex justify-center items-center py-10">
                <p>Loading results...</p>
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
                  Try adjusting your search terms or browse categories instead.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}