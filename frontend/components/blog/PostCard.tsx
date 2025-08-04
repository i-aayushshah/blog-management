'use client';

import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Calendar, Clock, User, Eye, Tag, BookOpen } from 'lucide-react';
import { Post } from '@/types';
import { formatDate, formatRelativeTime, truncateText, getDisplayName } from '@/lib/utils';
import { cn } from '@/lib/utils';

interface PostCardProps {
  post: Post;
  variant?: 'default' | 'featured' | 'compact';
  showAuthor?: boolean;
  showExcerpt?: boolean;
  className?: string;
}

const PostCard: React.FC<PostCardProps> = ({
  post,
  variant = 'default',
  showAuthor = true,
  showExcerpt = true,
  className,
}) => {
  const isFeatured = variant === 'featured';
  const isCompact = variant === 'compact';

  return (
    <article className={cn(
      'group bg-white rounded-lg shadow-sm hover:shadow-md transition-all duration-300 overflow-hidden border border-gray-100',
      isFeatured && 'lg:col-span-2',
      isCompact && 'flex gap-4',
      className
    )}>
      {/* Featured Image */}
      {post.featured_image && (
        <div className={cn(
          'relative overflow-hidden bg-gray-100',
          isFeatured ? 'h-64 lg:h-80' : isCompact ? 'w-24 h-24 flex-shrink-0' : 'h-48'
        )}>
          <Image
            src={post.featured_image}
            alt={post.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-300"
            sizes={isFeatured ? '(max-width: 768px) 100vw, 50vw' : '(max-width: 768px) 100vw, 33vw'}
          />
          {/* Status Badge */}
          {post.status === 'draft' && (
            <div className="absolute top-2 left-2 bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded-full font-medium">
              Draft
            </div>
          )}
        </div>
      )}

      {/* Content */}
      <div className={cn(
        'p-4',
        isCompact && 'flex-1 min-w-0'
      )}>
        {/* Category */}
        {post.category && post.category.name && (
          <Link
            href={`/blog/category/${post.category.slug}`}
            className="inline-block text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors mb-2"
          >
            {post.category.name}
          </Link>
        )}

        {/* Title */}
        <Link href={`/blog/${post.slug}`}>
          <h2 className={cn(
            'font-bold text-gray-900 hover:text-blue-600 transition-colors line-clamp-2',
            isFeatured ? 'text-xl lg:text-2xl' : isCompact ? 'text-base' : 'text-lg'
          )}>
            {post.title}
          </h2>
        </Link>

        {/* Excerpt */}
        {showExcerpt && post.excerpt && (
          <p className={cn(
            'text-gray-600 mt-2 line-clamp-3',
            isCompact ? 'text-sm' : 'text-base'
          )}>
            {truncateText(post.excerpt, isCompact ? 80 : 120)}
          </p>
        )}

        {/* Tags */}
        {post.tags && post.tags.length > 0 && !isCompact && (
          <div className="flex flex-wrap gap-1 mt-3">
            {post.tags.slice(0, 3).map((tag) => (
              <Link
                key={tag.id}
                href={`/blog/tag/${tag.slug}`}
                className="inline-flex items-center text-xs text-gray-500 hover:text-blue-600 transition-colors"
              >
                <Tag className="w-3 h-3 mr-1" />
                {tag.name}
              </Link>
            ))}
            {post.tags.length > 3 && (
              <span className="text-xs text-gray-400">
                +{post.tags.length - 3} more
              </span>
            )}
          </div>
        )}

        {/* Meta Information */}
        <div className={cn(
          'flex items-center justify-between mt-4 text-sm text-gray-500',
          isCompact && 'mt-2'
        )}>
          <div className="flex items-center gap-4">
            {/* Author */}
            {showAuthor && post.author && (
              <div className="flex items-center gap-1">
                <User className="w-4 h-4" />
                <span className="truncate">
                  {getDisplayName(post.author)}
                </span>
              </div>
            )}

            {/* Date */}
            <div className="flex items-center gap-1">
              <Calendar className="w-4 h-4" />
              <time dateTime={post.created_at}>
                {formatRelativeTime(post.created_at)}
              </time>
            </div>

            {/* Reading Time */}
            <div className="flex items-center gap-1">
              <BookOpen className="w-4 h-4" />
              <span>{post.reading_time} min read</span>
            </div>
          </div>

          {/* View Count (if available) */}
          {(post as { view_count?: number }).view_count !== undefined && (
            <div className="flex items-center gap-1">
              <Eye className="w-4 h-4" />
              <span>{(post as { view_count?: number }).view_count}</span>
            </div>
          )}
        </div>
      </div>
    </article>
  );
};

export default PostCard;
