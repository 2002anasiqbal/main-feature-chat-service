// services/holidayRentalService.js
import axiosInstance from '@/utils/axiosInstance';

const HOLIDAY_RENTAL_API_BASE = '/api/v1/properties/api/v1/holiday-rentals';

export const holidayRentalService = {
  // Holiday Rental Listings
  async searchHolidayRentals(searchParams) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/search`, {
        params: searchParams
      });
      return response.data;
    } catch (error) {
      console.error('Error searching holiday rentals:', error);
      throw error;
    }
  },

  async getHolidayRental(id) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching holiday rental:', error);
      throw error;
    }
  },

  async createHolidayRental(rentalData) {
    try {
      const response = await axiosInstance.post(`${HOLIDAY_RENTAL_API_BASE}/`, rentalData);
      return response.data;
    } catch (error) {
      console.error('Error creating holiday rental:', error);
      throw error;
    }
  },

  async updateHolidayRental(id, rentalData) {
    try {
      const response = await axiosInstance.put(`${HOLIDAY_RENTAL_API_BASE}/${id}`, rentalData);
      return response.data;
    } catch (error) {
      console.error('Error updating holiday rental:', error);
      throw error;
    }
  },

  async deleteHolidayRental(id) {
    try {
      await axiosInstance.delete(`${HOLIDAY_RENTAL_API_BASE}/${id}`);
      return true;
    } catch (error) {
      console.error('Error deleting holiday rental:', error);
      throw error;
    }
  },

  // Bookings
  async createBooking(bookingData) {
    try {
      const response = await axiosInstance.post(`${HOLIDAY_RENTAL_API_BASE}/bookings`, bookingData);
      return response.data;
    } catch (error) {
      console.error('Error creating booking:', error);
      throw error;
    }
  },

  async getMyBookings(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/bookings/my-bookings`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my bookings:', error);
      throw error;
    }
  },

  async getMyPropertyBookings(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/bookings/my-property-bookings`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my property bookings:', error);
      throw error;
    }
  },

  async updateBookingStatus(bookingId, status) {
    try {
      const response = await axiosInstance.patch(
        `${HOLIDAY_RENTAL_API_BASE}/bookings/${bookingId}/status`,
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
      const response = await axiosInstance.post(`${HOLIDAY_RENTAL_API_BASE}/reviews`, reviewData);
      return response.data;
    } catch (error) {
      console.error('Error creating review:', error);
      throw error;
    }
  },

  async getRentalReviews(rentalId, page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/${rentalId}/reviews`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching rental reviews:', error);
      throw error;
    }
  },

  // Featured and Popular
  async getFeaturedRentals(limit = 10) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/featured/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching featured rentals:', error);
      throw error;
    }
  },

  async getPopularDestinations() {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/popular/destinations`);
      return response.data;
    } catch (error) {
      console.error('Error fetching popular destinations:', error);
      throw error;
    }
  },

  async getAvailableRentalTypes() {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/types/available`);
      return response.data;
    } catch (error) {
      console.error('Error fetching rental types:', error);
      throw error;
    }
  },

  // Availability Management
  async checkAvailability(rentalId, checkIn, checkOut) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/${rentalId}/availability`, {
        params: { check_in: checkIn, check_out: checkOut }
      });
      return response.data;
    } catch (error) {
      console.error('Error checking availability:', error);
      throw error;
    }
  },

  async updateAvailability(rentalId, availabilityData) {
    try {
      const response = await axiosInstance.post(
        `${HOLIDAY_RENTAL_API_BASE}/${rentalId}/availability`,
        availabilityData
      );
      return response.data;
    } catch (error) {
      console.error('Error updating availability:', error);
      throw error;
    }
  },

  // Pricing
  async calculatePrice(rentalId, checkIn, checkOut, guests) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/${rentalId}/price`, {
        params: { check_in: checkIn, check_out: checkOut, guests }
      });
      return response.data;
    } catch (error) {
      console.error('Error calculating price:', error);
      throw error;
    }
  },

  async updatePricing(rentalId, pricingData) {
    try {
      const response = await axiosInstance.put(
        `${HOLIDAY_RENTAL_API_BASE}/${rentalId}/pricing`,
        pricingData
      );
      return response.data;
    } catch (error) {
      console.error('Error updating pricing:', error);
      throw error;
    }
  },

  // Favorites and Wishlist
  async addToWishlist(rentalId) {
    try {
      const response = await axiosInstance.post(`${HOLIDAY_RENTAL_API_BASE}/wishlist`, {
        rental_id: rentalId
      });
      return response.data;
    } catch (error) {
      console.error('Error adding to wishlist:', error);
      throw error;
    }
  },

  async removeFromWishlist(rentalId) {
    try {
      await axiosInstance.delete(`${HOLIDAY_RENTAL_API_BASE}/wishlist/${rentalId}`);
      return true;
    } catch (error) {
      console.error('Error removing from wishlist:', error);
      throw error;
    }
  },

  async getMyWishlist(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/wishlist/my-wishlist`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my wishlist:', error);
      throw error;
    }
  },

  // Statistics and Analytics
  async getHolidayRentalStats() {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/stats/overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching holiday rental stats:', error);
      throw error;
    }
  },

  async getOwnerDashboard() {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/dashboard/owner`);
      return response.data;
    } catch (error) {
      console.error('Error fetching owner dashboard:', error);
      throw error;
    }
  },

  async getBookingTrends(rentalId, period = '30d') {
    try {
      const response = await axiosInstance.get(
        `${HOLIDAY_RENTAL_API_BASE}/${rentalId}/trends/bookings`,
        { params: { period } }
      );
      return response.data;
    } catch (error) {
      console.error('Error fetching booking trends:', error);
      throw error;
    }
  },

  // Search Filters and Suggestions
  async getSearchSuggestions(query) {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/search/suggestions`, {
        params: { q: query }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching search suggestions:', error);
      throw error;
    }
  },

  async getFilterOptions() {
    try {
      const response = await axiosInstance.get(`${HOLIDAY_RENTAL_API_BASE}/search/filters`);
      return response.data;
    } catch (error) {
      console.error('Error fetching filter options:', error);
      throw error;
    }
  },

  // Image Management
  async uploadImage(file, rentalId) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('rental_id', rentalId);

      const response = await axiosInstance.post(
        `${HOLIDAY_RENTAL_API_BASE}/images/upload`,
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
      await axiosInstance.delete(`${HOLIDAY_RENTAL_API_BASE}/images/${imageId}`);
      return true;
    } catch (error) {
      console.error('Error deleting image:', error);
      throw error;
    }
  },

  async reorderImages(rentalId, imageOrder) {
    try {
      const response = await axiosInstance.put(
        `${HOLIDAY_RENTAL_API_BASE}/${rentalId}/images/reorder`,
        { image_order: imageOrder }
      );
      return response.data;
    } catch (error) {
      console.error('Error reordering images:', error);
      throw error;
    }
  }
};

export default holidayRentalService;