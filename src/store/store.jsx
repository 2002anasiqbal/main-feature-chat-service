import { create } from "zustand";
import { mockFetchUser, mockLogout } from "@/utils/mockAuth";

const isClient = typeof window !== "undefined"; // Ensure it's running on the client

const useAuthStore = create((set) => ({
  // Store the entire user object
  user: null,

  // Store individual fields for convenience
  userId: null,
  userName: null,
  userEmail: null,

  // Check if there's a token in cookies (client-only)
  isAuthenticated: () => {
    if (!isClient) return false;
    const Cookies = require("js-cookie");
    return !!Cookies.get("auth_token");
  },

  // Set the user object and also individual properties
  setUser: (user) =>
    set(() => ({
      user,
      userId: user?.id || null,
      userName: user?.name || null,
      userEmail: user?.email || null,
    })),

  // Fetch user from mock API, then update store
  fetchUser: async () => {
    const response = await mockFetchUser();
    const fetchedUser = response.user;

    set(() => ({
      user: fetchedUser,
      userId: fetchedUser?.id || null,
      userName: fetchedUser?.name || null,
      userEmail: fetchedUser?.email || null,
    }));
  },

  // Logout: clear token + reset store fields
  logout: async () => {
    if (isClient) {
      const Cookies = require("js-cookie");
      Cookies.remove("auth_token");
    }
    await mockLogout();

    set(() => ({
      user: null,
      userId: null,
      userName: null,
      userEmail: null,
    }));
  },
}));

export default useAuthStore;