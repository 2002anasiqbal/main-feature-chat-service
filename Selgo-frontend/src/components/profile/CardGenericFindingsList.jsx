"use client";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import boatService from "@/services/boatService";
import motorcycleService from "@/services/motorcycleService";

export default function CardGenericFindingsList({ findings = [], type = "boat" }) {
  // Keep all your existing state variables
  const router = useRouter();
  const [openMenuIndex, setOpenMenuIndex] = useState(null);
  const [favoriteBoats, setFavoriteBoats] = useState([]); // Keep the same name for consistency
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [debugInfo, setDebugInfo] = useState('');
  
  // Fetch favorite boats when component mounts
  useEffect(() => {
   const fetchFavorites = async () => {
   try {
    setLoading(true);
    setError(null);
    setDebugInfo('Starting fetch...');
    
    const token = localStorage.getItem('accessToken');
    if (!token) {
       console.log('No auth token found');
  setDebugInfo('No auth token found - user not logged in');
  setFavoriteBoats([]);
  setLoading(false);
  return;
    }
    
    setDebugInfo('Token found, fetching favorites...');
    
    let allFavorites = [];
    
    if (type === "combined") {
      // Fetch both boat AND motorcycle favorites
      console.log('🔍 Fetching combined favorites...');
      
      const [boatFavorites, motorcycleFavorites] = await Promise.all([
        boatService.getUserFavorites().catch(err => {
          console.error('Error fetching boat favorites:', err);
          return [];
        }),
        motorcycleService.getUserFavorites().catch(err => {
          console.error('Error fetching motorcycle favorites:', err);
          return [];
        })
      ]);
      
      // Process boat favorites and add type identifier
      const processedBoatFavorites = (Array.isArray(boatFavorites) ? boatFavorites : []).map(fav => ({
        ...fav,
        itemType: 'boat' // Add identifier
      }));
      
      // Process motorcycle favorites and add type identifier  
      const processedMotorcycleFavorites = (Array.isArray(motorcycleFavorites) ? motorcycleFavorites : []).map(fav => ({
        ...fav,
        itemType: 'motorcycle' // Add identifier
      }));
      
      // Combine both arrays
      allFavorites = [...processedBoatFavorites, ...processedMotorcycleFavorites];
      
      // Sort by creation date (newest first)
      allFavorites.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
      
      setDebugInfo(`Combined: ${processedBoatFavorites.length} boats + ${processedMotorcycleFavorites.length} motorcycles = ${allFavorites.length} total`);
      
    } else if (type === "motorcycle") {
      const favorites = await motorcycleService.getUserFavorites();
      allFavorites = Array.isArray(favorites) ? favorites.map(fav => ({...fav, itemType: 'motorcycle'})) : [];
      setDebugInfo(`Got ${allFavorites.length} motorcycle favorites`);
      
    } else {
      // Default to boats
      const favorites = await boatService.getUserFavorites();
      allFavorites = Array.isArray(favorites) ? favorites.map(fav => ({...fav, itemType: 'boat'})) : [];
      setDebugInfo(`Got ${allFavorites.length} boat favorites`);
    }
    
    console.log('✅ Processed favorites array:', allFavorites);
    setFavoriteBoats(allFavorites);
    setDebugInfo(`Successfully processed ${allFavorites.length} favorites`);
    
  } catch (error) {
    console.error('❌ Error fetching favorites:', error);
    setError(`Failed to load favorites: ${error.message}`);
    setDebugInfo(`Error: ${error.message}`);
    setFavoriteBoats([]);
  } finally {
    setLoading(false);
  }
};

    fetchFavorites();
  }, [type]); // Add type to dependencies

 // Update getImageUrl to handle motorcycle and boat default image
const getImageUrl = (imageUrl) => {
  if (!imageUrl) {
    return type === "motorcycle" || type === "combined" ? "/assets/swiper/1.jpg" : "/assets/boat/placeholder.jpg";
  }
  if (imageUrl.startsWith('http')) return imageUrl;
  if (imageUrl.startsWith('/uploads/')) return imageUrl;
  return `/uploads/${imageUrl}`;
};

// 4. UPDATE the handleItemClick function:
const handleItemClick = (itemId) => {
  if (type === "motorcycle" || type === "combined") {
    // For combined type, we need to determine if it's a boat or motorcycle
    // Look at the current favorite item to determine type
    const currentFavorite = favoriteBoats.find(fav => 
      fav.boat_id === itemId || fav.motorcycle_id === itemId
    );
    
    if (currentFavorite && currentFavorite.motorcycle_id) {
      router.push(`/routes/motor-cycle/category/${itemId}`);
    } else {
      router.push(`/routes/boat/${itemId}`);
    }
  } else {
    // Default to boat
    router.push(`/routes/boat/${itemId}`);
  }
};


// 5. UPDATE the removeFavorite function:
const removeFavorite = async (itemId) => {
  try {
    // Find the favorite item to determine its type
    const currentFavorite = favoriteBoats.find(fav => 
      fav.boat_id === itemId || fav.motorcycle_id === itemId
    );
    
    if (currentFavorite && currentFavorite.motorcycle_id) {
      // It's a motorcycle
      await motorcycleService.toggleFavorite(itemId);
      setFavoriteBoats(prev => prev.filter(fav => fav.motorcycle_id !== itemId));
    } else {
      // It's a boat
      await boatService.toggleFavorite(itemId);
      setFavoriteBoats(prev => prev.filter(fav => fav.boat_id !== itemId));
    }
    setOpenMenuIndex(null);
  } catch (error) {
    console.error('Error removing favorite:', error);
  }
};


// 5. UPDATE the copyItemLink function:
const copyItemLink = (itemId) => {
  // Find the favorite item to determine its type
  const currentFavorite = favoriteBoats.find(fav => 
    fav.boat_id === itemId || fav.motorcycle_id === itemId
  );
  
  const link = (currentFavorite && currentFavorite.motorcycle_id)
    ? `${window.location.origin}/routes/motor-cycle/category/${itemId}`
    : `${window.location.origin}/routes/boat/${itemId}`;
    
  navigator.clipboard.writeText(link);
  setOpenMenuIndex(null);
};

  // If no findings are provided, create a default one
  const defaultFindings = findings.length > 0 ? findings : [
    {
      title: "Favorite Items",
      ads: favoriteBoats.length
    }
  ];

  return (
    <div className="space-y-4 w-full">
      {/* Debug information */}
      <div className="bg-gray-100 p-2 text-xs text-gray-600 rounded">
        Debug: {debugInfo}
      </div>
      
      {defaultFindings.map((finding, index) => (
        <div key={index} className="bg-white border rounded-lg shadow-sm p-4">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold text-gray-800">{finding.title}</h3>
            <button className="text-gray-400 hover:text-gray-600">
              <span className="text-2xl">⋮</span>
            </button>
          </div>

          {/* Special handling for Favorite Items */}
          {finding.title === "Favorite Items" ? (
            <div className="space-y-3">
              {loading ? (
                <p className="text-gray-500">Loading favorites...</p>
              ) : error ? (
                <p className="text-red-500">{error}</p>
              ) : favoriteBoats.length > 0 ? (
                <div className="max-h-96 overflow-y-auto space-y-3">
                  {favoriteBoats.map((favorite, idx) => {
                    console.log(`Processing favorite ${idx}:`, favorite);

                    
                    const itemType = favorite.boat_id ? 'boat' : 'motorcycle';
                                   // Determine the type and get the correct item data
  const item = favorite.boat || favorite.motorcycle || favorite;
  const favoriteId = favorite.id || `fav-${favorite.boat_id || favorite.motorcycle_id || idx}`;
  const itemId = favorite.boat_id || favorite.motorcycle_id || item.id;
  
                    
                    // ADD THIS DEBUGGING:
  console.log(`🖼️ Image debugging for ${itemType} ${itemId}:`);
  console.log('  item object:', item);
  console.log('  item.primary_image:', item.primary_image);
  console.log('  item.images:', item.images);
  console.log('  favorite object:', favorite);


// Try different image sources
  let imageUrl = null;
   
 

  if (!item || !itemId) {
    console.warn('Invalid favorite item:', favorite);
    return (
      <div key={`invalid-${idx}`} className="p-2 bg-yellow-100 text-yellow-800 text-sm rounded">
        Invalid favorite data: {JSON.stringify(favorite).substring(0, 100)}...
      </div>
    );
    }



if (item.primary_image) {
    imageUrl = item.primary_image;
    console.log('  ✅ Using primary_image:', imageUrl);
  } else if (item.images && item.images.length > 0) {
    // Look for primary image in images array
    const primaryImg = item.images.find(img => img.is_primary);
    if (primaryImg) {
      imageUrl = primaryImg.image_url;
      console.log('  ✅ Using primary from images array:', imageUrl);
    } else {
      imageUrl = item.images[0].image_url || item.images[0];
      console.log('  ✅ Using first image from array:', imageUrl);
    }
  } else {
    console.log('  ❌ No image found, using placeholder');
    imageUrl = itemType === 'motorcycle' ? '/assets/swiper/1.jpg' : '/assets/boat/placeholder.jpg';
  }
  
  if (!item || !itemId) {
    console.warn('Invalid favorite item:', favorite);
    return (
      <div key={`invalid-${idx}`} className="p-2 bg-yellow-100 text-yellow-800 text-sm rounded">
        Invalid favorite data: {JSON.stringify(favorite).substring(0, 100)}...
      </div>
    );
  }


              // CREATE A UNIQUE KEY 
  const uniqueKey = `${itemType}-${itemId}-${favoriteId}`;

                    return (
                      <div 
                        key={uniqueKey}
                        className="relative flex items-start p-4 border border-gray-200 rounded-lg shadow-sm w-full cursor-pointer hover:bg-gray-50"
                        onClick={() => handleItemClick(itemId)}
                      >
                        {/* Image */}
        <div className="w-24 h-24 bg-gray-200 rounded-md mr-4 flex-shrink-0 overflow-hidden">
        <Image
          src={getImageUrl(imageUrl)}
          alt={item.title || (itemType === "motorcycle" ? "Motorcycle" : "Boat")}
          width={96}
          height={96}
          className="w-full h-full object-cover"
          unoptimized={true}
          onError={(e) => {
            console.log('❌ Image failed to load:', imageUrl);
            e.target.src = itemType === 'motorcycle' ? '/assets/swiper/1.jpg' : '/assets/boat/placeholder.jpg';
          }}
        />
        </div>
                        
        
      {/* Main Content Area */}
      <div className="flex-1 flex">
        {/* Item Details */}
        <div className="flex-grow">
          <h3 className="font-medium text-gray-800">
            {item.title || (itemType === "motorcycle" ? "Unknown Motorcycle" : "Unknown Boat")}
          </h3>
          <p className="text-base text-gray-800">
            {item.price ? `${Number(item.price).toLocaleString()} ${itemType === "motorcycle" ? "kr" : "$"}` : "Price not available"}
          </p>
          <p className="text-sm text-gray-600">
            {/* Handle different field names for boats vs motorcycles */}
            {itemType === "motorcycle" 
              ? (item.brand && item.model ? `${item.brand} ${item.model}` : "Details not available")
              : (item.make && item.model ? `${item.make} ${item.model}` : "Details not available")
            }
            {item.year && ` • ${item.year}`}
          </p>
          {/* Show city for motorcycles, location_name for boats */}
          {(item.city || item.location_name) && (
            <p className="text-xs text-gray-500 mt-1">
              {item.city || item.location_name}
            </p>
          )}
          <p className="text-xs text-gray-500 mt-1">
            Added {favorite.created_at ? new Date(favorite.created_at).toLocaleDateString() : "Recently"}
          </p>
          {/* Show type indicator */}
          <span className={`inline-block px-2 py-1 text-xs rounded mt-1 ${itemType === 'motorcycle' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
            {itemType === 'motorcycle' ? 'Motorcycle' : 'Boat'}
          </span>
          {/* Debug info */}
          <p className="text-xs text-blue-500 mt-1">
            ID: {itemId} | Fav: {favoriteId} | Type: {itemType}
          </p>
        </div>
                          
                          {/* Menu Section */}
                          <div className="relative">
                            {/* Menu Toggle Button */}
                            <button 
            className="text-gray-500 p-2 rounded-full hover:bg-gray-100"
            onClick={(e) => {
              e.stopPropagation();
              setOpenMenuIndex(openMenuIndex === favoriteId ? null : favoriteId);
            }}
          >
            {openMenuIndex === favoriteId ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="1"></circle>
                <circle cx="12" cy="5" r="1"></circle>
                <circle cx="12" cy="19" r="1"></circle>
              </svg>
            )}
          </button>
                            
          {/* Dropdown Menu */}
          {openMenuIndex === favoriteId && (
            <div className="absolute right-0 top-10 z-10 bg-white border border-gray-200 rounded-md shadow-md w-48">
              <button 
                className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700 border-b border-gray-200"
                onClick={(e) => {
                  e.stopPropagation();
                  copyItemLink(itemId);
                }}
              >
                Copy the link to ad
              </button>
              <button 
                className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700 border-b border-gray-200"
                onClick={(e) => {
                  e.stopPropagation();
                  setOpenMenuIndex(null);
                }}
              >
                Add note
              </button>
              <button 
                className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-red-600"
                onClick={(e) => {
                  e.stopPropagation();
                  removeFavorite(itemId);
                }}
              >
                Remove favourite
              </button>
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
               <div className="text-center py-8 text-gray-500">
                <p>No favorite items yet</p>
                <p className="text-sm">Start adding boats and motorcycles to your favorites!</p>
                <p className="text-xs text-gray-400 mt-2">
                  Array length: {favoriteBoats.length} | Type: {typeof favoriteBoats}
                </p>
              </div>
              )}
            </div>
          ) : (
            /* Default display for other findings - unchanged */
            <div className="relative flex items-start p-4 border border-gray-200 rounded-lg shadow-sm w-full">
              <div className="w-24 h-24 bg-gray-200 rounded-md mr-4 flex-shrink-0"></div>
              <div className="flex-1 flex">
                <div className="flex-grow">
                  <h3 className="font-medium text-gray-800">{finding.title}</h3>
                  <p className="text-base text-gray-800">{finding.price}</p>
                  <p className="text-sm text-gray-600">{finding.status}</p>
                  {finding.ads && (
                    <p className="text-sm text-gray-600">{finding.ads} ads</p>
                  )}
                </div>
                <div className="relative">
                  <button 
                    className="text-gray-500 p-2 rounded-full hover:bg-gray-100"
                    onClick={() => setOpenMenuIndex(openMenuIndex === index ? null : index)}
                  >
                    {openMenuIndex === index ? "×" : "⋮"}
                  </button>
                  {openMenuIndex === index && (
                    <div className="absolute right-0 top-10 z-10 bg-white border border-gray-200 rounded-md shadow-md w-48">
                      <button className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700">
                        Copy the link to ad
                      </button>
                      <button className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-gray-700">
                        Add note
                      </button>
                      <button className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm text-red-600">
                        Remove favourite
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}