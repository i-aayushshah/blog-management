'use client';

import React, { useEffect } from 'react';
import { Plus, Filter, X } from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import { useAuthStore } from '@/store/authStore';
import PostList from '@/components/blog/PostList';
import SearchBar from '@/components/blog/SearchBar';
import CategoryFilter from '@/components/blog/CategoryFilter';
import Button from '@/components/ui/Button';

const BlogPage: React.FC = () => {
  const { user } = useAuthStore();
  const {
    filters,
    clearFilters,
    fetchPosts,
    fetchFeaturedPosts,
    setStatusFilter
  } = useBlogStore();

  // Fetch posts on mount
  useEffect(() => {
    fetchPosts();
    fetchFeaturedPosts();
  }, [fetchPosts, fetchFeaturedPosts]);

  const hasActiveFilters = filters.search || filters.category || filters.tag || filters.status !== 'all';

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Blog</h1>
              <p className="text-gray-600 mt-2">
                Discover stories, thinking, and expertise from writers on any topic.
              </p>
            </div>

            {user && (
              <Button
                onClick={() => window.location.href = '/create-post'}
                className="flex items-center gap-2"
              >
                <Plus className="w-4 h-4" />
                Create Post
              </Button>
            )}
          </div>
        </div>

        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
            {/* Search */}
            <div className="lg:col-span-2">
              <SearchBar placeholder="Search posts by title, content, or author..." />
            </div>

            {/* Category Filter */}
            <div>
              <CategoryFilter />
            </div>

            {/* Status Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={filters.status}
                onChange={(e) => setStatusFilter(e.target.value as 'all' | 'draft' | 'published')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              >
                <option value="all">All Posts</option>
                <option value="published">Published</option>
                <option value="draft">Drafts</option>
              </select>
            </div>
          </div>

          {/* Active Filters */}
          {hasActiveFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex items-center gap-2">
                <Filter className="w-4 h-4 text-gray-400" />
                <span className="text-sm text-gray-500">Active filters:</span>

                {filters.search && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                    Search: &quot;{filters.search}&quot;
                  </span>
                )}

                {filters.category && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-700 text-xs rounded-full">
                    Category: {filters.category}
                  </span>
                )}

                {filters.tag && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-full">
                    Tag: {filters.tag}
                  </span>
                )}

                {filters.status !== 'all' && (
                  <span className="inline-flex items-center gap-1 px-2 py-1 bg-orange-100 text-orange-700 text-xs rounded-full">
                    Status: {filters.status}
                  </span>
                )}

                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearFilters}
                  className="flex items-center gap-1 text-gray-500 hover:text-gray-700"
                >
                  <X className="w-3 h-3" />
                  Clear all
                </Button>
              </div>
            </div>
          )}
        </div>

        {/* Posts */}
        <PostList />
      </div>
    </div>
  );
};

export default BlogPage;
