import React, { createContext, useContext, useState, useEffect, useCallback } from "react";
import { User } from "../types/index.js";
import { api } from "../services/api.js";

interface AuthContextValue {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<User>;
  register: (data: { name: string; email: string; password: string; confirmPassword: string }) => Promise<User>;
  logout: () => void;
  refreshUser: () => Promise<void>;
  updateLocalUser: (updates: Partial<User>) => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(() => {
    const saved = localStorage.getItem("career_framework_user");
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem("career_framework_token");
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const refreshUser = useCallback(async () => {
    const storedToken = localStorage.getItem("career_framework_token");
    if (!storedToken) {
      setUser(null);
      setIsLoading(false);
      return;
    }
    try {
      const userData = await api.auth.getMe();
      setUser(userData);
      localStorage.setItem("career_framework_user", JSON.stringify(userData));
    } catch (err) {
      console.warn("Session refresh failed:", err);
      setUser(null);
      setToken(null);
      localStorage.removeItem("career_framework_token");
      localStorage.removeItem("career_framework_user");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const login = async (credentials: { email: string; password: string }) => {
    setIsLoading(true);
    try {
      const res = await api.auth.login(credentials);
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem("career_framework_token", res.token);
      localStorage.setItem("career_framework_user", JSON.stringify(res.user));
      return res.user;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: { name: string; email: string; password: string; confirmPassword: string }) => {
    setIsLoading(true);
    try {
      const res = await api.auth.register(data);
      setToken(res.token);
      setUser(res.user);
      localStorage.setItem("career_framework_token", res.token);
      localStorage.setItem("career_framework_user", JSON.stringify(res.user));
      return res.user;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("career_framework_token");
    localStorage.removeItem("career_framework_user");
  };

  const updateLocalUser = (updates: Partial<User>) => {
    if (!user) return;
    const updated = { ...user, ...updates };
    setUser(updated);
    localStorage.setItem("career_framework_user", JSON.stringify(updated));
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        register,
        logout,
        refreshUser,
        updateLocalUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
