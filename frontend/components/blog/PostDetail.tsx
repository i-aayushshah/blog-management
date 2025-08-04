'use client';

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import {
  Calendar,
  User,
  BookOpen,
  Eye,
  EyeOff,
  Tag,
  Edit,
  Trash2,
  Share2,
  ArrowLeft
} from 'lucide-react';
import { useRouter } from 'next/navigation';
import { Post } from '@/types';
import { formatDate, formatRelativeTime, getDisplayName } from '@/lib/utils';
import { useBlogStore } from '@/store/blogStore';
import { useAuthStore } from '@/store/authStore';
import Button from '@/components/ui/Button';
import { cn } from '@/lib/utils';

interface PostDetailProps {
  post: Post;
  className?: string;
}

const PostDetail: React.FC<PostDetailProps> = ({ post, className }) => {
  const router = useRouter();
  const { user } = useAuthStore();
  const { deletePost, publishPost, unpublishPost, isDeleting } = useBlogStore();

  const isAuthor = user?.id === post.author.id;
  const canEdit = isAuthor;

  const handleEdit = () => {
    router.push(`/edit-post/${post.id}`);
  };

  const handleDelete = async () => {
    if (confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
      const success = await deletePost(post.id);
      if (success) {
        router.push('/blog');
      }
    }
  };

  const handlePublish = async () => {
    const success = await publishPost(post.id);
    if (success) {
      // Refresh the page to show updated status
      window.location.reload();
    }
  };

  const handleUnpublish = async () => {
    const success = await unpublishPost(post.id);
    if (success) {
      // Refresh the page to show updated status
      window.location.reload();
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: post.title,
        text: post.excerpt,
        url: window.location.href,
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  return (
    <article className={cn('max-w-4xl mx-auto', className)}>
      {/* Back Button */}
      <div className="mb-6">
        <Button
          variant="ghost"
          onClick={() => router.back()}
          className="flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Blog
        </Button>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Featured Image */}
        {post.featured_image && (
          <div className="relative h-64 md:h-96 bg-gray-100">
            <Image
              src={post.featured_image}
              alt={post.title}
              fill
              className="object-cover"
              priority
            />
            {/* Status Badge */}
            {post.status === 'draft' && (
              <div className="absolute top-4 left-4 bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                Draft
              </div>
            )}
          </div>
        )}

        {/* Content */}
        <div className="p-6 md:p-8">
          {/* Header */}
          <header className="mb-6">
            {/* Category */}
            {post.category && (
              <Link
                href={`/blog/category/${post.category.slug}`}
                className="inline-block text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors mb-3"
              >
                {post.category.name}
              </Link>
            )}

            {/* Title */}
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4 leading-tight">
              {post.title}
            </h1>

            {/* Meta Information */}
            <div className="flex flex-wrap items-center gap-4 text-sm text-gray-500 mb-6">
              {/* Author */}
              <div className="flex items-center gap-1">
                <User className="w-4 h-4" />
                <span>{getDisplayName(post.author)}</span>
              </div>

              {/* Date */}
              <div className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                <time dateTime={post.created_at}>
                  {formatDate(post.created_at)}
                </time>
              </div>

              {/* Reading Time */}
              <div className="flex items-center gap-1">
                <BookOpen className="w-4 h-4" />
                <span>{post.reading_time} min read</span>
              </div>

              {/* View Count */}
              {(post as any).view_count !== undefined && (
                <div className="flex items-center gap-1">
                  <Eye className="w-4 h-4" />
                  <span>{(post as any).view_count} views</span>
                </div>
              )}
            </div>

            {/* Tags */}
            {post.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {post.tags.map((tag) => (
                  <Link
                    key={tag.id}
                    href={`/blog/tag/${tag.slug}`}
                    className="inline-flex items-center gap-1 px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors"
                  >
                    <Tag className="w-3 h-3" />
                    {tag.name}
                  </Link>
                ))}
              </div>
            )}

            {/* Excerpt */}
            {post.excerpt && (
              <div className="bg-gray-50 rounded-lg p-4 mb-6">
                <p className="text-gray-700 text-lg leading-relaxed">
                  {post.excerpt}
                </p>
              </div>
            )}
          </header>

          {/* Content */}
          <div className="prose prose-lg max-w-none">
            <div
              dangerouslySetInnerHTML={{ __html: post.content }}
              className="text-gray-800 leading-relaxed"
            />
          </div>

          {/* Footer */}
          <footer className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              {/* Author Info */}
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                  <User className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">
                    {getDisplayName(post.author)}
                  </p>
                  <p className="text-sm text-gray-500">
                    Published {formatRelativeTime(post.created_at)}
                  </p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-2">
                {/* Share Button */}
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleShare}
                  className="flex items-center gap-2"
                >
                  <Share2 className="w-4 h-4" />
                  Share
                </Button>

                {/* Author Actions */}
                {canEdit && (
                  <>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleEdit}
                      className="flex items-center gap-2"
                    >
                      <Edit className="w-4 h-4" />
                      Edit
                    </Button>

                    {post.status === 'draft' ? (
                      <Button
                        size="sm"
                        onClick={handlePublish}
                        className="flex items-center gap-2"
                      >
                        <Eye className="w-4 h-4" />
                        Publish
                      </Button>
                    ) : (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={handleUnpublish}
                        className="flex items-center gap-2"
                      >
                        <EyeOff className="w-4 h-4" />
                        Unpublish
                      </Button>
                    )}

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleDelete}
                      loading={isDeleting}
                      className="flex items-center gap-2 text-red-600 hover:text-red-700 hover:border-red-300"
                    >
                      <Trash2 className="w-4 h-4" />
                      Delete
                    </Button>
                  </>
                )}
              </div>
            </div>
          </footer>
        </div>
      </div>
    </article>
  );
};

export default PostDetail;
