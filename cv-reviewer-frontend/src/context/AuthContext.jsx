import { createContext, useState, useEffect, useCallback } from "react";
import { jwtDecode } from "jwt-decode";
import { authAPI } from "../api/auth";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Check if a stored token is still valid
  const validateToken = useCallback(async () => {
    const token = localStorage.getItem("cv_token");
    if (!token) {
      setLoading(false);
      return;
    }

    try {
      const decoded = jwtDecode(token);
      // Check expiry
      if (decoded.exp * 1000 < Date.now()) {
        throw new Error("Token expired");
      }
      // Fetch current user from backend
      const res = await authAPI.getMe();
      setUser(res.data);
    } catch {
      localStorage.removeItem("cv_token");
      localStorage.removeItem("cv_user");
      setUser(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    validateToken();
  }, [validateToken]);

  const loginUser = useCallback((tokenData) => {
    localStorage.setItem("cv_token", tokenData.access_token);
    localStorage.setItem("cv_user", JSON.stringify(tokenData.user));
    setUser(tokenData.user);
  }, []);

  const logoutUser = useCallback(() => {
    localStorage.removeItem("cv_token");
    localStorage.removeItem("cv_user");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, loginUser, logoutUser, isAuthenticated: !!user }}
    >
      {children}
    </AuthContext.Provider>
  );
}
