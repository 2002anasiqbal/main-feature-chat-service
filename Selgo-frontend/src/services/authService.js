import axios from 'axios';

const AUTH_API_URL = 'http://localhost:8001/api/v1/auth';
const BOAT_API_URL = 'http://localhost:8000/api/v1';

// Create axios instance for auth
const authClient = axios.create({
  baseURL: AUTH_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Create axios instance for other services
const apiClient = axios.create({
  baseURL: BOAT_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for token refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        if (refreshToken) {
          const response = await authService.refreshToken(refreshToken);
          localStorage.setItem('accessToken', response.access_token);
          originalRequest.headers.Authorization = `Bearer ${response.access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        authService.logout();
        window.location.href = '/routes/auth/signin';
      }
    }
    
    return Promise.reject(error);
  }
);

const authService = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await authClient.post('/register', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await authClient.post('/login', credentials);
      const { access_token, refresh_token, user } = response.data;
      
      // Store tokens
      localStorage.setItem('accessToken', access_token);
      localStorage.setItem('refreshToken', refresh_token);
      localStorage.setItem('user', JSON.stringify(user));
      
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Refresh token
  refreshToken: async (refreshToken) => {
    try {
      const response = await authClient.post('/refresh', {
        refresh_token: refreshToken
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        await authClient.post('/logout', {
          refresh_token: refreshToken
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear local storage
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
    }
  },

  // Get current user
  getCurrentUser: async () => {
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) return null;
      
      const response = await authClient.get('/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Change password
  changePassword: async (passwordData) => {
    try {
      const token = localStorage.getItem('accessToken');
      const response = await authClient.post('/change-password', passwordData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Check if user is authenticated
  isAuthenticated: () => {
    const token = localStorage.getItem('accessToken');
    const user = localStorage.getItem('user');
    return !!(token && user);
  },

  // Get stored user data
  getStoredUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
};

export default authService;
export { apiClient }; // Export for use in other services