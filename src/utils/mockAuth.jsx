// /src/utils/mockAuth.js
import Cookies from "js-cookie";
import { mockUsers } from "./mockUsers";

// Simulated login
export const mockLogin = ({ email, password }) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const user = mockUsers.find(
        (u) => u.email === email && u.password === password
      );
      if (user) {
        // Set a cookie for the JWT
        Cookies.set("auth_token", user.token, { expires: 1 });
        resolve({ message: "Login successful", user, token: user.token });
      } else {
        reject(new Error("Invalid email or password"));
      }
    }, 500);
  });
};

// Simulated signup
export const mockSignup = ({ email, username, password }) => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Check if email already used
      const existing = mockUsers.some((u) => u.email === email);
      if (existing) {
        return reject(new Error("Email already in use"));
      }

      // Build a new user object
      const newUser = {
        id: mockUsers.length + 1,
        name: username,
        email,
        password,
        token: "mock_jwt_token_" + username,
        chats: [], // brand new user has no chats yet
      };

      mockUsers.push(newUser);

      Cookies.set("auth_token", newUser.token, { expires: 1 });
      resolve({
        message: "Signup successful",
        user: newUser,
        token: newUser.token,
      });
    }, 500);
  });
};

// Simulated logout
export const mockLogout = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      Cookies.remove("auth_token");
      resolve({ message: "Logout successful" });
    }, 300);
  });
};

// Fetch user from cookies
export const mockFetchUser = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const token = Cookies.get("auth_token");
      const user = mockUsers.find((u) => u.token === token);
      resolve({ user: user || null });
    }, 500);
  });
};