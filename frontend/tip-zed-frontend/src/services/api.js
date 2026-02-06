import axios from "axios";

// Setup Constants (Fixed for Vite)
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
const TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 15000;
const API_KEY = import.meta.env.VITE_API_CLIENT_KEY || "";

// Create Axios Instance
const api = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT,
  headers: {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json",
  },
});

// Request Interceptor (Attach Token)
api.interceptors.request.use(
  (config) => {
    const publicRoutes = [
      "/auth/login/",
      "/auth/register/",
      "/creators/all/",
      "/creator-catalog/",
      "/creator-profile/",
    ];

    const isPublic = publicRoutes.some((route) => config.url.includes(route));

    if (!isPublic) {
      const token = localStorage.getItem("accessToken");

      if (token) config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response Interceptor (Handle 401 & Refresh Token)
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Check if error is 401 (Unauthorized) and we haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Mark as retried to prevent infinite loops

      try {
        const refreshToken = localStorage.getItem("refreshToken");

        if (!refreshToken) {
          throw new Error("No refresh token available");
        }

        // Call backend to get a new access token
        const response = await axios.post(`${BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });

        const newAccessToken = response.data.access;

        // Save new token to storage
        localStorage.setItem("accessToken", newAccessToken);

        // Update the header for the failed request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;

        // Retry the original request with the new token
        return api(originalRequest);
      } catch (refreshError) {
        // If refresh fails (token expired), force logout
        localStorage.removeItem("accessToken");
        window.location.href = "/login"; // Redirect to login

        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  },
);

export default api;
