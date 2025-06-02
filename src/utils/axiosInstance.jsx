import axios from "axios";

const axiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "", // Set API base URL if needed
  withCredentials: true, // Allows sending cookies with requests
});

export default axiosInstance;
