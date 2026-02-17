import { createContext, useContext, useState } from "react";
import { creatorService } from "@/services/creatorService";
import { authService } from "@/services/authService";

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

  
  // Helper function to fetch and enhance user data
  const fetchEnhancedUserData = async (user) => {
    const { data: creatorData } = await creatorService.getCreatorBySlug(
      user.slug,
    );

    return {
      ...user,
      profileImage: creatorData.profileImage || user.profileImage,
      coverImage: creatorData.coverImage || user.coverImage,
    };
  };

  const login = async (email, password) => {
    try {
      const response = await authService.loginUser(email, password);

      const { accessToken, refreshToken } = response.data;
      saveTokens(accessToken, refreshToken);

      // Always fetch fresh profile data after login
      const { data: profileResponse } = await authService.getProfile();

      if (profileResponse.status === "success") {
        const profileData = profileResponse.data;

        // Fetch additional creator data with image status (for onboarding purposes)
        const enhancedUserData = await fetchEnhancedUserData(profileData);

        saveUser(enhancedUserData);

        return {
          success: true,
          user: enhancedUserData,
        };
      }

      throw new Error("No user found");
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || "Login failed",
      };
    }
  };

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

  const logout = async () => {
    await authService.logoutUser();
    setUser(null);
    setToken(null);
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
  };

  // Main update function
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
        };

        // If images were uploaded, fetch fresh data
        if (formData.get("profile_image") || formData.get("cover_image")) {
          updatedUserData = await fetchEnhancedUserData(updatedUserData);
        }

        // Save to localStorage
        saveUser(updatedUserData);

        return {
          success: true,
          user: updatedUserData,
          data: response.data,
        };
      }

      return { success: false, error: response.error };
      return { success: false, error: response.error };
    } catch (error) {
      console.log(error);
      return {
        success: false,
        error: error.response?.data?.message || "Profile Update failed",
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
