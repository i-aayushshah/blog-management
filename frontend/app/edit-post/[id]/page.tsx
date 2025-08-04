'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';
import { useBlogStore } from '@/store/blogStore';
import PostForm from '@/components/blog/PostForm';
import { Post } from '@/types';

const EditPostPage: React.FC = () => {
  const params = useParams();
  const router = useRouter();
  const postId = parseInt(params.id as string);

  const { user, isAuthenticated } = useAuthStore();
  const { fetchPost, currentPost } = useBlogStore();

  const [post, setPost] = useState<Post | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefetching, setIsRefetching] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login?redirect=/edit-post/' + postId);
    }
  }, [isAuthenticated, router, postId]);

  // Fetch post data
  useEffect(() => {
    const loadPost = async () => {
      if (!postId || !isAuthenticated) return;

      setIsLoading(true);
      setError(null);

      try {
        console.log('🔍 Fetching post with ID:', postId);
        await fetchPost(postId);
      } catch (err) {
        console.error('Error loading post:', err);
        setError('Failed to load post. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };

    loadPost();
  }, [postId, isAuthenticated, fetchPost]);

  // Check if user is the author
  useEffect(() => {
    if (currentPost && user) {
      console.log('🔍 Checking post author:', {
        postId: postId,
        currentPostId: currentPost.id,
        postAuthor: currentPost.author,
        currentUser: user.id
      });

      // Check if author exists and has an id
      if (!currentPost.author || !currentPost.author.id) {
        console.error('Post author is missing or invalid:', currentPost.author);
        // Don't set error immediately, try to refetch the post
        if (!isRefetching) {
          console.log('🔄 Attempting to refetch post to get author information...');
          setIsRefetching(true);
          fetchPost(postId).finally(() => setIsRefetching(false));
        }
        return;
      }

      if (currentPost.author.id !== user.id) {
        console.log('❌ User not authorized to edit this post');
        setError('You are not authorized to edit this post');
      } else {
        console.log('✅ User authorized to edit this post');
        setPost(currentPost);
      }
    }
  }, [currentPost, user, postId, fetchPost]);

  if (!isAuthenticated || !user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (isLoading || isRefetching) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-600">
              {isRefetching ? 'Refetching post data...' : 'Loading post...'}
            </p>
          </div>
        </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              {error}
            </h1>
            <p className="text-gray-600 mb-6">
              {error === 'You are not authorized to edit this post'
                ? 'Only the author can edit this post.'
                : 'The post could not be loaded.'}
            </p>
            <button
              onClick={() => router.back()}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!post) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Post Not Found
            </h1>
            <p className="text-gray-600 mb-6">
              The post you&apos;re trying to edit doesn&apos;t exist.
            </p>
            <button
              onClick={() => router.push('/blog')}
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Back to Blog
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <PostForm mode="edit" post={post} />
      </div>
    </div>
  );
};

export default EditPostPage;
