import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import api from '../services/api';

export interface User {
  id: number;
  email: string;
  name: string;
  role: string;
}

export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  register: (email: string, password: string, name: string) => Promise<boolean>;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('auth_token');
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load user from token on mount
  useEffect(() => {
    if (token) {
      const storedUser = localStorage.getItem('auth_user');
      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch (e) {
          console.error('Failed to parse stored user:', e);
        }
      }
    }
  }, []);

  const login = useCallback(async (email: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.login(email, password);

      if (response.success && response.data?.token) {
        const userData = response.data.user || { id: 1, email, name: email.split('@')[0], role: 'user' };
        
        setToken(response.data.token);
        setUser(userData);
        
        localStorage.setItem('auth_token', response.data.token);
        localStorage.setItem('auth_user', JSON.stringify(userData));
        
        return true;
      } else {
        setError(response.error || 'Login failed');
        return false;
      }
    } catch (err: any) {
      const errorMsg = err.message || 'An error occurred during login';
      setError(errorMsg);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const register = useCallback(async (email: string, password: string, name: string): Promise<boolean> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await api.register({
        email,
        password,
        name,
      });

      if (response.success) {
        // Automatically log in after registration
        return login(email, password);
      } else {
        setError(response.error || 'Registration failed');
        return false;
      }
    } catch (err: any) {
      const errorMsg = err.message || 'An error occurred during registration';
      setError(errorMsg);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, [login]);

  const logout = useCallback(() => {
    setUser(null);
    setToken(null);
    setError(null);
    
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!token && !!user,
    isLoading,
    error,
    login,
    logout,
    register,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
