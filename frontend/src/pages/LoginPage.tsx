/**
 * Login page with responsive design and authentication integration
 */

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { LoginForm } from '../components/auth/LoginForm';
import { useAuth } from '../hooks/useAuth';
import type { LoginFormData } from '../types/auth';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login, isAuthenticated, isLoading, error, clearError, user } = useAuth();

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      // Redirect based on user role
      if (user.is_admin) {
        navigate('/admin/dashboard', { replace: true });
      } else {
        navigate('/member/dashboard', { replace: true });
      }
    }
  }, [isAuthenticated, user, navigate]);

  const handleLogin = async (data: LoginFormData): Promise<void> => {
    await login(data.email, data.password);
  };

  // Show loading state while checking authentication
  if (isLoading && !error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 to-blue-50 px-4 py-8">
      <div className="w-full max-w-md space-y-8">
        {/* Logo and Header */}
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-green-600 rounded-full flex items-center justify-center mb-4">
            <svg
              className="h-8 w-8 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">LeagueLogik</h1>
          <p className="mt-2 text-gray-600">Golf League Management System</p>
        </div>

        {/* Login Card */}
        <Card className="shadow-lg border-0">
          <CardHeader className="space-y-1 pb-6">
            <CardTitle className="text-2xl font-semibold text-center">
              Welcome Back
            </CardTitle>
            <CardDescription className="text-center">
              Sign in to access your golf league account
            </CardDescription>
          </CardHeader>

          <CardContent>
            <LoginForm
              onSubmit={handleLogin}
              isLoading={isLoading}
              error={error}
              onClearError={clearError}
            />
          </CardContent>
        </Card>

        {/* Footer Information */}
        <div className="text-center text-sm text-gray-500 space-y-2">
          <p>
            For technical support or account issues,{' '}
            <a
              href="mailto:support@leaguelogik.com"
              className="text-blue-600 hover:text-blue-500 underline"
            >
              contact support
            </a>
          </p>
          <p>
            New member?{' '}
            <span className="text-gray-700">
              Contact your league administrator for account setup.
            </span>
          </p>
        </div>

        {/* Development Notice (remove in production) */}
        {import.meta.env.DEV && (
          <Card className="bg-yellow-50 border-yellow-200">
            <CardContent className="pt-6">
              <div className="text-center text-sm text-yellow-800">
                <p className="font-medium">Development Mode</p>
                <p>Default admin credentials:</p>
                <p className="font-mono text-xs mt-1">
                  admin@leaguelogik.com / Test123!@#$%^&*()
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default LoginPage;