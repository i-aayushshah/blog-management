import React from 'react';
import Navigation from '@/components/layout/Navigation';
import { Edit } from 'lucide-react';

export const metadata = {
  title: 'Edit Post - Blog Management',
  description: 'Edit your blog post',
};

const EditPostPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center mb-8">
            <Edit className="h-8 w-8 text-gray-600 mr-3" />
            <h1 className="text-3xl font-bold text-gray-900">Edit Post</h1>
          </div>

          <div className="text-center py-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">
              Post Editing Coming Soon
            </h2>
            <p className="text-gray-600">
              Post editing features will be implemented in the next phase.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditPostPage; 