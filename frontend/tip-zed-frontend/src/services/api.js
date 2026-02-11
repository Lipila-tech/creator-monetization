import axios from "axios";
import rateLimit from "axios-rate-limit";

// Setup Constants (Fixed for Vite)
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";
const TIMEOUT = Number(import.meta.env.VITE_API_TIMEOUT) || 15000;
const API_KEY = import.meta.env.VITE_API_CLIENT_KEY || "";

// Create Axios Instance
const api = rateLimit(
  axios.create({
    baseURL: BASE_URL,
    timeout: TIMEOUT,
    headers: {
      "X-API-KEY": API_KEY,
      "Content-Type": "application/json",
    },
  }),
  {
    maxRequests: 5,
    perMilliseconds: 1000,
  },
);

const refreshApi = axios.create({
  baseURL: BASE_URL,
  timeout: TIMEOUT,
  headers: {
    "Content-Type": "application/json",
    "X-API-KEY": API_KEY,
  },
});

let isRefreshing = false;
let refreshQueue = [];

const processQueue = (token) => {
  refreshQueue.forEach((cb) => cb(token));
  refreshQueue = [];
};

// Request Interceptor (Attach Token)
api.interceptors.request.use(
  (config) => {
    const publicRoutes = [
      "/auth/login/",
      "/auth/register/",
      "/creators/all/",
      "/creator-profile/",
      "/creator-catalog/",
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
      originalRequest._retry = true;

      if (isRefreshing) {
        return new Promise((resolve) => {
          refreshQueue.push((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            resolve(api(originalRequest));
          });
        });
      }

      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem("refreshToken");

        const { data } = await refreshApi.post("/auth/token/refresh/", {
          refresh: refreshToken,
        });

        const newToken = data.accessToken;
        localStorage.setItem("accessToken", newToken);

        processQueue(newToken);

        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (err) {
        localStorage.clear();
        window.location.href = "/login";
        return Promise.reject(err);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

export default api;
