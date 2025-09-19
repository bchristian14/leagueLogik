/**
 * Authentication types for LeagueLogik Golf League Management System
 */

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface User {
  member_id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number?: string;
  date_of_birth?: string;
  member_status: 'active' | 'inactive';
  member_type: 'candidate' | 'full' | 'lifetime';
  admin_roles?: string;
  GHIN_id?: string;
  member_balance: number;
  signup_date: string;
  AGA_membership_expiry?: string;
  created_at: string;
  updated_at: string;
  is_admin: boolean;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export interface TokenStorage {
  access_token: string;
  refresh_token: string;
  expires_at: number;
}

export interface ApiError {
  detail: string;
  type?: string;
}

export interface ValidationError {
  detail: Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}

export interface LoginFormData {
  email: string;
  password: string;
}

export interface AuthErrorType {
  invalid_credentials: string;
  account_locked: string;
  account_inactive: string;
  network_error: string;
  validation_error: string;
  unknown_error: string;
}