import { createContext, useContext, useState } from "react";
import authService from "../services/authService";

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

  const saveToken = (token) => {
    setToken(token);
    localStorage.setItem("token", token);
  };

  const [token, setToken] = useState(() => {
    return localStorage.getItem("token") || null;
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

      const { access_token } = response.data;

      saveToken(access_token);

      // if user is not in local storage
      if (!getUser()) {
        const responseUser = await authService.getProfile();

        if (responseUser.data) saveUser(responseUser.data);
      }

      return { success: true };
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
      const { access_token, ...userData } = response.data;

      saveToken(access_token);
      saveUser(userData)

      return { success: true };
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
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext);
