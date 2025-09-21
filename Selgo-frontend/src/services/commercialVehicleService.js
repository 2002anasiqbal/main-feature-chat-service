// services/commercialVehicleService.js
import axiosInstance from '@/utils/axiosInstance';

const COMMERCIAL_API_BASE = '/api/v1/commercial-vehicles';

export const commercialVehicleService = {
  // Commercial Vehicle Listings
  async searchCommercialVehicles(searchParams) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/search`, {
        params: searchParams
      });
      return response.data;
    } catch (error) {
      console.error('Error searching commercial vehicles:', error);
      throw error;
    }
  },

  async getCommercialVehicle(id) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching commercial vehicle:', error);
      throw error;
    }
  },

  async createCommercialVehicleListing(listingData) {
    try {
      const response = await axiosInstance.post(`${COMMERCIAL_API_BASE}/`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error creating commercial vehicle listing:', error);
      throw error;
    }
  },

  async updateCommercialVehicleListing(id, listingData) {
    try {
      const response = await axiosInstance.put(`${COMMERCIAL_API_BASE}/${id}`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error updating commercial vehicle listing:', error);
      throw error;
    }
  },

  async deleteCommercialVehicleListing(id) {
    try {
      await axiosInstance.delete(`${COMMERCIAL_API_BASE}/${id}`);
      return true;
    } catch (error) {
      console.error('Error deleting commercial vehicle listing:', error);
      throw error;
    }
  },

  // Vehicle Types and Categories
  async getVehicleTypes() {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/types/available`);
      return response.data;
    } catch (error) {
      console.error('Error fetching vehicle types:', error);
      throw error;
    }
  },

  async getBrands() {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/brands/list`);
      return response.data;
    } catch (error) {
      console.error('Error fetching commercial vehicle brands:', error);
      throw error;
    }
  },

  async getPopularBrands() {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/brands/popular`);
      return response.data;
    } catch (error) {
      console.error('Error fetching popular brands:', error);
      throw error;
    }
  },

  // Featured and Popular
  async getFeaturedVehicles(limit = 10) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/featured/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching featured commercial vehicles:', error);
      throw error;
    }
  },

  async getLatestVehicles(limit = 10) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/latest/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching latest commercial vehicles:', error);
      throw error;
    }
  },

  // Favorites
  async addToFavorites(vehicleId) {
    try {
      const response = await axiosInstance.post(`${COMMERCIAL_API_BASE}/favorites`, {
        vehicle_id: vehicleId
      });
      return response.data;
    } catch (error) {
      console.error('Error adding to favorites:', error);
      throw error;
    }
  },

  async removeFromFavorites(vehicleId) {
    try {
      await axiosInstance.delete(`${COMMERCIAL_API_BASE}/favorites/${vehicleId}`);
      return true;
    } catch (error) {
      console.error('Error removing from favorites:', error);
      throw error;
    }
  },

  async getMyFavorites(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/favorites/my-favorites`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my favorites:', error);
      throw error;
    }
  },

  // Financing and Leasing
  async getFinancingOptions(vehicleId) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/${vehicleId}/financing`);
      return response.data;
    } catch (error) {
      console.error('Error fetching financing options:', error);
      throw error;
    }
  },

  async calculateFinancing(vehicleId, financingData) {
    try {
      const response = await axiosInstance.post(
        `${COMMERCIAL_API_BASE}/${vehicleId}/financing/calculate`,
        financingData
      );
      return response.data;
    } catch (error) {
      console.error('Error calculating financing:', error);
      throw error;
    }
  },

  async getLeaseOptions(vehicleId) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/${vehicleId}/lease`);
      return response.data;
    } catch (error) {
      console.error('Error fetching lease options:', error);
      throw error;
    }
  },

  // Inspection and Reports
  async getInspectionReport(vehicleId) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/${vehicleId}/inspection`);
      return response.data;
    } catch (error) {
      console.error('Error fetching inspection report:', error);
      throw error;
    }
  },

  async requestInspection(vehicleId, inspectionData) {
    try {
      const response = await axiosInstance.post(
        `${COMMERCIAL_API_BASE}/${vehicleId}/inspection/request`,
        inspectionData
      );
      return response.data;
    } catch (error) {
      console.error('Error requesting inspection:', error);
      throw error;
    }
  },

  // Statistics and Market Data
  async getCommercialVehicleStats() {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/stats/overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching commercial vehicle stats:', error);
      throw error;
    }
  },

  async getMarketTrends(vehicleType, days = 30) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/trends/market`, {
        params: { vehicle_type: vehicleType, days }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching market trends:', error);
      throw error;
    }
  },

  async getPriceEstimate(vehicleData) {
    try {
      const response = await axiosInstance.post(`${COMMERCIAL_API_BASE}/price/estimate`, vehicleData);
      return response.data;
    } catch (error) {
      console.error('Error getting price estimate:', error);
      throw error;
    }
  },

  // Image upload
  async uploadImage(file, vehicleId) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('vehicle_id', vehicleId);

      const response = await axiosInstance.post(
        `${COMMERCIAL_API_BASE}/images/upload`,
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
      await axiosInstance.delete(`${COMMERCIAL_API_BASE}/images/${imageId}`);
      return true;
    } catch (error) {
      console.error('Error deleting image:', error);
      throw error;
    }
  },

  // Contact and Inquiries
  async sendInquiry(vehicleId, inquiryData) {
    try {
      const response = await axiosInstance.post(
        `${COMMERCIAL_API_BASE}/${vehicleId}/inquiry`,
        inquiryData
      );
      return response.data;
    } catch (error) {
      console.error('Error sending inquiry:', error);
      throw error;
    }
  },

  async getMyInquiries(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/inquiries/my-inquiries`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my inquiries:', error);
      throw error;
    }
  },

  async getReceivedInquiries(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${COMMERCIAL_API_BASE}/inquiries/received`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching received inquiries:', error);
      throw error;
    }
  }
};

export default commercialVehicleService;