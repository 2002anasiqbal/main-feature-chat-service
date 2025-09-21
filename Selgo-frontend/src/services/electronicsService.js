// services/electronicsService.js
import axiosInstance from '@/utils/axiosInstance';

const ELECTRONICS_API_BASE = '/api/v1/electronics';

export const electronicsService = {
  // Electronics Listings
  async searchElectronics(searchParams) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/search`, {
        params: searchParams
      });
      return response.data;
    } catch (error) {
      console.error('Error searching electronics:', error);
      throw error;
    }
  },

  async getElectronicsItem(id) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching electronics item:', error);
      throw error;
    }
  },

  async createElectronicsListing(listingData) {
    try {
      const response = await axiosInstance.post(`${ELECTRONICS_API_BASE}/`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error creating electronics listing:', error);
      throw error;
    }
  },

  async updateElectronicsListing(id, listingData) {
    try {
      const response = await axiosInstance.put(`${ELECTRONICS_API_BASE}/${id}`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error updating electronics listing:', error);
      throw error;
    }
  },

  async deleteElectronicsListing(id) {
    try {
      await axiosInstance.delete(`${ELECTRONICS_API_BASE}/${id}`);
      return true;
    } catch (error) {
      console.error('Error deleting electronics listing:', error);
      throw error;
    }
  },

  // Categories and Brands
  async getCategories() {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/categories/list`);
      return response.data;
    } catch (error) {
      console.error('Error fetching electronics categories:', error);
      throw error;
    }
  },

  async getBrands() {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/brands/list`);
      return response.data;
    } catch (error) {
      console.error('Error fetching electronics brands:', error);
      throw error;
    }
  },

  async getPopularBrands() {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/brands/popular`);
      return response.data;
    } catch (error) {
      console.error('Error fetching popular brands:', error);
      throw error;
    }
  },

  // Featured and Popular
  async getFeaturedElectronics(limit = 10) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/featured/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching featured electronics:', error);
      throw error;
    }
  },

  async getLatestElectronics(limit = 10) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/latest/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching latest electronics:', error);
      throw error;
    }
  },

  async getDealsOfTheDay(limit = 10) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/deals/today`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching deals of the day:', error);
      throw error;
    }
  },

  // Price tracking and alerts
  async createPriceAlert(alertData) {
    try {
      const response = await axiosInstance.post(`${ELECTRONICS_API_BASE}/price-alerts`, alertData);
      return response.data;
    } catch (error) {
      console.error('Error creating price alert:', error);
      throw error;
    }
  },

  async getMyPriceAlerts(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/price-alerts/my-alerts`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my price alerts:', error);
      throw error;
    }
  },

  async deletePriceAlert(alertId) {
    try {
      await axiosInstance.delete(`${ELECTRONICS_API_BASE}/price-alerts/${alertId}`);
      return true;
    } catch (error) {
      console.error('Error deleting price alert:', error);
      throw error;
    }
  },

  // Favorites
  async addToFavorites(itemId) {
    try {
      const response = await axiosInstance.post(`${ELECTRONICS_API_BASE}/favorites`, {
        electronics_id: itemId
      });
      return response.data;
    } catch (error) {
      console.error('Error adding to favorites:', error);
      throw error;
    }
  },

  async removeFromFavorites(itemId) {
    try {
      await axiosInstance.delete(`${ELECTRONICS_API_BASE}/favorites/${itemId}`);
      return true;
    } catch (error) {
      console.error('Error removing from favorites:', error);
      throw error;
    }
  },

  async getMyFavorites(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/favorites/my-favorites`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my favorites:', error);
      throw error;
    }
  },

  // Statistics and trends
  async getElectronicsStats() {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/stats/overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching electronics stats:', error);
      throw error;
    }
  },

  async getPriceTrends(category, days = 30) {
    try {
      const response = await axiosInstance.get(`${ELECTRONICS_API_BASE}/trends/prices`, {
        params: { category, days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching price trends:', error);
      throw error;
    }
  },

  // Image upload
  async uploadImage(file, itemId) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('electronics_id', itemId);

      const response = await axiosInstance.post(
        `${ELECTRONICS_API_BASE}/images/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error uploading image:', error);
      throw error;
    }
  },

  async deleteImage(imageId) {
    try {
      await axiosInstance.delete(`${ELECTRONICS_API_BASE}/images/${imageId}`);
      return true;
    } catch (error) {
      console.error('Error deleting image:', error);
      throw error;
    }
  }
};

export default electronicsService;