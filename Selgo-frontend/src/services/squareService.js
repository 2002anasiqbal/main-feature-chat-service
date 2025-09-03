const API_URL = process.env.NEXT_PUBLIC_SQUARE_API_URL || 'http://localhost:8006/api/v1';

import { apiClient } from './authService';

const squareService = {
  searchItems: async (filters = {}, page = 1, perPage = 20) => {
    try {
      const params = new URLSearchParams({
        page: page.toString(),
        per_page: perPage.toString()
      });

      Object.entries(filters).forEach(([key, value]) => {
        if (value != null && value !== '' && value !== undefined) {
          params.append(key, value.toString());
        }
      });

      const url = `/square/search?${params}`;
      const response = await apiClient.get(url);

      if (!response.data) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = response.data;

      return {
        items: data.items || [],
        total: data.total || 0,
        page: page,
        per_page: perPage,
        pages: Math.ceil((data.total || 0) / perPage),
        has_next: data.total > page * perPage,
        has_prev: page > 1
      };
    } catch (error) {
      console.error('Error searching items:', error);
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
  },

  getCategories: async (skip = 0, limit = 100) => {
    try {
      const response = await apiClient.get(`/square/categories?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching item categories:', error);
      return [];
    }
  },

  getItems: async (skip = 0, limit = 10) => {
    try {
      const response = await apiClient.get(`/square?skip=${skip}&limit=${limit}&sort_by=created_at&sort_order=desc`);
      return response.data;
    } catch (error) {
      console.error('Error fetching items:', error);
      throw error;
    }
  },

  filterItems: async (filters) => {
    try {
      const response = await apiClient.post('/square/filter', filters);
      return response.data;
    } catch (error) {
      console.error('Error filtering items:', error.response?.data || error);
      throw error;
    }
  },

  getRecommendedItems: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/square/recommended?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommended items:', error);
      throw error;
    }
  },

  getItemDetails: async (itemId) => {
    try {
      const timestamp = Date.now();
      const response = await apiClient.get(`/square/${itemId}?t=${timestamp}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching item details:`, error);
      throw error;
    }
  },

  getFeaturedItems: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/square/featured?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching featured items:', error);
      throw error;
    }
  },

  getHomepageItems: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/square/homepage?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching homepage items:', error);
      throw error;
    }
  },

  createItem: async (itemData) => {
    try {
      const response = await apiClient.post('/square', itemData);
      return response.data;
    } catch (error) {
      console.error('Error creating item:', error);
      throw error;
    }
  },

  uploadImage: async (formData) => {
    try {
      const response = await apiClient.post('/square/upload-image', formData, {
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

  toggleFavorite: async (itemId) => {
    try {
      const response = await apiClient.post('/square/favorites/toggle', {
        item_id: itemId
      });
      return response.data;
    } catch (error) {
      console.error('Error toggling favorite:', error);
      throw error;
    }
  },

  async getUserFavorites(skip = 0, limit = 100) {
    try {
      const response = await apiClient.get(`/square/favorites`);
      return response.data || [];
    } catch (error) {
      console.error('Error fetching user favorites:', error.response?.data || error);
      return [];
    }
  },

  isItemFavorite: async (itemId) => {
    try {
      const response = await apiClient.get(`/square/${itemId}/is-favorite`);
      return response.data.is_favorite;
    } catch (error) {
      console.error('Error checking favorite status:', error);
      return false;
    }
  },
};

export default squareService;
