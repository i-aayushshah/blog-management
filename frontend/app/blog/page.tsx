import React from 'react';
import Navigation from '@/components/layout/Navigation';
import { BookOpen } from 'lucide-react';

export const metadata = {
  title: 'Blog - Blog Management',
  description: 'Explore our blog posts',
};

const BlogPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Our Blog
          </h1>
          <p className="text-xl text-gray-600">
            Discover interesting articles and insights
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            Blog Coming Soon
          </h2>
          <p className="text-gray-600 mb-6">
            We&apos;re working on connecting to the backend API to display blog posts here.
          </p>
          <div className="text-sm text-gray-500">
            Backend API: {process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BlogPage;
