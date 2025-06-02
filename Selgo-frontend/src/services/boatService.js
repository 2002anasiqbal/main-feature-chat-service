// const API_URL = 'https://d78u3s-ip-175-107-245-22.tunnelmole.net/api/v1';


import { apiClient } from './authService'; // Use the authenticated client from authService

const boatService = {
  // Get loan estimate
  getLoanEstimate: async (loanData) => {
    try {
      const response = await apiClient.post('/boats/loan-estimate', loanData);
      return response.data;
    } catch (error) {
      console.error('Error calculating loan estimate:', error);
      throw error;
    }
  },

  // Create fix done request
createFixRequest: async (requestData) => {
  try {
    const url = `/boats/${requestData.boat_id}/fix-requests`;
    console.log("Base URL:", apiClient.defaults.baseURL);
    console.log("Endpoint:", url);
    console.log("Full URL:", apiClient.defaults.baseURL + url);
    
    const response = await apiClient.post(url, requestData);
    return response.data;
  } catch (error) {
    console.error('Error creating fix request:', error.response?.status, error.response?.data);
    console.error('Request that failed:', {
      url: error.config?.url,
      method: error.config?.method,
      data: error.config?.data
    });
    throw error;
  }
},
  
  // Categories
  getCategories: async (skip = 0, limit = 100) => {
    try {
      console.log("Fetching boat categories from API");
      const response = await apiClient.get(`/boats/categories?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching boat categories:', error);
      return [];
    }
  },

  // Features
  getFeatures: async (skip = 0, limit = 100) => {
    try {
      const response = await apiClient.get(`/boats/features?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching boat features:', error);
      throw error;
    }
  },

  // Boat listings
getBoats: async (skip = 0, limit = 10) => {
  try {
    const response = await apiClient.get(`/boats?skip=${skip}&limit=${limit}&sort_by=created_at&sort_order=desc`);
    return response.data;
  } catch (error) {
    console.error('Error fetching boats:', error);
    throw error;
  }
},
  // Filter boats - Enhanced for sidebar filtering
  filterBoats: async (filters) => {
  try {
    console.log("🚀 boatService: Sending filter request to API:", JSON.stringify(filters, null, 2));
    
    const response = await apiClient.post('/boats/filter', filters);
    
    console.log(`🚀 boatService: Filter API response contains ${response.data?.items?.length || 0} boats`);
    
    if (response.data?.items?.length === 0) {
      console.log("No boats found for filter criteria:", filters);
    }
    
    return response.data;
  } catch (error) {
    console.error('Error filtering boats:', error.response?.data || error);
    throw error;
  }
},

  // Get recommended boats
  getRecommendedBoats: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/boats/recommended?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommended boats:', error);
      throw error;
    }
  },

  // Get boat details

getBoatDetails: async (boatId) => {
  try {
    // Add a cache-busting parameter
    const timestamp = Date.now();
    const response = await apiClient.get(`/boats/${boatId}?t=${timestamp}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching boat details:`, error);
    throw error;
  }
},

  // Search boats by term
  searchBoats: async (searchTerm, limit = 10) => {
    try {
      const filters = {
        search_term: searchTerm,
        limit: limit,
        offset: 0
      };
      const response = await apiClient.post('/boats/filter', filters);
      return response.data;
    } catch (error) {
      console.error('Error searching boats:', error);
      throw error;
    }
  },
  
  // For map-based searching with geolocation
  searchBoatsByLocation: async (latitude, longitude, distance = 50, limit = 20) => {
    try {
      const filters = {
        location: {
          latitude,
          longitude
        },
        distance, // in kilometers
        limit,
        offset: 0
      };
      const response = await apiClient.post('/boats/filter', filters);
      return response.data;
    } catch (error) {
      console.error('Error searching boats by location:', error);
      throw error;
    }
  },

// Get featured boats for homepage slider
getFeaturedBoats: async (limit = 10) => {
  try {
    const response = await apiClient.get(`/boats/featured?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching featured boats:', error);
    throw error;
  }
},

// Get homepage boats for "Find the boats that suits you"
getHomepageBoats: async (limit = 10) => {
  try {
    const response = await apiClient.get(`/boats/homepage?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching homepage boats:', error);
    throw error;
  }
},

// Mark newly created boat in localStorage for frontend priority
markNewlyCreated: (boatId) => {
  localStorage.setItem('newlyCreatedBoatId', boatId.toString());
  localStorage.setItem('newlyCreatedBoatTimestamp', Date.now().toString());
},
  
createBoat: async (boatData) => {
  try {
    // The backend doesn't have 'featured' or 'recommended' fields,
    // but we can sort by creation date to prioritize new boats
    const response = await apiClient.post('/boats', boatData);
    return response.data;
  } catch (error) {
    console.error('Error creating boat:', error);
    throw error;
  }
},
// Add this utility function to force-refresh data
checkLatestBoats: async () => {
  try {
    // Add a timestamp to prevent caching
    const timestamp = new Date().getTime();
    const response = await apiClient.get(`/boats?skip=0&limit=5&sort_by=created_at&sort_order=desc&t=${timestamp}`);
    console.log("Latest boats from API:", response.data);
    return response.data;
  } catch (error) {
    console.error('Error checking latest boats:', error);
    throw error;
  }
},
uploadImage: async (formData) => {
  try {
    const response = await apiClient.post('/boats/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading image:', error);
    throw error;
  }
}

};

export default boatService;