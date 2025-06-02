"use client";
import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import boatService from "@/services/boatService";
import ProductDetail from "@/components/general/ProductDetail"; 
import LocationMap from "@/components/general/LocationMap";


// Geocoding function to convert location name to coordinates
async function geocodeLocationName(locationName) {
  try {
    // Using Nominatim (OpenStreetMap) for geocoding - it's free and doesn't require API key
    const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationName)}`);
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
    // Return default coordinates (e.g., center of the world map)
    return {
      latitude: 0,
      longitude: 0
    };
  }
}

export default function BoatDetailPage() {
  const params = useParams();
  const router = useRouter();
  const boatId = params.id;
  const [boat, setBoat] = useState(null);
  const [loading, setLoading] = useState(true);
  
  const [mapCoordinates, setMapCoordinates] = useState(null);

  
  // Loan calculator state
  const [loanParams, setLoanParams] = useState({
    price: 0,
    duration: 60,
    interest_rate: 5.5
  });
  const [loanResult, setLoanResult] = useState(null);
  const [showLoanCalculator, setShowLoanCalculator] = useState(false);
  
  // Fix done request state
  const [fixDoneRequest, setFixDoneRequest] = useState({
    boat_id: 0,
    price: 0,
    message: ''
  });
  const [showFixDoneForm, setShowFixDoneForm] = useState(false);

  useEffect(() => {
    const fetchBoatDetails = async () => {
      try {
        setLoading(true);
        const data = await boatService.getBoatDetails(boatId);
        setBoat(data);
        
        setLoanParams(prev => ({
          ...prev,
          price: data.price
        }));
        
        setFixDoneRequest({
          boat_id: data.id,
          price: data.price,
          message: ''
        });
        
        setLoading(false);
      } catch (error) {
        console.error(`Error fetching boat details:`, error);
        setLoading(false);
      }
    };

    if (boatId) {
      fetchBoatDetails();
    }
  }, [boatId]);

    // Add this useEffect for geocoding
  useEffect(() => {
    const getCoordinates = async () => {
      if (boat) {
        if (boat.location) {
          // Use existing coordinates if available
          setMapCoordinates({
            latitude: boat.location.latitude,
            longitude: boat.location.longitude
          });
        } else if (boat.location_name) {
          // Geocode the location name
          try {
            console.log("Geocoding location:", boat.location_name);
            const coords = await geocodeLocationName(boat.location_name);
            console.log("Geocoded coordinates:", coords);
            setMapCoordinates(coords);
          } catch (error) {
            console.error("Failed to geocode location:", error);
          }
        }
      }
    };

    getCoordinates();
  }, [boat]);


  const handleLoanParamChange = (e) => {
    const { name, value } = e.target;
    setLoanParams({
      ...loanParams,
      [name]: value ? Number(value) : 0
    });
  };

  const calculateLoan = async (e) => {
    e.preventDefault();
    try {
      const result = await boatService.getLoanEstimate(loanParams);
      setLoanResult(result);
    } catch (error) {
      console.error("Error calculating loan:", error);
      alert("Error calculating loan. Please try again.");
    }
  };

  const handleFixDoneChange = (e) => {
    const { name, value } = e.target;
    setFixDoneRequest({
      ...fixDoneRequest,
      [name]: name === 'price' ? Number(value) : value
    });
  };

const submitFixDoneRequest = async (e) => {
  e.preventDefault();
  
  try {
    // Use the new auth system to check authentication
    const token = localStorage.getItem('accessToken');
    const userStr = localStorage.getItem('user');
    
    if (!token || !userStr) {
      alert("Please log in to submit a Fix Done request.");
      router.push('/routes/auth/signin');
      return;
    }

    // Parse the user object
    const user = JSON.parse(userStr);
    console.log("Current user:", user);
    console.log("Boat user_id:", boat.user_id);
    
    // Check if user is trying to create a fix request for their own boat
    if (user.id === boat.user_id) {
      alert("You cannot create a Fix Done request for your own boat.");
      return;
    }

    // Submit the fix done request
    await boatService.createFixRequest(fixDoneRequest);
    alert("Fix Done request submitted successfully!");
    setShowFixDoneForm(false);

  } catch (error) {
    console.error("Error submitting Fix Done request:", error);
    
    // Check if it's an authentication error
    if (error.response?.status === 401) {
      alert("Your session has expired. Please log in again.");
      // Clear invalid tokens
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      router.push('/routes/auth/signin');
    } else {
      alert("Error submitting request. Please try again.");
    }
  }
};

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Loading boat details...</p>
      </div>
    );
  }

  if (!boat) {
    return (
      <div className="container mx-auto px-4 py-10 text-center">
        <h1 className="text-2xl font-bold text-red-600">Boat not found</h1>
        <p className="mt-4">The boat you are looking for does not exist or has been removed.</p>
        <button
          onClick={() => router.push("/routes/boat")}
          className="mt-6 bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
        >
          Back to Boats
        </button>
      </div>
    );
  }

  const images = boat.images || [];
  const imageUrls = images.length > 0 
    ? images.map(img => img.image_url || img) 
    : ["/assets/boat/placeholder.jpg"];

  const keyInfo = `${boat.year || "N/A"} · ${boat.make || ""} ${boat.model || ""} · Length: ${boat.length ? `${boat.length} ft` : "Not specified"}`;
  
  const expandedKeyInfo = (
    <div className="space-y-2">
      <p><strong>Year:</strong> {boat.year || "N/A"}</p>
      <p><strong>Make:</strong> {boat.make || "N/A"}</p>
      <p><strong>Model:</strong> {boat.model || "N/A"}</p>
      <p><strong>Length:</strong> {boat.length ? `${boat.length} ft` : "N/A"}</p>
      <p><strong>Beam:</strong> {boat.beam ? `${boat.beam} ft` : "N/A"}</p>
      <p><strong>Draft:</strong> {boat.draft ? `${boat.draft} ft` : "N/A"}</p>
      <p><strong>Fuel Type:</strong> {boat.fuel_type || "N/A"}</p>
      <p><strong>Hull Material:</strong> {boat.hull_material || "N/A"}</p>
      <p><strong>Engine Make:</strong> {boat.engine_make || "N/A"}</p>
      <p><strong>Engine Model:</strong> {boat.engine_model || "N/A"}</p>
      <p><strong>Engine Hours:</strong> {boat.engine_hours || "N/A"}</p>
      <p><strong>Engine Power:</strong> {boat.engine_power ? `${boat.engine_power} HP` : "N/A"}</p>
      <p><strong>Condition:</strong> {boat.condition?.replace(/_/g, ' ').charAt(0).toUpperCase() + boat.condition?.slice(1).replace(/_/g, ' ') || "N/A"}</p>
    </div>
  );
  
  const description = boat.description || "No description provided.";
  
  const sellerInfo = {
    name: boat.user_id ? `Seller ID: ${boat.user_id}` : "Seller",
    website: "#",
    moreAds: "#",
    followCompany: "#"
  };

 const handleMessageClick = () => {
  // Check authentication before allowing message
  const token = localStorage.getItem('accessToken');
  const user = localStorage.getItem('user');
  
  if (!token || !user) {
    alert("Please log in to send a message.");
    router.push('/routes/auth/signin');
    return;
  }
  
  router.push(`/routes/message?boat_id=${boat.id}`);
};

  const handleFixDoneClick = () => {
    setShowFixDoneForm(!showFixDoneForm);
  };

  return (
    <div className="container mx-auto">
      <ProductDetail
        title={boat.title}
        price={boat.price.toLocaleString()}
        currency="$"
        productImages={imageUrls}
        description={description}
        keyInfo={keyInfo}
        expandedKeyInfo={expandedKeyInfo} // Pass expanded info
        sellerInfo={sellerInfo}
        onMessageClick={handleMessageClick}
        onFixDoneClick={handleFixDoneClick}
      />
      
      {/* Fix Done Request Form - ABOVE the Loan Calculator and Map */}
      {showFixDoneForm && (
        <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold mb-4">Make Fix Done Request</h2>
          <form onSubmit={submitFixDoneRequest} className="space-y-4">
            <div>
              <label className="block text-gray-600 mb-1">Offer Price</label>
              <input
                type="number"
                name="price"
                value={fixDoneRequest.price}
                onChange={handleFixDoneChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                required
              />
            </div>
            <div>
              <label className="block text-gray-600 mb-1">Message</label>
              <textarea
                name="message"
                value={fixDoneRequest.message}
                onChange={handleFixDoneChange}
                className="w-full p-2 border border-gray-300 rounded-md"
                rows={3}
                placeholder="Add any additional information or questions..."
              />
            </div>
            <div className="flex gap-4">
              <button
                type="submit"
                className="px-6 py-2 bg-teal-600 text-white rounded-md hover:bg-teal-700"
              >
                Submit Request
              </button>
              <button
                type="button"
                onClick={() => setShowFixDoneForm(false)}
                className="px-6 py-2 border border-gray-400 text-gray-700 rounded-md hover:bg-gray-100"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}
      
      {/* Loan Calculator Section */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold">Loan Calculator</h2>
          <button 
            onClick={() => setShowLoanCalculator(!showLoanCalculator)}
            className="text-teal-600 hover:underline"
          >
            {showLoanCalculator ? "Hide Calculator" : "Show Calculator"}
          </button>
        </div>
        
        {showLoanCalculator && (
          <div className="flex flex-col md:flex-row gap-8">
            <div className="md:w-1/2">
              <form onSubmit={calculateLoan} className="space-y-4">
                <div>
                  <label className="block text-gray-600 mb-1">Boat Price ($)</label>
                  <input
                    type="number"
                    name="price"
                    value={loanParams.price}
                    onChange={handleLoanParamChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    required
                  />
                </div>
                <div>
                  <label className="block text-gray-600 mb-1">Loan Term (months)</label>
                  <input
                    type="number"
                    name="duration"
                    value={loanParams.duration}
                    onChange={handleLoanParamChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    min="12"
                    max="240"
                    required
                  />
                </div>
                <div>
                  <label className="block text-gray-600 mb-1">Interest Rate (%)</label>
                  <input
                    type="number"
                    name="interest_rate"
                    value={loanParams.interest_rate}
                    onChange={handleLoanParamChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    step="0.1"
                    min="0"
                    required
                  />
                </div>
                <button
                  type="submit"
                  className="w-full bg-teal-600 text-white py-2 rounded-md hover:bg-teal-700"
                >
                  Calculate
                </button>
              </form>
            </div>
            
            <div className="md:w-1/2">
              {loanResult ? (
                <div className="bg-white p-4 rounded-md border border-gray-200">
                  <h3 className="font-semibold text-xl mb-2">Loan Summary</h3>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span>Monthly Payment:</span>
                      <span className="font-bold">${loanResult.monthly_payment.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Interest:</span>
                      <span>${loanResult.total_interest.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Amount Payable:</span>
                      <span>${loanResult.total_payable.toFixed(2)}</span>
                    </div>
                    
                    <h4 className="font-semibold mt-4 mb-2">Monthly Breakdown</h4>
                    <div className="max-h-48 overflow-y-auto">
                      {Object.entries(loanResult.breakdown).map(([month, details]) => (
                        <div key={month} className="border-b border-gray-100 py-1">
                          <div className="flex justify-between text-sm">
                            <span>{month}:</span>
                            <span>${details.payment}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full">
                  <p className="text-gray-500">Enter your loan details and click calculate to see your monthly payments.</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      
      {/* Location Map - Now at the BOTTOM */}
    {/* Location Map - Now at the BOTTOM with geocoding */}
     {boat && boat.location_name && mapCoordinates && (
        <LocationMap 
          heading="Location"
          latitude={mapCoordinates.latitude}
          longitude={mapCoordinates.longitude}
          locationName={boat.location_name || "Boat Location"}
        />
      )}
    </div>
  );
}