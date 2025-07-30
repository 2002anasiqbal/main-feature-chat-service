// Selgo-frontend/src/services/motorcycleService.js

const API_BASE_URL = process.env.NEXT_PUBLIC_MOTORCYCLE_API_URL || 'http://localhost:8003/api';

class MotorcycleService {
  
  // Helper method to get auth headers
  getAuthHeaders() {
    const token = localStorage.getItem('accessToken');
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    return headers;
  }

  // Helper method to make authenticated requests
  async makeAuthenticatedRequest(url, options = {}) {
    const headers = this.getAuthHeaders();
    
    const requestOptions = {
      ...options,
      headers: {
        ...headers,
        ...options.headers
      }
    };
    
    return fetch(url, requestOptions);
  }

  // NEW: Get motorcycles for homepage with better error handling
  async getHomepageMotorcycles(limit = 50) {
    try {
      console.log(`🌐 Fetching homepage motorcycles from: ${API_BASE_URL}/motorcycles/search`);
      
      const response = await fetch(`${API_BASE_URL}/motorcycles/search?per_page=${limit}`);
      
      console.log("📥 Response status:", response.status);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📊 Homepage motorcycles response:", data);
      
      return data.items || [];
    } catch (error) {
      console.error('❌ Error fetching homepage motorcycles:', error);
      return [];
    }
  }  

  // Calculate loan with proper number formatting
  async calculateLoan(loanData) {
    try {
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/tools/motorcycle-loans`, {
        method: 'POST',
        body: JSON.stringify(loanData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📥 Loan calculation response:", data);
      
      return {
        price: Number(data.price),
        term_months: Number(data.term_months),
        interest_rate: Number(data.interest_rate),
        monthly_payment: Number(data.monthly_payment),
        total_amount: Number(data.total_amount),
        total_interest: Number(data.total_interest)
      };
    } catch (error) {
      console.error('❌ Error calculating loan:', error);
      throw error;
    }
  }

  // Get all categories
  async getCategories() {
    try {
      const response = await fetch(`${API_BASE_URL}/categories/all`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📥 Categories response:", data);
      return data.categories || [];
    } catch (error) {
      console.error('❌ Error fetching categories:', error);
      throw error;
    }
  }  

  // Create new motorcycle ad
  async createMotorcycle(motorcycleData) {
    try {
      console.log("🌐 API URL:", `${API_BASE_URL}/motorcycles/new`);
      console.log("📤 Sending data:", motorcycleData);
      
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/new`, {
        method: 'POST',
        body: JSON.stringify(motorcycleData),
      });
      
      console.log("📥 Response status:", response.status);
      console.log("📥 Response headers:", response.headers);
      
      const responseText = await response.text();
      console.log("📥 Response text:", responseText);
      
      if (!response.ok) {
        let errorData;
        try {
          errorData = JSON.parse(responseText);
        } catch (e) {
          errorData = { detail: responseText };
        }
        
        console.error("❌ API Error Response:", errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      const result = JSON.parse(responseText);
      console.log("✅ Success response:", result);
      return result;
      
    } catch (error) {
      console.error('❌ Error creating motorcycle:', error);
      throw error;
    }
  }

  // Get motorcycles by category
  async getMotorcyclesByCategory(categoryName, page = 1, perPage = 20) {
    try {
      return await this.searchMotorcycles({ category_name: categoryName }, page, perPage);
    } catch (error) {
      console.error(`❌ Error fetching motorcycles for category "${categoryName}":`, error);
      throw error;
    }
  }

  // Search motorcycles (UPDATED with better error handling)
  async searchMotorcycles(filters = {}, page = 1, perPage = 20) {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: perPage.toString()
      });

      Object.entries(filters).forEach(([key, value]) => {
        if (value != null && value !== '' && value !== undefined) {
          if (key === 'motorcycle_types' && Array.isArray(value)) {
            params.append('motorcycle_types', value.join(','));
          } else {
            params.append(key, value.toString());
          }
        }
      });

      const url = `${API_BASE_URL}/motorcycles/search?${params}`;
      console.log("🌐 Making request to:", url);

      const response = await fetch(url);
      
      if (!response.ok) {
        console.error(`❌ Search API error: ${response.status}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📥 Search response:", data);
      
      return {
        items: data.items || [],
        total: data.total || 0,
        page: data.page || page,
        per_page: data.per_page || perPage,
        pages: data.pages || 0,
        has_next: data.has_next || false,
        has_prev: data.has_prev || false
      };
    } catch (error) {
      console.error('❌ Error searching motorcycles:', error);
      return {
        items: [],
        total: 0,
        page: page,
        per_page: perPage,
        pages: 0,
        has_next: false,
        has_prev: false
      };
    }
  }

  // Get motorcycle details
  async getMotorcycleDetail(motorcycleId) {
    try {
      const response = await fetch(`${API_BASE_URL}/motorcycles/${motorcycleId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log("📥 Motorcycle detail response:", data);
      return data;
    } catch (error) {
      console.error('❌ Error fetching motorcycle details:', error);
      throw error;
    }
  }

  // Format motorcycle data for existing BoatCard component (reuse existing UI)
  formatMotorcycleForDisplay(motorcycle) {
    return {
      id: motorcycle.id,
      title: motorcycle.title || "Unnamed Motorcycle",
      description: motorcycle.brand && motorcycle.model 
        ? `${motorcycle.brand} ${motorcycle.model} - ${motorcycle.year}`.trim() 
        : motorcycle.city || "No details available",
      price: motorcycle.price ? `${motorcycle.price.toLocaleString()} kr` : "Price unavailable",
      image: motorcycle.primary_image || (motorcycle.images && motorcycle.images.length > 0 ? motorcycle.images[0].image_url : null),
      originalData: motorcycle
    };
  }

  async getFilterOptions() {
    try {
      const response = await fetch(`${API_BASE_URL}/motorcycles/filter/sidebar`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error fetching filter options:', error);
      throw error;
    }
  }

  async filterMotorcyclesByLocation(mapFilterData, page = 1, perPage = 20) {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: perPage.toString()
      });

      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/filter/map?${params}`, {
        method: 'POST',
        body: JSON.stringify(mapFilterData),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error filtering motorcycles by location:', error);
      throw error;
    }
  }

  // ==================== Favorites Methods ====================
  
  // Toggle favorite status
  async toggleFavorite(motorcycleId) {
    try {
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/favorites/toggle`, {
        method: 'POST',
        body: JSON.stringify({
          motorcycle_id: motorcycleId
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Toggle favorite response:', data);
      return data;
    } catch (error) {
      console.error('❌ Error toggling favorite:', error);
      throw error;
    }
  }

  // Get user's favorite motorcycles
  async getUserFavorites(skip = 0, limit = 100) {
    try {
      console.log('🔍 Fetching motorcycle favorites...');
      
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/favorites-simple`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('✅ Motorcycle Favorites response:', data);
      return data || [];
      
    } catch (error) {
      console.error('❌ Error fetching motorcycle favorites:', error);
      return [];
    }
  }

  // Get favorites count
  async getFavoritesCount() {
    try {
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/favorites/count`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.count;
    } catch (error) {
      console.error('❌ Error fetching favorites count:', error);
      return 0;
    }
  }

  // Check if motorcycle is favorite
  async isMotorcycleFavorite(motorcycleId) {
    try {
      const response = await this.makeAuthenticatedRequest(`${API_BASE_URL}/motorcycles/${motorcycleId}/is-favorite`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data.is_favorite;
    } catch (error) {
      console.error('❌ Error checking favorite status:', error);
      return false;
    }
  }
}

const motorcycleService = new MotorcycleService();
export default motorcycleService;