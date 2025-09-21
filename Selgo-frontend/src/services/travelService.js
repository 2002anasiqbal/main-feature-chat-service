// services/travelService.js
import axiosInstance from '@/utils/axiosInstance';

const TRAVEL_API_BASE = '/api/v1/travel';

export const travelService = {
  // Travel Listings
  async searchTravelListings(searchParams) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/search`, {
        params: searchParams
      });
      return response.data;
    } catch (error) {
      console.error('Error searching travel listings:', error);
      throw error;
    }
  },

  async getTravelListing(id) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching travel listing:', error);
      throw error;
    }
  },

  async createTravelListing(listingData) {
    try {
      const response = await axiosInstance.post(`${TRAVEL_API_BASE}/`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error creating travel listing:', error);
      throw error;
    }
  },

  async updateTravelListing(id, listingData) {
    try {
      const response = await axiosInstance.put(`${TRAVEL_API_BASE}/${id}`, listingData);
      return response.data;
    } catch (error) {
      console.error('Error updating travel listing:', error);
      throw error;
    }
  },

  async deleteTravelListing(id) {
    try {
      await axiosInstance.delete(`${TRAVEL_API_BASE}/${id}`);
      return true;
    } catch (error) {
      console.error('Error deleting travel listing:', error);
      throw error;
    }
  },

  // Travel Bookings
  async createBooking(bookingData) {
    try {
      const response = await axiosInstance.post(`${TRAVEL_API_BASE}/bookings`, bookingData);
      return response.data;
    } catch (error) {
      console.error('Error creating booking:', error);
      throw error;
    }
  },

  async getMyBookings(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/bookings/my-bookings`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my bookings:', error);
      throw error;
    }
  },

  async getMyListingBookings(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/bookings/my-listing-bookings`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my listing bookings:', error);
      throw error;
    }
  },

  async updateBookingStatus(bookingId, status) {
    try {
      const response = await axiosInstance.patch(
        `${TRAVEL_API_BASE}/bookings/${bookingId}/status`,
        { status }
      );
      return response.data;
    } catch (error) {
      console.error('Error updating booking status:', error);
      throw error;
    }
  },

  // Reviews
  async createReview(reviewData) {
    try {
      const response = await axiosInstance.post(`${TRAVEL_API_BASE}/reviews`, reviewData);
      return response.data;
    } catch (error) {
      console.error('Error creating review:', error);
      throw error;
    }
  },

  async getListingReviews(listingId, page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/reviews/${listingId}`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching listing reviews:', error);
      throw error;
    }
  },

  // Featured and Popular
  async getFeaturedListings(limit = 10) {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/featured/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching featured listings:', error);
      throw error;
    }
  },

  async getPopularDestinations() {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/popular/destinations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching popular destinations:', error);
      throw error;
    }
  },

  async getTravelTypes() {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/types/available`);
      return response.data;
    } catch (error) {
      console.error('Error fetching travel types:', error);
      throw error;
    }
  },

  // Statistics
  async getTravelStats() {
    try {
      const response = await axiosInstance.get(`${TRAVEL_API_BASE}/stats/overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching travel stats:', error);
      throw error;
    }
  }
};

export default travelService;