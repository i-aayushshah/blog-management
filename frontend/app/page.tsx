'use client';

import React, { useEffect } from 'react';
import Link from 'next/link';
import { ArrowRight, BookOpen, Users, FileText, TrendingUp } from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import { useAuthStore } from '@/store/authStore';
import PostList from '@/components/blog/PostList';
import PostCard from '@/components/blog/PostCard';
import Button from '@/components/ui/Button';

const HomePage: React.FC = () => {
  const { user } = useAuthStore();
  const {
    featuredPosts,
    posts,
    fetchFeaturedPosts,
    fetchPosts
  } = useBlogStore();

  useEffect(() => {
    fetchFeaturedPosts();
    fetchPosts({ page: 1, limit: 6 });
  }, [fetchFeaturedPosts, fetchPosts]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Share Your Story
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100 max-w-3xl mx-auto">
              Create, publish, and share your thoughts with the world.
              Join our community of writers and readers.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              {user ? (
                <Link href="/create-post">
                  <Button size="lg" className="text-lg px-8 py-4">
                    <FileText className="w-5 h-5 mr-2" />
                    Write Your First Post
                  </Button>
                </Link>
              ) : (
                <Link href="/register">
                  <Button size="lg" className="text-lg px-8 py-4">
                    <Users className="w-5 h-5 mr-2" />
                    Join Our Community
                  </Button>
                </Link>
              )}
              <Link href="/blog">
                <Button variant="outline" size="lg" className="text-lg px-8 py-4 border-white text-white hover:bg-white hover:text-blue-600">
                  <BookOpen className="w-5 h-5 mr-2" />
                  Explore Posts
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Posts Section */}
      {featuredPosts.length > 0 && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between mb-8">
              <div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Featured Posts
                </h2>
                <p className="text-gray-600">
                  Discover our most popular and trending content
                </p>
              </div>
              <Link href="/blog">
                <Button variant="outline" className="flex items-center gap-2">
                  View All Posts
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {featuredPosts.slice(0, 2).map((post) => (
                <PostCard
                  key={post.id}
                  post={post}
                  variant="featured"
                />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Latest Posts Section */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Latest Posts
              </h2>
              <p className="text-gray-600">
                Fresh content from our community
              </p>
            </div>
            <Link href="/blog">
              <Button variant="outline" className="flex items-center gap-2">
                View All Posts
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>

          <PostList
            posts={posts.slice(0, 6)}
            showPagination={false}
            emptyMessage="No posts yet. Be the first to create one!"
          />
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Our Community
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Join thousands of writers and readers who are already part of our growing community
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-blue-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                {posts.length}+
              </h3>
              <p className="text-gray-600">Posts Published</p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                Growing
              </h3>
              <p className="text-gray-600">Active Writers</p>
            </div>

            <div className="text-center">
              <div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">
                Daily
              </h3>
              <p className="text-gray-600">New Content</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Start Writing?
          </h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Share your knowledge, experiences, and stories with our community.
            Start creating content that matters.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            {user ? (
              <Link href="/create-post">
                <Button size="lg" variant="secondary" className="text-lg px-8 py-4">
                  <FileText className="w-5 h-5 mr-2" />
                  Create Your First Post
                </Button>
              </Link>
            ) : (
              <Link href="/register">
                <Button size="lg" variant="secondary" className="text-lg px-8 py-4">
                  <Users className="w-5 h-5 mr-2" />
                  Get Started Today
                </Button>
              </Link>
            )}
            <Link href="/blog">
              <Button size="lg" variant="outline" className="text-lg px-8 py-4 border-white text-white hover:bg-white hover:text-blue-600">
                <BookOpen className="w-5 h-5 mr-2" />
                Explore Posts
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
