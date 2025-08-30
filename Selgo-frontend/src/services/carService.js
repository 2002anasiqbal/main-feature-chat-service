const API_URL = process.env.NEXT_PUBLIC_CAR_API_URL || 'http://localhost:8005/api/v1';

import { apiClient } from './authService';

const carService = {
  searchCars: async (filters = {}, page = 1, perPage = 20) => {
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

      const url = `/cars/search?${params}`;
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
      console.error('Error searching cars:', error);
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
      const response = await apiClient.get(`/cars/categories?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching car categories:', error);
      return [];
    }
  },

  getFeatures: async (skip = 0, limit = 100) => {
    try {
      const response = await apiClient.get(`/cars/features?skip=${skip}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching car features:', error);
      throw error;
    }
  },

  getCars: async (skip = 0, limit = 10) => {
    try {
      const response = await apiClient.get(`/cars?skip=${skip}&limit=${limit}&sort_by=created_at&sort_order=desc`);
      return response.data;
    } catch (error) {
      console.error('Error fetching cars:', error);
      throw error;
    }
  },

  filterCars: async (filters) => {
    try {
      const response = await apiClient.post('/cars/filter', filters);
      return response.data;
    } catch (error) {
      console.error('Error filtering cars:', error.response?.data || error);
      throw error;
    }
  },

  getRecommendedCars: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/cars/recommended?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching recommended cars:', error);
      throw error;
    }
  },

  getCarDetails: async (carId) => {
    try {
      const timestamp = Date.now();
      const response = await apiClient.get(`/cars/${carId}?t=${timestamp}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching car details:`, error);
      throw error;
    }
  },

  getFeaturedCars: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/cars/featured?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching featured cars:', error);
      throw error;
    }
  },

  getHomepageCars: async (limit = 10) => {
    try {
      const response = await apiClient.get(`/cars/homepage?limit=${limit}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching homepage cars:', error);
      throw error;
    }
  },

  createCar: async (carData) => {
    try {
      const response = await apiClient.post('/cars', carData);
      return response.data;
    } catch (error) {
      console.error('Error creating car:', error);
      throw error;
    }
  },

  uploadImage: async (formData) => {
    try {
      const response = await apiClient.post('/cars/upload-image', formData, {
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

  toggleFavorite: async (carId) => {
    try {
      const response = await apiClient.post('/cars/favorites/toggle', {
        car_id: carId
      });
      return response.data;
    } catch (error) {
      console.error('Error toggling favorite:', error);
      throw error;
    }
  },

  async getUserFavorites(skip = 0, limit = 100) {
    try {
      const response = await apiClient.get(`/cars/favorites`);
      return response.data || [];
    } catch (error) {
      console.error('Error fetching user favorites:', error.response?.data || error);
      return [];
    }
  },

  isCarFavorite: async (carId) => {
    try {
      const response = await apiClient.get(`/cars/${carId}/is-favorite`);
      return response.data.is_favorite;
    } catch (error) {
      console.error('Error checking favorite status:', error);
      return false;
    }
  },
};

export default carService;
