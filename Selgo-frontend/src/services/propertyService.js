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

export default propertyService;