'use client';

import React, { useEffect } from 'react';
import { ChevronLeft, ChevronRight, Loader2, FileText } from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import PostCard from './PostCard';
import { cn } from '@/lib/utils';

interface PostListProps {
  posts?: any[];
  isLoading?: boolean;
  showPagination?: boolean;
  variant?: 'default' | 'featured' | 'compact';
  className?: string;
  emptyMessage?: string;
}

const PostList: React.FC<PostListProps> = ({
  posts: propPosts,
  isLoading: propIsLoading,
  showPagination = true,
  variant = 'default',
  className,
  emptyMessage = 'No posts found',
}) => {
  const {
    posts: storePosts,
    isLoading: storeIsLoading,
    pagination,
    fetchPosts,
    filters,
  } = useBlogStore();

  const posts = propPosts || storePosts;
  const isLoading = propIsLoading !== undefined ? propIsLoading : storeIsLoading;

  // Fetch posts when filters change
  useEffect(() => {
    if (!propPosts) {
      const params: Record<string, string | number> = {
        page: pagination.currentPage,
      };

      if (filters.search) {
        params.search = filters.search;
      }
      if (filters.category) {
        params.category = filters.category;
      }
      if (filters.tag) {
        params.tag = filters.tag;
      }
      if (filters.status !== 'all') {
        params.status = filters.status;
      }

      fetchPosts(params);
    }
  }, [filters, pagination.currentPage, fetchPosts, propPosts]);

  const handlePageChange = (page: number) => {
    if (!propPosts) {
      const params: Record<string, string | number> = {
        page,
      };

      if (filters.search) {
        params.search = filters.search;
      }
      if (filters.category) {
        params.category = filters.category;
      }
      if (filters.tag) {
        params.tag = filters.tag;
      }
      if (filters.status !== 'all') {
        params.status = filters.status;
      }

      fetchPosts(params);
    }
  };

  const totalPages = Math.ceil(pagination.count / 10); // Assuming 10 posts per page

  if (isLoading) {
    return (
      <div className={cn('space-y-6', className)}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, index) => (
            <div
              key={index}
              className="bg-white rounded-lg shadow-sm border border-gray-100 overflow-hidden animate-pulse"
            >
              <div className="h-48 bg-gray-200" />
              <div className="p-4 space-y-3">
                <div className="h-4 bg-gray-200 rounded w-3/4" />
                <div className="h-6 bg-gray-200 rounded w-full" />
                <div className="h-4 bg-gray-200 rounded w-full" />
                <div className="h-4 bg-gray-200 rounded w-2/3" />
                <div className="flex items-center gap-4 pt-2">
                  <div className="h-3 bg-gray-200 rounded w-20" />
                  <div className="h-3 bg-gray-200 rounded w-16" />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!posts || posts.length === 0) {
    return (
      <div className={cn('text-center py-12', className)}>
        <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          {emptyMessage}
        </h3>
        <p className="text-gray-500">
          {filters.search || filters.category || filters.tag
            ? 'Try adjusting your search or filters'
            : 'Check back later for new content'}
        </p>
      </div>
    );
  }

  return (
    <div className={cn('space-y-6', className)}>
      {/* Posts Grid */}
      <div className={cn(
        'grid gap-6',
        variant === 'featured' && 'grid-cols-1 lg:grid-cols-2',
        variant === 'compact' && 'grid-cols-1',
        variant === 'default' && 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
      )}>
        {posts && posts.map((post) => (
          <PostCard
            key={post.id}
            post={post}
            variant={variant}
          />
        ))}
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="flex items-center justify-between border-t border-gray-200 pt-6">
          <div className="flex items-center text-sm text-gray-700">
            <span>
              Showing {((pagination.currentPage - 1) * 10) + 1} to{' '}
              {Math.min(pagination.currentPage * 10, pagination.count)} of{' '}
              {pagination.count} results
            </span>
          </div>

          <div className="flex items-center gap-2">
            {/* Previous Page */}
            <button
              onClick={() => handlePageChange(pagination.currentPage - 1)}
              disabled={!pagination.previous}
              className={cn(
                'flex items-center gap-1 px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                pagination.previous
                  ? 'text-gray-700 hover:bg-gray-100'
                  : 'text-gray-400 cursor-not-allowed'
              )}
            >
              <ChevronLeft className="w-4 h-4" />
              Previous
            </button>

            {/* Page Numbers */}
            <div className="flex items-center gap-1">
              {[...Array(totalPages)].map((_, index) => {
                const page = index + 1;
                const isCurrent = page === pagination.currentPage;
                const isNearCurrent = Math.abs(page - pagination.currentPage) <= 1;
                const isFirst = page === 1;
                const isLast = page === totalPages;

                if (isCurrent || isNearCurrent || isFirst || isLast) {
                  return (
                    <button
                      key={page}
                      onClick={() => handlePageChange(page)}
                      className={cn(
                        'px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                        isCurrent
                          ? 'bg-blue-600 text-white'
                          : 'text-gray-700 hover:bg-gray-100'
                      )}
                    >
                      {page}
                    </button>
                  );
                } else if (
                  (page === 2 && pagination.currentPage > 3) ||
                  (page === totalPages - 1 && pagination.currentPage < totalPages - 2)
                ) {
                  return (
                    <span key={page} className="px-2 text-gray-400">
                      ...
                    </span>
                  );
                }
                return null;
              })}
            </div>

            {/* Next Page */}
            <button
              onClick={() => handlePageChange(pagination.currentPage + 1)}
              disabled={!pagination.next}
              className={cn(
                'flex items-center gap-1 px-3 py-2 text-sm font-medium rounded-lg transition-colors',
                pagination.next
                  ? 'text-gray-700 hover:bg-gray-100'
                  : 'text-gray-400 cursor-not-allowed'
              )}
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default PostList;
