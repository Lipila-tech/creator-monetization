import { createContext, useContext, useState } from "react";
import { creatorService } from "@/services/creatorService";
import { authService } from "@/services/authService";
import { walletService } from "../services/walletService";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Lazy Initialization: Reads storage ONCE when app starts so there is no need for useEffect.

  const getUser = () => {
    return JSON.parse(localStorage.getItem("user"));
  };

  const saveUser = (user) => {
    setUser(user);
    localStorage.setItem("user", JSON.stringify(user));
  };

  const saveTokens = (access, refresh) => {
    setToken(token);
    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
  };

  const [token, setToken] = useState(() => {
    return localStorage.getItem("accessToken") || null;
  });

  const [user, setUser] = useState(() => {
    const storedUser = getUser();
    try {
      return storedUser ?? null;
    } catch (error) {
      console.error("Failed to parse user data", error);
      return null;
    }
  });

  /**
   * Helper function to fetch and enhance user data
   * @param {*} user current minimal user data that requires enhancement
   * @returns fully complete user profile data
   */
  const fetchEnhancedUserData = async (user) => {
    const [{ data: creatorData }, walletData] = await Promise.all([
      creatorService.getCreatorBySlug(user.slug),
      walletService.getWalletData(),
    ]);

    return {
      ...user,
      bio: creatorData.bio,
      profileImage: creatorData.profileImage || user.profileImage,
      coverImage: creatorData.coverImage || user.coverImage,
      hasEarnings:
        walletData?.totalEarnings > 0 || walletData?.transactionCount,
    };
  };

  /**
   * Silently enhances user data in the background to prevent prolonged login
   * @param {*} user current minimal user data that requires enhancement
   */
  const enhanceUserInBackground = async (user) => {
    try {
      const enhancedUser = await fetchEnhancedUserData(user);

      const prev = getUser();

      if (!prev) throw new Error("User not found");

      // Merge minimal user data with fill profile data
      saveUser({
        ...prev, // minimal
        ...enhancedUser, // full profile
      });
    } catch (err) {
      // let login continue without enhancement (silent fail)
      console.warn("User enhancement failed:", err);
    }
  };

  /**
   * Call login endpoint and performs a global update of user state and auth state
   * @param {string} email user's email
   * @param {string} password user's password
   * @returns
   */
  const login = async (email, password) => {
    try {
      const { data } = await authService.loginUser(email, password);
      const { accessToken, refreshToken } = data;

      saveTokens(accessToken, refreshToken);

      const { data: profileResponse } = await authService.getProfile();

      if (profileResponse.status !== "success") {
        throw new Error("No user found");
      }

      const baseUser = profileResponse.data;

      // Instant UX so app can render now
      saveUser(baseUser);

      enhanceUserInBackground(baseUser);

      return {
        success: true,
        user: baseUser,
      };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || "Login failed",
      };
    }
  };

  /**
   * Calls the register endpoint and performs a global update of user state and auth state
   * @param {*} formData user data
   * @returns
   */
  const register = async (formData) => {
    try {
      const response = await authService.registerUser(formData);
      const { accessToken, refreshToken, ...userData } = response.data;

      saveTokens(accessToken, refreshToken);
      saveUser(userData.user);

      return { success: true, user: userData.user };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || "Registration failed",
      };
    }
  };

  /**
   * Calls logout endpoint and removes global user and auth state
   */
  const logout = async () => {
    await authService.logoutUser();
    setUser(null);
    setToken(null);
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
  };

  /**
   * Calls the update endpoint and updates the global user state
   * @param {*} formData
   * @returns
   */
  const update = async (formData) => {
    try {
      const response = await creatorService.updateCreator(formData);

      if (response.success) {
        const currentUser = getUser();

        // Build updated user data
        let updatedUserData = {
          ...currentUser,
          firstName: formData.get("first_name") || currentUser.firstName,
          lastName: formData.get("last_name") || currentUser.lastName,
          bio: formData.get("bio") || currentUser.bio,
          phoneNumber: formData.get("phone_number") || currentUser.phoneNumber,
          email: formData.get("email") || currentUser.email,
          categorySlugs:
            formData.get("category_slugs") || currentUser.categorySlugs,
        };

        // If images were uploaded, fetch fresh data
        if (formData.get("profile_image") || formData.get("cover_image")) {
          // required to fetch server side user image urls
          enhanceUserInBackground(updatedUserData);
        } else {
          // if no images a local update of user data can occur
          saveUser(updatedUserData);
        }

        return {
          success: true,
          user: updatedUserData,
          data: response.data,
        };
      }

      return { success: false, error: response.error };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || "Profile Update failed",
      };
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, token, login, register, logout, update }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
