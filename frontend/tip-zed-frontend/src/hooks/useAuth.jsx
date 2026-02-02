import { createContext, useContext, useState } from "react";
import authService from "../services/authService";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  // Lazy Initialization: Reads storage ONCE when app starts so there is no need for useEffect.

  const [token, setToken] = useState(() => {
    return localStorage.getItem("token") || null;
  });

  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem("user");
    try {
      return storedUser ? JSON.parse(storedUser) : null;
    } catch (error) {
      console.error("Failed to parse user data", error);
      return null;
    }
  });

  const login = async (email, password) => {
    try {
      const response = await authService.loginUser(email, password);

      const { access_token, user: userData } = response.data;

      // Save to State
      setToken(access_token);
      if (userData) setUser(userData); // if user is returned on login

      // Save to LocalStorage
      localStorage.setItem("token", access_token);
      if (userData) localStorage.setItem("user", JSON.stringify(userData));

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

      setToken(access_token);
      setUser(userData);

      localStorage.setItem("token", access_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.message || "Registration failed",
      };
    }
  };

  const logout = () => {
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
