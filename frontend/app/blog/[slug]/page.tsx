'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { useBlogStore } from '@/store/blogStore';
import PostDetail from '@/components/blog/PostDetail';
import PostList from '@/components/blog/PostList';
import { Post } from '@/types';

const PostPage: React.FC = () => {
  const params = useParams();
  const slug = params.slug as string;
  const [post, setPost] = useState<Post | null>(null);
  const [relatedPosts, setRelatedPosts] = useState<Post[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const { fetchPost, posts } = useBlogStore();

  useEffect(() => {
    const loadPost = async () => {
      if (!slug) return;

      setIsLoading(true);
      setError(null);

      try {
        // Find post by slug in the store first
        const existingPost = posts.find(p => p.slug === slug);

        if (existingPost) {
          setPost(existingPost);
          // Get related posts (same category or tags)
          const related = posts
            .filter(p => p.id !== existingPost.id && p.status === 'published')
            .slice(0, 3);
          setRelatedPosts(related);
        } else {
          // If not in store, try to fetch by slug
          // This would require a backend endpoint to fetch by slug
          // For now, we'll show an error
          setError('Post not found');
        }
      } catch (err) {
        setError('Failed to load post');
        console.error('Error loading post:', err);
      } finally {
        setIsLoading(false);
      }
    };

    loadPost();
  }, [slug, posts]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
            <div className="animate-pulse space-y-6">
              <div className="h-8 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
              <div className="h-4 bg-gray-200 rounded w-1/3"></div>
              <div className="space-y-3">
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-full"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Post Not Found
            </h1>
            <p className="text-gray-600 mb-6">
              The post you&apos;re looking for doesn&apos;t exist or has been removed.
            </p>
            <a
              href="/blog"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Back to Blog
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Don't show draft posts to non-authors
  if (post.status === 'draft') {
    // This would need proper authorization check
    // For now, we'll show a generic message
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Post Not Available
            </h1>
            <p className="text-gray-600 mb-6">
              This post is not available for public viewing.
            </p>
            <a
              href="/blog"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Back to Blog
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Main Post */}
        <PostDetail post={post} />

        {/* Related Posts */}
        {relatedPosts.length > 0 && (
          <div className="mt-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">
              Related Posts
            </h2>
            <PostList
              posts={relatedPosts}
              showPagination={false}
              variant="compact"
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default PostPage;
