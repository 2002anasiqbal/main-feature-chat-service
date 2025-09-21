"use client";
import { useState, useEffect, useRef } from 'react';

const MapView = ({ 
  items = [], 
  center = { lat: 59.9139, lng: 10.7522 }, // Oslo coordinates
  zoom = 10,
  height = '400px',
  onMarkerClick,
  showSearch = true,
  className = ''
}) => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [isLoaded, setIsLoaded] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);

  // Initialize Google Maps
  useEffect(() => {
    const initMap = () => {
      if (window.google && mapRef.current) {
        const mapInstance = new window.google.maps.Map(mapRef.current, {
          center: center,
          zoom: zoom,
          styles: [
            {
              featureType: 'poi',
              elementType: 'labels',
              stylers: [{ visibility: 'off' }]
            }
          ]
        });
        setMap(mapInstance);
        setIsLoaded(true);
      }
    };

    // Load Google Maps API if not already loaded
    if (!window.google) {
      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places`;
      script.async = true;
      script.defer = true;
      script.onload = initMap;
      document.head.appendChild(script);
    } else {
      initMap();
    }
  }, [center, zoom]);

  // Update markers when items change
  useEffect(() => {
    if (map && isLoaded) {
      // Clear existing markers
      markers.forEach(marker => marker.setMap(null));
      
      const newMarkers = items.map(item => {
        if (!item.latitude || !item.longitude) return null;

        const marker = new window.google.maps.Marker({
          position: { lat: parseFloat(item.latitude), lng: parseFloat(item.longitude) },
          map: map,
          title: item.title,
          icon: {
            url: getMarkerIcon(item.type),
            scaledSize: new window.google.maps.Size(30, 30)
          }
        });

        // Create info window
        const infoWindow = new window.google.maps.InfoWindow({
          content: createInfoWindowContent(item)
        });

        marker.addListener('click', () => {
          // Close other info windows
          markers.forEach(m => {
            if (m.infoWindow) {
              m.infoWindow.close();
            }
          });
          
          infoWindow.open(map, marker);
          setSelectedItem(item);
          
          if (onMarkerClick) {
            onMarkerClick(item);
          }
        });

        marker.infoWindow = infoWindow;
        return marker;
      }).filter(Boolean);

      setMarkers(newMarkers);

      // Adjust map bounds to fit all markers
      if (newMarkers.length > 0) {
        const bounds = new window.google.maps.LatLngBounds();
        newMarkers.forEach(marker => {
          bounds.extend(marker.getPosition());
        });
        map.fitBounds(bounds);
      }
    }
  }, [map, items, isLoaded]);

  const getMarkerIcon = (type) => {
    const icons = {
      car: '/assets/map/car-marker.png',
      property: '/assets/map/house-marker.png',
      job: '/assets/map/job-marker.png',
      travel: '/assets/map/travel-marker.png',
      electronics: '/assets/map/electronics-marker.png',
      boat: '/assets/map/boat-marker.png',
      motorcycle: '/assets/map/motorcycle-marker.png',
      default: '/assets/map/default-marker.png'
    };
    return icons[type] || icons.default;
  };

  const createInfoWindowContent = (item) => {
    const price = item.price ? `$${item.price.toLocaleString()}` : 'Price on request';
    const image = item.images && item.images.length > 0 ? item.images[0].image_url : '/assets/placeholder.jpg';
    
    return `
      <div style="max-width: 250px; padding: 10px;">
        <img src="${image}" alt="${item.title}" style="width: 100%; height: 120px; object-fit: cover; border-radius: 8px; margin-bottom: 8px;" />
        <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: 600; color: #1f2937;">${item.title}</h3>
        <p style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700; color: #059669;">${price}</p>
        <p style="margin: 0 0 8px 0; font-size: 14px; color: #6b7280;">${item.location || ''}</p>
        <button onclick="window.open('/routes/${item.type}/${item.id}', '_blank')" 
                style="background: #059669; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px;">
          View Details
        </button>
      </div>
    `;
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (!map || !searchQuery.trim()) return;

    const geocoder = new window.google.maps.Geocoder();
    geocoder.geocode({ address: searchQuery }, (results, status) => {
      if (status === 'OK' && results[0]) {
        const location = results[0].geometry.location;
        map.setCenter(location);
        map.setZoom(12);
        
        // Add a temporary marker for the searched location
        const searchMarker = new window.google.maps.Marker({
          position: location,
          map: map,
          title: 'Search Result',
          icon: {
            url: '/assets/map/search-marker.png',
            scaledSize: new window.google.maps.Size(40, 40)
          }
        });

        // Remove the search marker after 5 seconds
        setTimeout(() => {
          searchMarker.setMap(null);
        }, 5000);
      }
    });
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          map.setCenter(pos);
          map.setZoom(12);
        },
        () => {
          console.error('Error: The Geolocation service failed.');
        }
      );
    }
  };

  return (
    <div className={`relative ${className}`}>
      {/* Search Bar */}
      {showSearch && (
        <div className="absolute top-4 left-4 right-4 z-10">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              placeholder="Search location..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-md focus:ring-2 focus:ring-teal-500 focus:border-transparent"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-teal-600 text-white rounded-lg shadow-md hover:bg-teal-700 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
            <button
              type="button"
              onClick={getCurrentLocation}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg shadow-md hover:bg-gray-700 transition-colors"
              title="Get current location"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </form>
        </div>
      )}

      {/* Map Container */}
      <div 
        ref={mapRef} 
        style={{ height: height, width: '100%' }}
        className="rounded-lg"
      />

      {/* Loading Overlay */}
      {!isLoaded && (
        <div className="absolute inset-0 bg-gray-200 rounded-lg flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-teal-500 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading map...</p>
          </div>
        </div>
      )}

      {/* Map Controls */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2">
        <button
          onClick={() => map && map.setZoom(map.getZoom() + 1)}
          className="w-10 h-10 bg-white border border-gray-300 rounded-lg shadow-md hover:bg-gray-50 flex items-center justify-center"
          title="Zoom in"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </button>
        <button
          onClick={() => map && map.setZoom(map.getZoom() - 1)}
          className="w-10 h-10 bg-white border border-gray-300 rounded-lg shadow-md hover:bg-gray-50 flex items-center justify-center"
          title="Zoom out"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18 12H6" />
          </svg>
        </button>
      </div>

      {/* Results Counter */}
      {items.length > 0 && (
        <div className="absolute bottom-4 left-4 bg-white border border-gray-300 rounded-lg shadow-md px-3 py-2">
          <span className="text-sm font-medium text-gray-700">
            {items.length} {items.length === 1 ? 'result' : 'results'} on map
          </span>
        </div>
      )}
    </div>
  );
};

export default MapView;