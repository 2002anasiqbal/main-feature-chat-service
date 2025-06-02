// import { create } from "zustand";
// import { mockFetchUser, mockLogout } from "@/utils/mockAuth";

// const isClient = typeof window !== "undefined"; // Ensure it's running on the client

// const useAuthStore = create((set) => ({
//   // Store the entire user object
//   user: null,

//   // Store individual fields for convenience
//   userId: null,
//   userName: null,
//   userEmail: null,

//   // Check if there's a token in cookies (client-only)
//   isAuthenticated: () => {
//     if (!isClient) return false;
//     const Cookies = require("js-cookie");
//     return !!Cookies.get("auth_token");
//   },

//   // Set the user object and also individual properties
//   setUser: (user) =>
//     set(() => ({
//       user,
//       userId: user?.id || null,
//       userName: user?.name || null,
//       userEmail: user?.email || null,
//     })),

//   // Fetch user from mock API, then update store
//   fetchUser: async () => {
//     const response = await mockFetchUser();
//     const fetchedUser = response.user;

//     set(() => ({
//       user: fetchedUser,
//       userId: fetchedUser?.id || null,
//       userName: fetchedUser?.name || null,
//       userEmail: fetchedUser?.email || null,
//     }));
//   },

//   // Logout: clear token + reset store fields
//   logout: async () => {
//     if (isClient) {
//       const Cookies = require("js-cookie");
//       Cookies.remove("auth_token");
//     }
//     await mockLogout();

//     set(() => ({
//       user: null,
//       userId: null,
//       userName: null,
//       userEmail: null,
//     }));
//   },
// }));

// export default useAuthStore;

import { create } from "zustand";
import authService from "@/services/authService";

const isClient = typeof window !== "undefined";

const useAuthStore = create((set, get) => ({
  // Store the entire user object
  user: null,
  
  // Store individual fields for convenience
  userId: null,
  userName: null,
  userEmail: null,

  // Check if there's a token in localStorage (client-only)
  isAuthenticated: () => {
    if (!isClient) return false;
    return authService.isAuthenticated();
  },

  // Set the user object and also individual properties
  setUser: (user) =>
    set(() => ({
      user,
      userId: user?.id || null,
      userName: user?.username || null,
      userEmail: user?.email || null,
    })),

  // Fetch user from real auth service
  fetchUser: async () => {
    try {
      if (!authService.isAuthenticated()) {
        set(() => ({
          user: null,
          userId: null,
          userName: null,
          userEmail: null,
        }));
        return;
      }

      const user = await authService.getCurrentUser();
      set(() => ({
        user: user,
        userId: user?.id || null,
        userName: user?.username || null,
        userEmail: user?.email || null,
      }));
    } catch (error) {
      console.error("Failed to fetch user:", error);
      // Clear invalid tokens
      await authService.logout();
      set(() => ({
        user: null,
        userId: null,
        userName: null,
        userEmail: null,
      }));
    }
  },

  // Logout: clear tokens + reset store fields
  logout: async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      set(() => ({
        user: null,
        userId: null,
        userName: null,
        userEmail: null,
      }));
    }
  },
}));

export default useAuthStore;