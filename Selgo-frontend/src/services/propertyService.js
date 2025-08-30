<<<<<<< HEAD
// Selgo-frontend/src/services/propertyService.js (Updated with Points 6-10)
class PropertyService {
  constructor() {
    this.baseURL = process.env.NEXT_PUBLIC_PROPERTY_SERVICE_URL || 'http://localhost:8004/api/properties';
  }

  // Helper method for API calls
  async apiCall(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Property service API call failed:', error);
      throw error;
    }
  }

  // Helper to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('auth_token'); // Adjust based on your auth implementation
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  // Points 1-5 (Existing methods)
  async getPropertyCategories(propertyType = null) {
    const params = new URLSearchParams();
    if (propertyType) {
      params.append('property_type', propertyType);
    }
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/categories${queryString}`);
  }

  async searchProperties(filters = {}) {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/search${queryString}`);
  }

  async getFeaturedProperties(limit = 10) {
    return this.apiCall(`/featured?limit=${limit}`);
  }

  async getRecommendedProperties(propertyType = null, limit = 10) {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    if (propertyType) {
      params.append('property_type', propertyType);
    }
    
    return this.apiCall(`/recommended?${params.toString()}`);
  }

  async getPropertyById(propertyId, userId = null) {
    const params = new URLSearchParams();
    if (userId) {
      params.append('user_id', userId);
    }
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/${propertyId}${queryString}`);
  }

  async contactPropertyOwner(propertyId, messageData) {
    return this.apiCall(`/${propertyId}/contact`, {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }

  // Point 6: Property Map Location Module
  async getPropertyLocation(propertyId) {
    return this.apiCall(`/${propertyId}/location`);
  }

  async searchPropertiesByMap(searchData) {
    return this.apiCall('/map/search', {
      method: 'POST',
      body: JSON.stringify(searchData),
      headers: this.getAuthHeaders()
    });
  }

  async getNearbyPlaces(propertyId) {
    return this.apiCall(`/${propertyId}/nearby`);
  }

  // Point 7: Property Comparison Module
  async createPropertyComparison(propertyIds, comparisonName = null) {
    const data = {
      property_ids: propertyIds,
      comparison_name: comparisonName,
      session_id: this.generateSessionId()
    };
    
    return this.apiCall('/compare', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: this.getAuthHeaders()
    });
  }

  async getPropertyComparison(sessionId) {
    return this.apiCall(`/compare/${sessionId}`);
  }

  async addComparisonNote(sessionId, propertyId, noteText, noteCategory = null) {
    const params = new URLSearchParams();
    params.append('note_text', noteText);
    if (noteCategory) {
      params.append('note_category', noteCategory);
    }
    
    return this.apiCall(`/compare/${sessionId}/notes?${params.toString()}`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
  }

  // Point 8: Property Loan Estimator Module
  async calculateLoanEstimate(loanData) {
    return this.apiCall('/loan-estimate', {
      method: 'POST',
      body: JSON.stringify(loanData),
      headers: this.getAuthHeaders()
    });
  }

  async getLoanProviders() {
    return this.apiCall('/loan-providers');
  }

  async getUserLoanEstimates(userId) {
    return this.apiCall(`/users/${userId}/loan-estimates`, {
      headers: this.getAuthHeaders()
    });
  }

  // Point 9: New Rental Ad Module
  async createRentalAd(rentalData) {
    return this.apiCall('/rentals', {
      method: 'POST',
      body: JSON.stringify(rentalData),
      headers: this.getAuthHeaders()
    });
  }

  async getRentalProperties(filters = {}) {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/rentals${queryString}`);
  }

  async submitRentalApplication(rentalId, applicationData) {
    return this.apiCall(`/rentals/${rentalId}/applications`, {
      method: 'POST',
      body: JSON.stringify(applicationData),
      headers: this.getAuthHeaders()
    });
  }

  async getRentalSuggestions(filters = {}) {
    const params = new URLSearchParams();
    
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== '') {
        params.append(key, value.toString());
      }
    });
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/rentals/suggestions${queryString}`, {
      headers: this.getAuthHeaders()
    });
  }

  // Point 10: Lease Contract Module
  async getLeaseTemplates() {
    return this.apiCall('/lease/templates');
  }

  async createLeaseContract(contractData) {
    return this.apiCall('/lease/contracts', {
      method: 'POST',
      body: JSON.stringify(contractData),
      headers: this.getAuthHeaders()
    });
  }

  async signLeaseContract(contractId, userType) {
    const params = new URLSearchParams();
    params.append('user_type', userType);
    
    return this.apiCall(`/lease/contracts/${contractId}/sign?${params.toString()}`, {
      method: 'POST',
      headers: this.getAuthHeaders()
    });
  }

  async getLeaseContract(contractId) {
    return this.apiCall(`/lease/contracts/${contractId}`, {
      headers: this.getAuthHeaders()
    });
  }

  // Utility methods
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  async getPopularCities() {
    return this.apiCall('/utils/popular-cities');
  }

  async getRentalTips() {
    return this.apiCall('/utils/rental-tips');
  }

  async submitFeedback(feedbackData) {
    return this.apiCall('/utils/feedback', {
      method: 'POST',
      body: JSON.stringify(feedbackData),
    });
  }

  async getPriceInsights(city = null) {
    const params = new URLSearchParams();
    if (city) {
      params.append('city', city);
    }
    
    const queryString = params.toString() ? `?${params.toString()}` : '';
    return this.apiCall(`/utils/price-insights${queryString}`);
  }

  // Advanced search with map integration
  async searchWithMapBounds(bounds, filters = {}) {
    const center_lat = (bounds.north + bounds.south) / 2;
    const center_lng = (bounds.east + bounds.west) / 2;
    
    // Calculate radius from bounds
    const radius_km = this.calculateDistanceFromBounds(bounds);
    
    const searchData = {
      center_lat,
      center_lng,
      radius_km,
      filters,
      session_id: this.generateSessionId()
    };
    
    return this.searchPropertiesByMap(searchData);
  }

  calculateDistanceFromBounds(bounds) {
    // Simple calculation - in production, use more accurate method
    const latDiff = bounds.north - bounds.south;
    const lngDiff = bounds.east - bounds.west;
    return Math.max(latDiff, lngDiff) * 111; // Rough km conversion
  }

  // Format property for display (existing method)
  formatPropertyForDisplay(property) {
    return {
      id: property.id,
      image: property.images && property.images.length > 0 
        ? property.images.find(img => img.is_primary)?.image_url || property.images[0].image_url
        : "/assets/property/property.jpeg",
      title: property.title || "Property",
      description: this.formatPropertyDescription(property),
      price: property.price ? `$${Number(property.price).toLocaleString()}` : "Price on request",
      originalData: property
    };
  }

  formatPropertyDescription(property) {
    const parts = [];
    
    if (property.bedrooms) {
      parts.push(`${property.bedrooms} bedroom${property.bedrooms > 1 ? 's' : ''}`);
    }
    
    if (property.use_area) {
      parts.push(`${property.use_area}m²`);
    }
    
    if (property.city) {
      parts.push(property.city);
    }
    
    return parts.join(' • ') || 'No details available';
  }

  async getHomepageProperties(limit = 10) {
    try {
      const featured = await this.getFeaturedProperties(limit);
      return featured.map(property => this.formatPropertyForDisplay(property));
    } catch (error) {
      console.error('Failed to fetch homepage properties:', error);
      return [];
    }
  }

  // Property comparison utilities
  async saveComparison(sessionId, comparisonName) {
    return this.apiCall(`/compare/${sessionId}/save`, {
      method: 'POST',
      body: JSON.stringify({ comparison_name: comparisonName }),
      headers: this.getAuthHeaders()
    });
  }

  // Loan calculation utilities
  calculateMonthlyPayment(principal, annualRate, years) {
    const monthlyRate = annualRate / 100 / 12;
    const numPayments = years * 12;
    
    if (monthlyRate === 0) {
      return principal / numPayments;
    }
    
    return principal * (monthlyRate * Math.pow(1 + monthlyRate, numPayments)) /
           (Math.pow(1 + monthlyRate, numPayments) - 1);
  }

  // Quick loan estimate (client-side calculation)
  quickLoanEstimate(propertyPrice, downPayment, interestRate, years) {
    const loanAmount = propertyPrice - downPayment;
    const monthlyPayment = this.calculateMonthlyPayment(loanAmount, interestRate, years);
    const totalPayment = monthlyPayment * years * 12;
    const totalInterest = totalPayment - loanAmount;
    
    return {
      loanAmount,
      monthlyPayment,
      totalPayment,
      totalInterest
    };
  }
}

// Create and export singleton instance
const propertyService = new PropertyService();
=======
const API_URL = process.env.NEXT_PUBLIC_PROPERTY_API_URL || 'http://localhost:8004/api/v1';

import { apiClient } from './authService';

const propertyService = {
  getCategories: async () => {
    try {
      const response = await apiClient.get(`/properties/categories`);
      return response.data;
    } catch (error) {
      console.error('Error fetching property categories:', error);
      return [];
    }
  },

  filterProperties: async (filters) => {
    try {
      const response = await apiClient.post('/properties/filter', filters);
      return response.data;
    } catch (error) {
      console.error('Error filtering properties:', error.response?.data || error);
      throw error;
    }
  },

  getPropertyDetails: async (propertyId) => {
    try {
      const timestamp = Date.now();
      const response = await apiClient.get(`/properties/${propertyId}?t=${timestamp}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching property details:`, error);
      throw error;
    }
  },

  createProperty: async (propertyData) => {
    try {
      const response = await apiClient.post('/properties', propertyData);
      return response.data;
    } catch (error) {
      console.error('Error creating property:', error);
      throw error;
    }
  },

  uploadImage: async (formData) => {
    try {
      const response = await apiClient.post('/properties/upload-image', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
    }
  },
};

>>>>>>> ef864b3 (Replace Features branch with selgo-feature contents)
export default propertyService;