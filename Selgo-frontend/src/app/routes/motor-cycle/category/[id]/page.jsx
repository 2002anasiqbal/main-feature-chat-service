"use client";
import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import motorcycleService from "@/services/motorcycleService";
import MotorcycleDetail from "@/components/MC/MotorcycleDetail";
import LocationMap from "@/components/general/LocationMap";
import useAuthStore from "@/store/store";

import Page from "@/components/GenerateCard"; // Use your existing component
// Enhanced geocoding function
async function geocodeLocationName(locationName) {
  try {
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationName)}&limit=1`);
    const data = await response.json();
    
    if (data && data.length > 0) {
      return {
        latitude: parseFloat(data[0].lat),
        longitude: parseFloat(data[0].lon)
      };
    }
    throw new Error("Location not found");
  } catch (error) {
    console.error("Geocoding error:", error);
    // Default to Oslo, Norway
    return {
      latitude: 59.9139,
      longitude: 10.7522
    };
  }
}

export default function MotorcycleDetailPage() {
  const params = useParams();
  const router = useRouter();
  const { user, fetchUser } = useAuthStore();
  const motorcycleId = params.id;
  
  const [motorcycle, setMotorcycle] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mapCoordinates, setMapCoordinates] = useState(null);
  const [similarMotorcycles, setSimilarMotorcycles] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  // Loan calculator state
  const [loanParams, setLoanParams] = useState({
    price: 0,
    term_months: 36,
    interest_rate: 7.5
  });
  const [loanResult, setLoanResult] = useState(null);
  const [showLoanCalculator, setShowLoanCalculator] = useState(false);

  // Fetch user on component mount
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);

  useEffect(() => {
    const fetchMotorcycleDetails = async () => {
      try {
        setLoading(true);
        const data = await motorcycleService.getMotorcycleDetail(motorcycleId);
        setMotorcycle(data);
        
        setLoanParams(prev => ({
          ...prev,
          price: data.price
        }));
        
        setLoading(false);
      } catch (error) {
        console.error(`Error fetching motorcycle details:`, error);
        setLoading(false);
      }
    };

    if (motorcycleId) {
      fetchMotorcycleDetails();
    }
  }, [motorcycleId]);

  useEffect(() => {
  const fetchSimilarMotorcycles = async () => {
    if (!motorcycle) return;
    
    setLoadingSimilar(true);
    try {
      console.log("🔍 Fetching similar motorcycles for:", motorcycle.title);
      
      const searchFilters = {
        brand: motorcycle.brand,
        
      };
      
      const response = await motorcycleService.searchMotorcycles(searchFilters, 1, 6);
      
      // Filter out the current motorcycle
      const similar = (response.items || [])
        .filter(item => item.id !== motorcycle.id)
        .slice(0, 6); // Take 6 similar motorcycles
      
      console.log("✅ Found similar motorcycles:", similar);
      setSimilarMotorcycles(similar);
    } catch (error) {
      console.error("❌ Error fetching similar motorcycles:", error);
      setSimilarMotorcycles([]);
    } finally {
      setLoadingSimilar(false);
    }
  };

  fetchSimilarMotorcycles();
}, [motorcycle]);

  // Geocode location for map
  useEffect(() => {
    const getCoordinates = async () => {
      if (motorcycle) {
        try {
          // Use address first, then city as fallback
          const locationToGeocode = motorcycle.address || motorcycle.city;
          if (locationToGeocode) {
            const coords = await geocodeLocationName(locationToGeocode);
            setMapCoordinates(coords);
          }
        } catch (error) {
          console.error("Failed to geocode location:", error);
        }
      }
    };

    getCoordinates();
  }, [motorcycle]);

  const calculateLoan = async (e) => {
    e.preventDefault();
    try {
      const result = await motorcycleService.calculateLoan(loanParams);
      setLoanResult(result);
    } catch (error) {
      console.error("Error calculating loan:", error);
      alert("Error calculating loan. Please try again.");
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-teal-500"></div>
      </div>
    );
  }

  if (!motorcycle) {
    return (
      <div className="container mx-auto px-4 py-10 text-center">
        <h1 className="text-2xl font-bold text-red-600">Motorcycle not found</h1>
        <p className="mt-4">The motorcycle you are looking for does not exist or has been removed.</p>
        <button
          onClick={() => router.push("/routes/motor-cycle")}
          className="mt-6 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
        >
          Back to Motorcycles
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto">
      <MotorcycleDetail
        motorcycle={motorcycle}
        onLoanCalculate={calculateLoan}
        loanResult={loanResult}
        showLoanCalculator={showLoanCalculator}
        setShowLoanCalculator={setShowLoanCalculator}
        loanParams={loanParams}
        setLoanParams={setLoanParams}
      />
      
      {/* Location Map */}
      {motorcycle && mapCoordinates && (
        <LocationMap 
          heading="Location"
          latitude={mapCoordinates.latitude}
          longitude={mapCoordinates.longitude}
          locationName={motorcycle.address || motorcycle.city || "Motorcycle Location"}
        />
      )}

      {/* More like this section */}
     {/* More like this section */}
<div className="mt-8">
  <h2 className="text-2xl font-bold mb-6 px-4">More like this</h2>
  
  {loadingSimilar ? (
    <div className="flex justify-center items-center h-32">
      <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-teal-500"></div>
      <span className="ml-4 text-gray-600">Loading similar motorcycles...</span>
    </div>
  ) : similarMotorcycles.length > 0 ? (
    <Page 
      columns={3}
      route="/routes/motor-cycle/category"
      cards={similarMotorcycles}
      disableAutoFetch={true}
    />
  ) : (
    <div className="bg-gray-100 rounded-lg p-8 text-center mx-4">
      <p className="text-gray-600">No similar motorcycles found in our database.</p>
    </div>
  )}
</div>
    </div>
  );
}