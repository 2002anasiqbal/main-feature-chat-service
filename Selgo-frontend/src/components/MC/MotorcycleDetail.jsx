"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { FaArrowLeft, FaPhone, FaEnvelope } from "react-icons/fa";
import { FiArrowRight, FiArrowLeft } from "react-icons/fi";
import useAuthStore from "@/store/store";
import { CiHeart } from "react-icons/ci";
import { FaHeart } from "react-icons/fa";
import motorcycleService from "@/services/motorcycleService";

const MotorcycleDetail = ({
  motorcycle,
  onLoanCalculate,
  loanResult,
  showLoanCalculator,
  setShowLoanCalculator,
  loanParams,
  setLoanParams
}) => {
  const router = useRouter();
  const [currentImage, setCurrentImage] = useState(0);
  const [showExpandedSpecs, setShowExpandedSpecs] = useState(false);
  const [isFavorite, setIsFavorite] = useState(false);
const [favoriteLoading, setFavoriteLoading] = useState(false);
  // Get user from store AND check localStorage directly as fallback
  const { user, fetchUser } = useAuthStore();
  const [localUser, setLocalUser] = useState(null);

  // Check for user in localStorage as fallback
  useEffect(() => {
    const checkUserState = async () => {
      console.log("🔍 Checking user state...");
      
      // First try to get user from store
      if (user) {
        console.log("✅ User from store:", user);
        setLocalUser(user);
        return;
      }

      // Fallback: check localStorage directly
      const storedUser = localStorage.getItem('user');
      if (storedUser) {
        try {
          const parsedUser = JSON.parse(storedUser);
          console.log("✅ User from localStorage:", parsedUser);
          setLocalUser(parsedUser);
          
          // Try to update store
          if (fetchUser) {
            await fetchUser();
          }
        } catch (error) {
          console.error("❌ Error parsing stored user:", error);
        }
      } else {
        console.log("❌ No user found in localStorage");
        setLocalUser(null);
      }
    };

    checkUserState();
  }, [user, fetchUser]);

  // Add this useEffect after your existing useEffects
useEffect(() => {
  const checkFavoriteStatus = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      if (token && motorcycle?.id) {
        const favorite = await motorcycleService.isMotorcycleFavorite(motorcycle.id);
        setIsFavorite(favorite);
      }
    } catch (error) {
      console.error('Error checking favorite status:', error);
    }
  };

  if (motorcycle) {
    checkFavoriteStatus();
  }
}, [motorcycle]);

  // Use localUser as the primary user source
  const currentUser = localUser || user;

  const getImageUrl = (imageUrl) => {
    if (!imageUrl) return "/assets/swiper/1.jpg";
    if (imageUrl.startsWith('http')) return imageUrl;
    if (imageUrl.startsWith('/uploads/')) return imageUrl;
    return imageUrl;
  };

  const images = motorcycle.images || [];
  const imageUrls = images.length > 0 
    ? images.map(img => img.image_url || img) 
    : ["/assets/swiper/1.jpg"];

  const nextImage = () => {
    setCurrentImage((prev) => (prev + 1) % imageUrls.length);
  };

  const prevImage = () => {
    setCurrentImage((prev) =>
      prev === 0 ? imageUrls.length - 1 : prev - 1
    );
  };

  const handleLoanParamChange = (e) => {
    const { name, value } = e.target;
    setLoanParams({
      ...loanParams,
      [name]: value ? Number(value) : 0
    });
  };

  // Check if current user is the seller
  const isOwner = user && motorcycle.seller_id === user.id;
  const canContact = motorcycle.seller_id !== user?.id; // Can contact if not the owner

  // Get seller display name
  const getSellerName = () => {
    if (motorcycle.seller?.name) {
      return motorcycle.seller.name;
    }
    return `Seller #${motorcycle.seller_id}`;
  };

  // Get seller join year
  const getSellerJoinYear = () => {
    if (motorcycle.seller?.created_at) {
      return new Date(motorcycle.seller.created_at).getFullYear();
    }
    return 2025; // Default year
  };

  // Simple contact handlers
  const handleContactSeller = () => {
    if (!user) {
      router.push(`/routes/auth/signin?redirect=${encodeURIComponent(window.location.pathname)}`);
      return;
    }
    
    // Simple alert for now - you can enhance this later
    alert(`Contact seller: ${motorcycle.seller?.email || 'Contact information not available'}`);
  };

  const handleCallSeller = () => {
    if (!user) {
      router.push(`/routes/auth/signin?redirect=${encodeURIComponent(window.location.pathname)}`);
      return;
    }
    
    // Simple alert for now
    alert(`Call seller: ${motorcycle.seller?.phone || 'Phone number not available'}`);
  };
  // Add this function after your existing functions
const handleFavoriteToggle = async () => {
  if (!currentUser) {
    router.push(`/routes/auth/signin?redirect=${encodeURIComponent(window.location.pathname)}`);
    return;
  }

  setFavoriteLoading(true);
  try {
    const response = await motorcycleService.toggleFavorite(motorcycle.id);
    setIsFavorite(response.is_favorite);
    
    console.log(response.is_favorite ? "Added to favorites!" : "Removed from favorites!");
  } catch (error) {
    console.error('Error toggling favorite:', error);
    alert("Error updating favorites. Please try again.");
  } finally {
    setFavoriteLoading(false);
  }
};

  // Debug logging
  useEffect(() => {
    console.log("🔍 User state:", user);
    console.log("🔍 Is Owner:", isOwner);
    console.log("🔍 Can Contact:", canContact);
    console.log("🔍 Motorcycle seller_id:", motorcycle?.seller_id);
  }, [user, motorcycle]);

  return (
    <div className="max-w-6xl mx-auto p-6 lg:p-12 bg-white">
      {/* Back Button */}
      <button
        className="flex items-center text-gray-700 hover:text-black font-medium mb-6"
        onClick={() => router.back()}
      >
        <FaArrowLeft className="mr-2" />
        Back
      </button>

      {/* Image Carousel - Full Width at Top */}
      <div className="w-full mb-8">
        <div className="relative">
          <Image
            src={getImageUrl(imageUrls[currentImage])}
            alt={motorcycle.title}
            width={1200}
            height={600}
            className="rounded-lg object-cover w-full h-80 sm:h-96 md:h-[500px] lg:h-[600px] xl:h-[700px] border"
            unoptimized={true}
          />
          
          {/* Image Counter */}
          <div className="absolute top-3 right-3 bg-black text-white px-3 py-1 text-sm rounded-lg shadow-md">
            <span className="font-semibold">{currentImage + 1}</span> / {imageUrls.length}
          </div>

          {/* Navigation Arrows */}
          {imageUrls.length > 1 && (
            <>
              <button
                onClick={prevImage}
                className="absolute left-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100"
              >
                <FiArrowLeft size={22} className="text-gray-600"/>
              </button>
              <button
                onClick={nextImage}
                className="absolute right-3 top-1/2 transform -translate-y-1/2 p-3 bg-white shadow-md rounded-full hover:bg-gray-100"
              >
                <FiArrowRight size={22} className="text-gray-600"/>
              </button>
            </>
          )}
        </div>

 
      </div>

      {/* Motorcycle Information - Below Image */}
      <div className="space-y-6">
        {/* Title and Price */}
        <div>
          <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            {motorcycle.title}
          </h1>
          
          <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-6">
            <div className="text-sm text-blue-700 mb-1">Total price</div>
            <div className="text-2xl font-bold text-black">
              {motorcycle.price?.toLocaleString()} kr
            </div>
          </div>
        </div>

        {/* Key Specifications */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Key Specifications</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <span className="text-gray-600">📅</span>
              <div>
                <div className="text-gray-500">Model year</div>
                <div className="font-semibold">{motorcycle.year || "N/A"}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">📏</span>
              <div>
                <div className="text-gray-500">Mileage</div>
                <div className="font-semibold">{motorcycle.mileage ? `${motorcycle.mileage.toLocaleString()} km` : "N/A"}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">⚙️</span>
              <div>
                <div className="text-gray-500">Displacement</div>
                <div className="font-semibold">{motorcycle.engine_size ? `${motorcycle.engine_size}cc` : "N/A"}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-gray-600">⚡</span>
              <div>
                <div className="text-gray-500">Effect</div>
                <div className="font-semibold">{motorcycle.engine_power ? `${motorcycle.engine_power} hp` : "10 hp"}</div>
              </div>
            </div>
          </div>
          
          <button
            onClick={() => setShowExpandedSpecs(!showExpandedSpecs)}
            className="mt-4 px-5 py-2 border border-gray-400 rounded-md font-medium text-gray-800 hover:bg-gray-100 transition"
          >
            {showExpandedSpecs ? "See Less" : "See More"}
          </button>
        </div>

        {/* Expanded Specifications */}
        {showExpandedSpecs && (
          <div className="border-t pt-6">
            <h2 className="text-2xl font-bold mb-4">Detailed Specifications</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Left Column */}
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Model</h4>
                  <p className="text-gray-600">{motorcycle.model || "N/A"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Brand</h4>
                  <p className="text-gray-600">{motorcycle.brand || "N/A"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Model year</h4>
                  <p className="text-gray-600">{motorcycle.year || "N/A"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Displacement</h4>
                  <p className="text-gray-600">{motorcycle.engine_size ? `${motorcycle.engine_size}cc` : "N/A"}</p>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Type</h4>
                  <p className="text-gray-600">{motorcycle.motorcycle_type || "N/A"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Mileage</h4>
                  <p className="text-gray-600">{motorcycle.mileage ? `${motorcycle.mileage.toLocaleString()} km` : "N/A"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">Condition</h4>
                  <p className="text-gray-600">{motorcycle.condition || "Used"}</p>
                </div>
                <div>
                  <h4 className="font-semibold text-gray-800 mb-2">City</h4>
                  <p className="text-gray-600">{motorcycle.city || "N/A"}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Description and Seller Info - Below Specs */}
      <div className="mt-10 border-t pt-6 flex flex-col lg:flex-row justify-between items-start gap-8">
        {/* Description Section */}
        <div className="w-full lg:w-3/4 space-y-4">
          <h3 className="text-2xl font-bold text-gray-900">Description</h3>
          <div className="prose max-w-none">
            <p className="text-gray-700 whitespace-pre-line">
              {motorcycle.description || "No description provided."}
            </p>
          </div>

          
        </div>

        {/* Seller Info Card */}
        <div className="w-full lg:w-1/4 shadow-md p-4 rounded-lg border">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Seller Information</h3>
          
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gray-300 rounded-full flex items-center justify-center">
              <span className="text-gray-600 font-bold">
                {motorcycle.seller?.name ? motorcycle.seller.name.charAt(0).toUpperCase() : "?"}
              </span>
            </div>
            <div>
              <div className="font-semibold">
                {isOwner ? "Your Listing" : getSellerName()}
              </div>
              <div className="text-sm text-gray-600">
                {motorcycle.seller_type === 'dealer' ? 'Professional Dealer' : 'Private Seller'}
              </div>
              <div className="text-sm text-gray-600">
                Seller ID: #{motorcycle.seller_id}
              </div>
              <div className="text-sm text-gray-600">
                On Selgo since {getSellerJoinYear()}
              </div>
            </div>
          </div>

          {/* Removed reviews section */}

          {/* Contact Buttons - Only show if not owner and user is logged in */}
          {!isOwner && currentUser && canContact && (
            <div className="space-y-2">
              <button
                onClick={handleContactSeller}
                className="w-full bg-teal-600 text-white py-2 rounded-md hover:bg-teal-700 transition flex items-center justify-center gap-2"
              >
                <FaEnvelope size={16} />
                Contact Seller
              </button>
              <button
                onClick={handleCallSeller}
                className="w-full border border-gray-400 rounded-md font-medium text-gray-800 hover:bg-gray-100 transition py-2 flex items-center justify-center gap-2"
              >
                <FaPhone size={16} />
                Call Seller
              </button>

              {/* ADD THIS - Heart/Favorite button */}
  
            </div>
          )}

          

          {/* Owner Actions */}
          {isOwner && (
            <div className="space-y-2">
              <div className="bg-green-50 border border-green-200 rounded-md p-3 text-center">
                <p className="text-green-700 font-medium">This is your listing</p>
              </div>
              <button
                onClick={() => router.push(`/routes/motor-cycle/edit/${motorcycle.id}`)}
                className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition"
              >
                Edit Listing
              </button>
            </div>
          )}

          {/* Authentication Required Message */}
          {!currentUser && canContact && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 text-center">
              <p className="text-yellow-700 text-sm mb-2">Sign in to contact seller</p>
              <button
                onClick={() => router.push(`/routes/auth/signin?redirect=${encodeURIComponent(window.location.pathname)}`)}
                className="text-blue-600 underline text-sm"
              >
                Sign In
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Loan Calculator Section */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow-md border">
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
              <form onSubmit={onLoanCalculate} className="space-y-4">
                <div>
                  <label className="block text-gray-600 mb-1">Motorcycle Price (kr)</label>
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
                    name="term_months"
                    value={loanParams.term_months}
                    onChange={handleLoanParamChange}
                    className="w-full p-2 border border-gray-300 rounded-md"
                    min="12"
                    max="84"
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
                      <span className="font-bold">{Number(loanResult.monthly_payment).toFixed(2)} kr</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Interest:</span>
                      <span>{Number(loanResult.total_interest).toFixed(2)} kr</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Total Amount Payable:</span>
                      <span>{Number(loanResult.total_amount).toFixed(2)} kr</span>
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
    </div>
  );
};

export default MotorcycleDetail;