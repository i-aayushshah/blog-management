'use client';

import React, { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/authStore';

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { checkAuth, isAuthenticated, isLoading } = useAuthStore();
  const [authInitialized, setAuthInitialized] = useState(false);

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        console.log('🔐 Initializing authentication...');
        await checkAuth();
        console.log('✅ Authentication initialized');
      } catch (error) {
        console.error('❌ Authentication initialization failed:', error);
      } finally {
        setAuthInitialized(true);
      }
    };

    initializeAuth();
  }, [checkAuth]);

  // Show loading state while checking authentication
  if (!authInitialized || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initializing...</p>
          <p className="text-sm text-gray-500 mt-2">isAuthenticated: {String(isAuthenticated)}</p>
          <p className="text-sm text-gray-500">isLoading: {String(isLoading)}</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
};

export default AuthProvider;
