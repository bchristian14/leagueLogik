/**
 * Admin Dashboard placeholder component
 */

import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';

export const AdminDashboard: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="h-8 w-8 bg-green-600 rounded-full flex items-center justify-center mr-3">
                <svg
                  className="h-4 w-4 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <h1 className="text-xl font-semibold text-gray-900">LeagueLogik Admin</h1>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-700">
                Welcome, {user?.first_name} {user?.last_name}
              </div>
              <Button variant="outline" onClick={logout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Welcome Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Admin Dashboard
            </h2>
            <p className="text-gray-600">
              Welcome to the LeagueLogik administration panel. Use the navigation below to manage your golf league.
            </p>
          </div>

          {/* Dashboard Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* User Info Card */}
            <Card>
              <CardHeader>
                <CardTitle>Your Account</CardTitle>
                <CardDescription>Account information and settings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="text-sm">
                  <span className="font-medium">Email:</span> {user?.email}
                </div>
                <div className="text-sm">
                  <span className="font-medium">Member Type:</span> {user?.member_type}
                </div>
                <div className="text-sm">
                  <span className="font-medium">Status:</span> {user?.member_status}
                </div>
                <div className="text-sm">
                  <span className="font-medium">Admin Role:</span> {user?.admin_roles || 'Standard Admin'}
                </div>
              </CardContent>
            </Card>

            {/* Member Management */}
            <Card>
              <CardHeader>
                <CardTitle>Member Management</CardTitle>
                <CardDescription>Add, edit, and manage league members</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" disabled>
                  Manage Members
                  <span className="ml-2 text-xs">(Coming Soon)</span>
                </Button>
              </CardContent>
            </Card>

            {/* Financial Management */}
            <Card>
              <CardHeader>
                <CardTitle>Financial Management</CardTitle>
                <CardDescription>Handle transactions and member balances</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" disabled>
                  Financial Tools
                  <span className="ml-2 text-xs">(Coming Soon)</span>
                </Button>
              </CardContent>
            </Card>

            {/* Tournament Management */}
            <Card>
              <CardHeader>
                <CardTitle>Tournament Management</CardTitle>
                <CardDescription>Schedule rounds and manage tournaments</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" disabled>
                  Tournament Tools
                  <span className="ml-2 text-xs">(Coming Soon)</span>
                </Button>
              </CardContent>
            </Card>

            {/* Season Management */}
            <Card>
              <CardHeader>
                <CardTitle>Season Management</CardTitle>
                <CardDescription>Configure seasons and settings</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" disabled>
                  Season Settings
                  <span className="ml-2 text-xs">(Coming Soon)</span>
                </Button>
              </CardContent>
            </Card>

            {/* Reports */}
            <Card>
              <CardHeader>
                <CardTitle>Reports & Analytics</CardTitle>
                <CardDescription>View league statistics and reports</CardDescription>
              </CardHeader>
              <CardContent>
                <Button className="w-full" disabled>
                  View Reports
                  <span className="ml-2 text-xs">(Coming Soon)</span>
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Development Status */}
          {import.meta.env.DEV && (
            <Card className="mt-8 bg-blue-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-blue-800">Development Status</CardTitle>
                <CardDescription className="text-blue-600">
                  Task T131: Login Page Implementation - COMPLETE
                </CardDescription>
              </CardHeader>
              <CardContent className="text-blue-700">
                <p className="text-sm">
                  Authentication system is now functional. Next phase will implement member management features.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;