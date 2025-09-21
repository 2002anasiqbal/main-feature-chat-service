// services/carAuctionService.js
import axiosInstance from '@/utils/axiosInstance';

const CAR_AUCTION_API_BASE = '/api/v1/cars/api/v1/car-auctions';

export const carAuctionService = {
  // Auction Management
  async searchAuctions(searchParams) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/search`, {
        params: searchParams
      });
      return response.data;
    } catch (error) {
      console.error('Error searching auctions:', error);
      throw error;
    }
  },

  async getAuction(id) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching auction:', error);
      throw error;
    }
  },

  async createAuction(auctionData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/`, auctionData);
      return response.data;
    } catch (error) {
      console.error('Error creating auction:', error);
      throw error;
    }
  },

  async updateAuction(id, auctionData) {
    try {
      const response = await axiosInstance.put(`${CAR_AUCTION_API_BASE}/${id}`, auctionData);
      return response.data;
    } catch (error) {
      console.error('Error updating auction:', error);
      throw error;
    }
  },

  async cancelAuction(id) {
    try {
      await axiosInstance.delete(`${CAR_AUCTION_API_BASE}/${id}/cancel`);
      return true;
    } catch (error) {
      console.error('Error cancelling auction:', error);
      throw error;
    }
  },

  // Bidding
  async placeBid(bidData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/bids`, bidData);
      return response.data;
    } catch (error) {
      console.error('Error placing bid:', error);
      throw error;
    }
  },

  async getAuctionBids(auctionId, page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/${auctionId}/bids`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching auction bids:', error);
      throw error;
    }
  },

  async getMyBids(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/bids/my-bids`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my bids:', error);
      throw error;
    }
  },

  // Watchlist
  async watchAuction(watcherData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/watch`, watcherData);
      return response.data;
    } catch (error) {
      console.error('Error watching auction:', error);
      throw error;
    }
  },

  async unwatchAuction(auctionId) {
    try {
      await axiosInstance.delete(`${CAR_AUCTION_API_BASE}/${auctionId}/unwatch`);
      return true;
    } catch (error) {
      console.error('Error unwatching auction:', error);
      throw error;
    }
  },

  async getWatchedAuctions(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/watchlist/my-watched`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching watched auctions:', error);
      throw error;
    }
  },

  // Dashboard and Statistics
  async getSellerDashboard() {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/dashboard/seller`);
      return response.data;
    } catch (error) {
      console.error('Error fetching seller dashboard:', error);
      throw error;
    }
  },

  async getBidderDashboard() {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/dashboard/bidder`);
      return response.data;
    } catch (error) {
      console.error('Error fetching bidder dashboard:', error);
      throw error;
    }
  },

  async getAuctionStats() {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/stats/overview`);
      return response.data;
    } catch (error) {
      console.error('Error fetching auction stats:', error);
      throw error;
    }
  },

  // Featured and Popular
  async getFeaturedAuctions(limit = 10) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/featured/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching featured auctions:', error);
      throw error;
    }
  },

  async getEndingSoonAuctions(limit = 10) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/ending-soon/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching ending soon auctions:', error);
      throw error;
    }
  },

  async getNoReserveAuctions(limit = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/no-reserve/list`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching no-reserve auctions:', error);
      throw error;
    }
  },

  async getPopularCategories() {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/categories/popular`);
      return response.data;
    } catch (error) {
      console.error('Error fetching popular categories:', error);
      throw error;
    }
  },

  async getWeeklyTrends() {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/trends/weekly`);
      return response.data;
    } catch (error) {
      console.error('Error fetching weekly trends:', error);
      throw error;
    }
  },

  // Auction History and Reports
  async getAuctionHistory(auctionId) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/${auctionId}/history`);
      return response.data;
    } catch (error) {
      console.error('Error fetching auction history:', error);
      throw error;
    }
  },

  async getMyAuctionHistory(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/history/my-auctions`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my auction history:', error);
      throw error;
    }
  },

  async getWonAuctions(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/won/my-wins`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching won auctions:', error);
      throw error;
    }
  },

  // Notifications and Alerts
  async getAuctionNotifications(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/notifications`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching auction notifications:', error);
      throw error;
    }
  },

  async markNotificationAsRead(notificationId) {
    try {
      await axiosInstance.patch(`${CAR_AUCTION_API_BASE}/notifications/${notificationId}/read`);
      return true;
    } catch (error) {
      console.error('Error marking notification as read:', error);
      throw error;
    }
  },

  async setAuctionAlert(alertData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/alerts`, alertData);
      return response.data;
    } catch (error) {
      console.error('Error setting auction alert:', error);
      throw error;
    }
  },

  async getMyAlerts(page = 1, perPage = 20) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/alerts/my-alerts`, {
        params: { page, per_page: perPage }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching my alerts:', error);
      throw error;
    }
  },

  async deleteAlert(alertId) {
    try {
      await axiosInstance.delete(`${CAR_AUCTION_API_BASE}/alerts/${alertId}`);
      return true;
    } catch (error) {
      console.error('Error deleting alert:', error);
      throw error;
    }
  },

  // Real-time Updates
  async getAuctionUpdates(auctionId, lastUpdateTime) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/${auctionId}/updates`, {
        params: { since: lastUpdateTime }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching auction updates:', error);
      throw error;
    }
  },

  // Auction Validation and Estimates
  async validateAuctionData(auctionData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/validate`, auctionData);
      return response.data;
    } catch (error) {
      console.error('Error validating auction data:', error);
      throw error;
    }
  },

  async getEstimatedValue(carData) {
    try {
      const response = await axiosInstance.post(`${CAR_AUCTION_API_BASE}/estimate-value`, carData);
      return response.data;
    } catch (error) {
      console.error('Error getting estimated value:', error);
      throw error;
    }
  },

  async getSimilarAuctions(auctionId, limit = 5) {
    try {
      const response = await axiosInstance.get(`${CAR_AUCTION_API_BASE}/${auctionId}/similar`, {
        params: { limit }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching similar auctions:', error);
      throw error;
    }
  },

  // Image and Document Management
  async uploadAuctionImage(file, auctionId) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('auction_id', auctionId);

      const response = await axiosInstance.post(
        `${CAR_AUCTION_API_BASE}/images/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error uploading auction image:', error);
      throw error;
    }
  },

  async deleteAuctionImage(imageId) {
    try {
      await axiosInstance.delete(`${CAR_AUCTION_API_BASE}/images/${imageId}`);
      return true;
    } catch (error) {
      console.error('Error deleting auction image:', error);
      throw error;
    }
  },

  async uploadDocument(file, auctionId, documentType) {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('auction_id', auctionId);
      formData.append('document_type', documentType);

      const response = await axiosInstance.post(
        `${CAR_AUCTION_API_BASE}/documents/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error uploading document:', error);
      throw error;
    }
  }
};

export default carAuctionService;