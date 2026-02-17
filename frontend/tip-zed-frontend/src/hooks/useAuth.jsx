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

  const login = async (email, password) => {
    try {
      const response = await authService.loginUser(email, password);

      const { accessToken, refreshToken } = response.data;

      saveTokens(accessToken, refreshToken);

      // if user is not in local storage
      if (!getUser()) {
        const { data: responseData } = await authService.getProfile();

        if (responseData.status === "success") {
          saveUser(responseData.data);
          return { success: true, user: responseData.data };
        }
      } else {
        return { success: true, user: getUser() };
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

  const update = async (formData) => {
    try {
      const response = await creatorService.updateCreator(formData);

      if (response.success) {
        // Extract data from FormData
        const updatedUserData = {
          ...user,
          firstName: formData.get("firstName"),
          lastName: formData.get("lastName"),
          bio: formData.get("bio") || user.bio,
        };

        // Update profile image URL if returned in response
        if (response.data?.profileImage) {
          updatedUserData.profileImage = response.data.profileImage;
        }

        // Update cover image URL if returned in response
        if (response.data?.coverImage) {
          updatedUserData.coverImage = response.data.coverImage;
        }

        saveUser(updatedUserData);

        console.log(updatedUserData);

        return {
          success: true,
          user: updatedUserData,
          data: response.data, // Pass through any response data
        };
      }

      return { success: false, error: response.error };
    } catch (error) {
      console.log(error);
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
