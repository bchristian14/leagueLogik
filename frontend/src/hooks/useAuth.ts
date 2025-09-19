/**
 * Authentication hook for LeagueLogik Golf League Management System
 */

import { useState, useEffect, useCallback } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { AxiosError } from 'axios';
import apiClient, { mapApiError } from '../lib/api';
import { tokenStorage } from '../lib/auth';
import type {
  LoginRequest,
  LoginResponse,
  User,
  AuthState,
  AuthContextType
} from '../types/auth';

/**
 * Authentication API functions
 */
const authApi = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/login', credentials);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  logout: async (): Promise<void> => {
    await apiClient.post('/auth/logout');
  },

  refreshToken: async (refreshToken: string): Promise<LoginResponse> => {
    const response = await apiClient.post('/auth/refresh', {
      refresh_token: refreshToken,
    });
    return response.data;
  },
};

/**
 * Authentication hook
 */
export const useAuth = (): AuthContextType => {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Query to get current user (only runs if token exists)
  const { data: user, isLoading: userLoading, error: userError } = useQuery({
    queryKey: ['currentUser'],
    queryFn: authApi.getCurrentUser,
    enabled: !!tokenStorage.getAccessToken() && !tokenStorage.isTokenExpired(),
    retry: (failureCount, error) => {
      // Don't retry on 401 errors
      if (error instanceof AxiosError && error.response?.status === 401) {
        return false;
      }
      return failureCount < 2;
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Login mutation
  const loginMutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (data: LoginResponse) => {
      // Store tokens
      tokenStorage.set({
        access_token: data.access_token,
        refresh_token: data.refresh_token,
        expires_in: data.expires_in,
      });

      // Clear error state
      setAuthState(prev => ({ ...prev, error: null }));

      // Refetch user data
      queryClient.invalidateQueries({ queryKey: ['currentUser'] });
    },
    onError: (error: AxiosError) => {
      const errorMessage = mapApiError(error);
      setAuthState(prev => ({ ...prev, error: errorMessage }));
    },
  });

  // Logout mutation
  const logoutMutation = useMutation({
    mutationFn: authApi.logout,
    onSettled: () => {
      // Always clear local state, even if API call fails
      tokenStorage.remove();
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
      queryClient.clear();

      // Redirect to login page immediately after logout
      navigate('/login', { replace: true });
    },
  });

  // Update auth state when user data changes
  useEffect(() => {
    const hasToken = !!tokenStorage.getAccessToken() && !tokenStorage.isTokenExpired();
    const isAuthenticated = hasToken && !!user && !userError;

    setAuthState(prev => ({
      ...prev,
      user: user || null,
      isAuthenticated,
      isLoading: userLoading && hasToken,
      error: userError ? mapApiError(userError as AxiosError) : prev.error,
    }));
  }, [user, userLoading, userError]);

  // Initialize auth state on mount
  useEffect(() => {
    const hasToken = !!tokenStorage.getAccessToken() && !tokenStorage.isTokenExpired();

    if (!hasToken) {
      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  }, []);

  // Login function
  const login = useCallback(async (email: string, password: string): Promise<void> => {
    setAuthState(prev => ({ ...prev, error: null }));
    await loginMutation.mutateAsync({ email, password });
  }, [loginMutation]);

  // Logout function
  const logout = useCallback((): void => {
    logoutMutation.mutate();
  }, [logoutMutation]);

  // Clear error function
  const clearError = useCallback((): void => {
    setAuthState(prev => ({ ...prev, error: null }));
  }, []);

  return {
    user: authState.user,
    isAuthenticated: authState.isAuthenticated,
    isLoading: authState.isLoading || loginMutation.isPending || logoutMutation.isPending,
    error: authState.error,
    login,
    logout,
    clearError,
  };
};

export default useAuth;