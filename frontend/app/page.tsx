import React from 'react';
import Navigation from '@/components/layout/Navigation';
import { BookOpen, Users, FileText, Shield } from 'lucide-react';
import Link from 'next/link';
import Button from '@/components/ui/Button';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />

      {/* Hero Section */}
      <section className="bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-gray-900 sm:text-6xl">
              Welcome to{' '}
              <span className="text-blue-600">Blog Management</span>
            </h1>
            <p className="mt-6 text-xl text-gray-600 max-w-3xl mx-auto">
              A modern, full-stack blog management system built with Next.js, Django, and Tailwind CSS.
              Create, manage, and share your content with ease.
            </p>
            <div className="mt-10 flex justify-center space-x-4">
              <Link href="/blog">
                <Button size="lg">
                  Explore Blog
                </Button>
              </Link>
              <Link href="/register">
                <Button variant="outline" size="lg">
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900">
              Powerful Features
            </h2>
            <p className="mt-4 text-lg text-gray-600">
              Everything you need to manage your blog effectively
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <BookOpen className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Content Management
              </h3>
              <p className="text-gray-600">
                Create, edit, and manage your blog posts with a rich editor and advanced features.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                User Authentication
              </h3>
              <p className="text-gray-600">
                Secure user registration, login, and profile management with email verification.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <FileText className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Rich Content
              </h3>
              <p className="text-gray-600">
                Support for categories, tags, featured images, and reading time estimation.
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-md">
              <div className="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-red-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Security & Performance
              </h3>
              <p className="text-gray-600">
                JWT authentication, role-based permissions, and optimized performance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white mb-4">
              Ready to Start Blogging?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join our community and start sharing your thoughts with the world.
            </p>
            <div className="flex justify-center space-x-4">
              <Link href="/register">
                <Button variant="secondary" size="lg">
                  Create Account
                </Button>
              </Link>
              <Link href="/login">
                <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-blue-600">
                  Sign In
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <BookOpen className="h-8 w-8 text-blue-400" />
              <span className="text-xl font-bold">Blog Management</span>
            </div>
            <p className="text-gray-400">
              A modern blog management system built with Next.js, Django, and Tailwind CSS.
            </p>
            <div className="mt-8 text-sm text-gray-400">
              © 2024 Blog Management. All rights reserved.
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
