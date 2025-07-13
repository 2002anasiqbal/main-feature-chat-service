// Selgo-frontend/src/components/MC/MCMain.jsx
// UPDATED: Connect "Find Bikes" section to real motorcycle backend data

"use client";
import { useState, useEffect } from "react";
import Image from "next/image";
import ButtonCard from "../general/ButtonCard";
import GenericCardCollection from "../GenericCardCollection";
import SearchBar from "../root/SearchBar";
import Page from "../GenerateCard";
import { useRouter } from "next/navigation";
import motorcycleService from "@/services/motorcycleService";

// ORIGINAL card data - NO CHANGES to UI
const cardData = [
  {
    items: [
      { tag: "Thresher 6000", icon: "1.svg", route: "/routes/motor-cycle/category?category=Thresher 6000" },
      { tag: "Suzuki 6000", icon: "2.svg", route: "/routes/motor-cycle/category?category=Suzuki 6000" },
      { tag: "Motorcycles 6000", icon: "3.svg", route: "/routes/motor-cycle/category?category=Motorcycles 6000" },
    ],
  },
  {
    items: [
      { tag: "Auto bikes 6000", icon: "4.svg", route: "/routes/motor-cycle/category?category=Auto bikes 6000" },
      { tag: "Tractor 6000", icon: "5.svg", route: "/routes/motor-cycle/category?category=Tractor 6000" },
      { tag: "Bikes 6000", icon: "6.svg", route: "/routes/motor-cycle/category?category=Bikes 6000" },
    ],
  },
];

// ORIGINAL rowStyles - NO CHANGES
const rowStyles = {
  0: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-3",
    gap: "gap-6",
    marginBottom: "mb-6",
  },
  1: {
    gridCols: "grid-cols-1 sm:grid-cols-3 lg:grid-cols-3",
    gap: "gap-6",
    centered: true,
  },
};

export default function MCMain() {
  const router = useRouter();
  
  // NEW: State for motorcycle data and search
  const [motorcycles, setMotorcycles] = useState([]);
  const [filteredMotorcycles, setFilteredMotorcycles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  
  // NEW: Fetch all motorcycles on component mount
  useEffect(() => {
    const fetchMotorcycles = async () => {
      try {
        setLoading(true);
        console.log("🔄 Fetching motorcycles for main page...");
        
        // Fetch motorcycles from backend
        const response = await motorcycleService.searchMotorcycles({}, 1, 50); // Get first 50
        console.log("📊 Motorcycles response:", response);
        
        if (response && response.items) {
          setMotorcycles(response.items);
          setFilteredMotorcycles(response.items);
          console.log(`✅ Loaded ${response.items.length} motorcycles`);
        } else {
          console.log("⚠️ No motorcycles found");
          setMotorcycles([]);
          setFilteredMotorcycles([]);
        }
      } catch (error) {
        console.error("❌ Error fetching motorcycles:", error);
        setMotorcycles([]);
        setFilteredMotorcycles([]);
      } finally {
        setLoading(false);
      }
    };

    fetchMotorcycles();
  }, []);

  // NEW: Handle search functionality
  const handleSearchChange = (e) => {
    const searchValue = e.target.value;
    setSearchTerm(searchValue);
    
    console.log("🔍 Search term changed:", searchValue);
    
    if (searchValue.trim() === "") {
      // If search is empty, show all motorcycles
      setFilteredMotorcycles(motorcycles);
      console.log("🔄 Search cleared, showing all motorcycles");
    } else {
      // Filter motorcycles based on search term
      const filtered = motorcycles.filter(motorcycle => 
        motorcycle.title?.toLowerCase().includes(searchValue.toLowerCase()) ||
        motorcycle.brand?.toLowerCase().includes(searchValue.toLowerCase()) ||
        motorcycle.model?.toLowerCase().includes(searchValue.toLowerCase()) ||
        motorcycle.description?.toLowerCase().includes(searchValue.toLowerCase())
      );
      
      setFilteredMotorcycles(filtered);
      console.log(`🔍 Found ${filtered.length} motorcycles matching "${searchValue}"`);
    }
  };

  // NEW: Format motorcycles for GenerateCard component
  const formatMotorcyclesForDisplay = (motorcyclesList) => {
    return motorcyclesList.map(motorcycle => ({
      id: motorcycle.id,
      title: motorcycle.title || "Unnamed Motorcycle",
      description: motorcycle.brand && motorcycle.model 
        ? `${motorcycle.brand} ${motorcycle.model} - ${motorcycle.year}`.trim() 
        : motorcycle.city || "No details available",
      price: motorcycle.price ? `${motorcycle.price.toLocaleString()} kr` : "Price unavailable",
      image: motorcycle.primary_image || "/assets/swiper/1.jpg",
      originalData: motorcycle
    }));
  };

  return (
    <div className="pt-24 sm:pt-16 bg-white min-h-screen">
      {/* ORIGINAL Hero Image - NO CHANGES */}
      <div className="relative w-full h-[500px] mb-6">
        <Image
          src="/assets/MC/motorcycle.svg"
          alt="Motorcycle Hero"
          fill
          className="object-cover object-center"
          priority
        />
      </div>

      {/* ORIGINAL Title - NO CHANGES */}
      <h1 className="text-5xl text-gray-900 font-bold pb-10">
        Motorcycles
      </h1>

      {/* UPDATED Search Bar - Now functional */}
      <div className="justify-center items-center gap-4 w-full mb-6">
        <SearchBar 
          placeholder="Search motorcycles..." 
          value={searchTerm}
          onChange={handleSearchChange}
        />
      </div>

      {/* ORIGINAL Cards Section - NO CHANGES */}
      <GenericCardCollection
        rows={cardData}
        rowStyles={rowStyles}
        imageBasePath="/assets/MC/"
        size="h-32 w-32"
      />

      {/* NEW: Find Bikes Section with Real Data */}
      <div className="mt-12">
        <h2 className="text-3xl font-bold text-gray-800 mb-6">
          Find Bikes {searchTerm && `(${filteredMotorcycles.length} results for "${searchTerm}")`}
        </h2>
        
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
            <span className="ml-4 text-gray-600">Loading motorcycles...</span>
          </div>
        ) : filteredMotorcycles.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">
              {searchTerm ? `No motorcycles found for "${searchTerm}"` : "No motorcycles available"}
            </div>
            {searchTerm && (
              <button
                onClick={() => {
                  setSearchTerm("");
                  setFilteredMotorcycles(motorcycles);
                }}
                className="mt-4 px-4 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700 transition"
              >
                Clear Search
              </button>
            )}
          </div>
        ) : (
          <Page 
            columns={3}
            route="/routes/motor-cycle"
            cards={formatMotorcyclesForDisplay(filteredMotorcycles)}
            disableAutoFetch={true}
          />
        )}
      </div>

      {/* ORIGINAL Centered Button - NO CHANGES */}
      <div className="flex justify-center items-center mt-8">
        <ButtonCard />
      </div>
    </div>
  );
}