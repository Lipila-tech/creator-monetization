import api from "./api";

export const authService = {
  /**
   * Authenticates a user and retrieves JWT tokens.
   * @param {string} email The user’s registered email address.
   * @param {string} password The user’s account password.
   *
   * @returns {Promise<{
   *   success: boolean,
   *   data?: {
   *     accessToken: string,
   *     refreshToken: string
   *   },
   *   error?: string
   * }>} Returns JWT tokens on success or an error message on failure.
   */
  loginUser: async (email, password) => {
    try {
      const response = await api.post("/auth/token/", {
        email,
        password,
      });

      return { success: true, data: response.data };
    } catch (error) {
      return {
        success: false,
        error:
          error.response?.data?.message ||
          "Login failed. Please check your connection.",
      };
    }
  },

  /**
   * Registers a new user account.
   * @param {{
   *   username: string,
   *   email: string,
   *   password: string,
   *   password2: string
   * }} userData The registration payload for the new user.
   *
   * @returns {Promise<{
   *   success: boolean,
   *   data?: {
   *     accessToken: string,
   *     refreshToken: string,
   *     user: any
   *   },
   *   error?: string
   * }>} Returns authentication tokens and user info on success.
   */
  registerUser: async (userData) => {
    try {
      const response = await api.post("/auth/register/", userData);

      return { success: true, data: response.data };
    } catch (error) {
      console.error("Register API Error:", error.response);
      return {
        success: false,
        error:
          error.response?.data?.message ||
          "Registration failed. Please try again.",
      };
    }
  },

  /**
   * Logs out the currently authenticated user.
   * 
   * @returns {Promise<{
   *   success: boolean,
   *   data?: any,
   *   error?: string
   * }>} Returns a success flag when logout completes.
   */
  logoutUser: async () => {
    try {
      const response = await api.post("/auth/logout/");

      return { success: true, data: response.data };
    } catch (error) {
      console.error("Logout API Error:", error.response);
      return {
        success: false,
        error:
          error.response?.data?.message ||
          "Logout failed. Please try again.",
      };
    }
  },

  /**
   * Retrieves the authenticated user’s profile.
   * 
   * @returns {Promise<{
   *   success: boolean,
   *   data?: any,
   *   error?: string
   * }>} Returns the current user profile if authenticated.
   */
  getProfile: async () => {
    try {
      const response = await api.get("/auth/profile/");

      return { success: true, data: response.data };
    } catch (error) {
      console.error("Profile API Error:", error.response);
      return {
        success: false,
        error:
          error.response?.data?.message ||
          "Failed to fetch user profile.",
      };
    }
  },
};
