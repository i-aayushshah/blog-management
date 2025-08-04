'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import PostForm from '@/components/blog/PostForm';

const CreatePostPage: React.FC = () => {
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useAuthStore();
  const [authChecked, setAuthChecked] = useState(false);

  // Check authentication status
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Wait a bit for auth to initialize
        await new Promise(resolve => setTimeout(resolve, 1000));
        setAuthChecked(true);
      } catch (error) {
        console.error('Auth check error:', error);
        setAuthChecked(true);
      }
    };

    checkAuth();
  }, []);

  // Redirect if not authenticated
  useEffect(() => {
    if (authChecked && !isAuthenticated) {
      router.push('/login?redirect=/create-post');
    }
  }, [isAuthenticated, authChecked, router]);

  // Show loading while checking auth
  if (!authChecked || isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Checking authentication...</p>
          <p className="text-sm text-gray-500 mt-2">isAuthenticated: {String(isAuthenticated)}</p>
          <p className="text-sm text-gray-500">isLoading: {String(isLoading)}</p>
        </div>
      </div>
    );
  }

  // Show error if not authenticated
  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-600 mb-4">
            <svg className="w-12 h-12 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Authentication Required</h2>
          <p className="text-gray-600 mb-4">You need to be logged in to create a post.</p>
          <button
            onClick={() => router.push('/login?redirect=/create-post')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PostForm mode="create" />
      </div>
    </div>
  );
};

export default CreatePostPage;
