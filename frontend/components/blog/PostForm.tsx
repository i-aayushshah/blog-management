'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import {
  Save,
  Eye,
  EyeOff,
  Upload,
  X,
  Loader2,
  AlertCircle,
  CheckCircle
} from 'lucide-react';
import { useBlogStore } from '@/store/blogStore';
import { useAuthStore } from '@/store/authStore';
import { CreatePostData, UpdatePostData, Post, Category, Tag } from '@/types';
import { generateSlug } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';
import { cn } from '@/lib/utils';

interface PostFormProps {
  post?: Post;
  mode: 'create' | 'edit';
  onSuccess?: () => void;
}

interface FormData {
  title: string;
  content: string;
  excerpt: string;
  status: 'draft' | 'published';
  category_id: number | null;
  tag_ids: number[];
}

const PostForm: React.FC<PostFormProps> = ({ post, mode, onSuccess }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [featuredImage, setFeaturedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(
    post?.featured_image || null
  );
  const [selectedTags, setSelectedTags] = useState<number[]>(
    post?.tags?.map(tag => tag.id) || []
  );

  const router = useRouter();
  const { user, debugState } = useAuthStore();
  const {
    categories,
    tags,
    fetchCategories,
    fetchTags,
    createPost,
    updatePost,
    isCreating,
    isUpdating,
  } = useBlogStore();

  // Debug user state before update
  useEffect(() => {
    console.log('🔍 PostForm: User state:', {
      user: user,
      displayName: user?.first_name || user?.username || 'User'
    });
  }, [user]);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid },
    reset,
  } = useForm<FormData>({
    defaultValues: {
      title: post?.title || '',
      content: post?.content || '',
      excerpt: post?.excerpt || '',
      status: post?.status || 'draft',
      category_id: post?.category?.id || null,
      tag_ids: post?.tags?.map(tag => tag.id) || [],
    },
  });

  const watchedTitle = watch('title');
  const watchedContent = watch('content');

  // Fetch categories and tags on mount
  useEffect(() => {
    fetchCategories();
    fetchTags();
  }, [fetchCategories, fetchTags]);

  // Auto-generate excerpt from content
  useEffect(() => {
    if (watchedContent && !watch('excerpt')) {
      const excerpt = watchedContent
        .replace(/<[^>]*>/g, '') // Remove HTML tags
        .substring(0, 160)
        .trim();
      setValue('excerpt', excerpt);
    }
  }, [watchedContent, setValue, watch]);

  // Handle image upload
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) { // 5MB limit
        alert('Image size must be less than 5MB');
        return;
      }

      setFeaturedImage(file);
      const reader = new FileReader();
      reader.onload = (e) => {
        setImagePreview(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove image
  const handleRemoveImage = () => {
    setFeaturedImage(null);
    setImagePreview(null);
  };

  // Handle tag selection
  const handleTagToggle = (tagId: number) => {
    setSelectedTags(prev =>
      prev.includes(tagId)
        ? prev.filter(id => id !== tagId)
        : [...prev, tagId]
    );
  };

  // Handle form submission
  const onSubmit = async (data: FormData) => {
    if (!user) {
      alert('You must be logged in to create/edit posts');
      return;
    }

    setIsSubmitting(true);

    try {
      // Create the post data object
      const postData: CreatePostData = {
        title: data.title,
        content: data.content,
        excerpt: data.excerpt,
        status: data.status,
        category_id: data.category_id || undefined,
        tag_ids: selectedTags.length > 0 ? selectedTags : undefined,
        featured_image: featuredImage || undefined,
      };

      let success = false;
      if (mode === 'create') {
        success = await createPost(postData);
        if (success) {
          router.push('/blog');
        }
      } else if (post) {
                console.log('🔍 Before post update - User state:', {
          user: user,
          displayName: user?.first_name || user?.username || 'User'
        });

        success = await updatePost(post.id, postData);

        console.log('🔍 After post update - User state:', {
          user: user,
          displayName: user?.first_name || user?.username || 'User'
        });

        if (success) {
          // Don't refresh auth - let it persist naturally
          console.log('✅ Post updated successfully, auth state preserved');
          router.push('/profile');
        }
      }

      if (success && onSuccess) {
        onSuccess();
      }
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const isSubmittingOrLoading = isSubmitting || isCreating || isUpdating;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        {/* Header */}
        <div className="px-6 py-4 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900">
            {mode === 'create' ? 'Create New Post' : 'Edit Post'}
          </h1>
          <p className="text-gray-600 mt-1">
            {mode === 'create'
              ? 'Share your thoughts with the world'
              : 'Update your post content and settings'
            }
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="p-6 space-y-6">
          {/* Title */}
          <div>
            <Input
              label="Post Title"
              type="text"
              placeholder="Enter your post title"
              error={errors.title?.message}
              {...register('title', {
                required: 'Title is required',
                minLength: {
                  value: 5,
                  message: 'Title must be at least 5 characters',
                },
                maxLength: {
                  value: 200,
                  message: 'Title must be less than 200 characters',
                },
              })}
            />
            {watchedTitle && (
              <p className="text-sm text-gray-500 mt-1">
                Slug: {generateSlug(watchedTitle)}
              </p>
            )}
          </div>

          {/* Content */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Content
            </label>
            <div className="relative">
              <textarea
                {...register('content', {
                  required: 'Content is required',
                  minLength: {
                    value: 50,
                    message: 'Content must be at least 50 characters',
                  },
                })}
                rows={12}
                placeholder="Write your post content here... You can use basic HTML tags like <strong>, <em>, <a>, <ul>, <li>, etc."
                className={cn(
                  'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-y',
                  errors.content && 'border-red-300 focus:ring-red-500'
                )}
              />
              {errors.content && (
                <p className="text-sm text-red-600 mt-1">{errors.content.message}</p>
              )}
            </div>
            <div className="flex items-center justify-between mt-2 text-sm text-gray-500">
              <span>
                {watchedContent.length} characters
              </span>
              <button
                type="button"
                onClick={() => setShowPreview(!showPreview)}
                className="flex items-center gap-1 text-blue-600 hover:text-blue-700"
              >
                {showPreview ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                {showPreview ? 'Hide Preview' : 'Show Preview'}
              </button>
            </div>
          </div>

          {/* Content Preview */}
          {showPreview && watchedContent && (
            <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
              <h3 className="text-sm font-medium text-gray-700 mb-2">Preview:</h3>
              <div
                className="prose prose-sm max-w-none"
                dangerouslySetInnerHTML={{ __html: watchedContent }}
              />
            </div>
          )}

          {/* Excerpt */}
          <div>
            <Input
              label="Excerpt"
              type="text"
              placeholder="Brief description of your post (auto-generated from content)"
              error={errors.excerpt?.message}
              {...register('excerpt', {
                maxLength: {
                  value: 300,
                  message: 'Excerpt must be less than 300 characters',
                },
              })}
            />
            <p className="text-sm text-gray-500 mt-1">
              A brief summary that will appear in post previews
            </p>
          </div>

          {/* Featured Image */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Featured Image
            </label>
            <div className="space-y-4">
              {imagePreview && (
                <div className="relative">
                  <img
                    src={imagePreview}
                    alt="Featured image preview"
                    className="w-full h-48 object-cover rounded-lg border border-gray-200"
                  />
                  <button
                    type="button"
                    onClick={handleRemoveImage}
                    className="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>
              )}

              <div className="flex items-center justify-center w-full">
                <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                  <div className="flex flex-col items-center justify-center pt-5 pb-6">
                    <Upload className="w-8 h-8 mb-2 text-gray-400" />
                    <p className="mb-2 text-sm text-gray-500">
                      <span className="font-semibold">Click to upload</span> or drag and drop
                    </p>
                    <p className="text-xs text-gray-500">PNG, JPG, GIF up to 5MB</p>
                  </div>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    className="hidden"
                  />
                </label>
              </div>
            </div>
          </div>

          {/* Category and Tags */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Category */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Category
              </label>
              <select
                {...register('category_id')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              >
                <option value="">Select a category</option>
                {categories && categories.map((category) => (
                  <option key={category.id} value={category.id}>
                    {category.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Status */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                {...register('status')}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
              </select>
            </div>
          </div>

          {/* Tags */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <div className="flex flex-wrap gap-2">
              {tags && tags.map((tag) => (
                <button
                  key={tag.id}
                  type="button"
                  onClick={() => handleTagToggle(tag.id)}
                  className={cn(
                    'px-3 py-1 text-sm rounded-full border transition-colors',
                    selectedTags.includes(tag.id)
                      ? 'bg-blue-100 text-blue-700 border-blue-200'
                      : 'bg-gray-100 text-gray-700 border-gray-200 hover:bg-gray-200'
                  )}
                >
                  {tag.name}
                </button>
              ))}
            </div>
            <p className="text-sm text-gray-500 mt-1">
              Click tags to select/deselect them
            </p>
          </div>

          {/* Form Actions */}
          <div className="flex items-center justify-between pt-6 border-t border-gray-200">
            <div className="flex items-center gap-4">
              <Button
                type="submit"
                loading={isSubmittingOrLoading}
                disabled={isSubmittingOrLoading}
                className="flex items-center gap-2"
              >
                <Save className="w-4 h-4" />
                {mode === 'create' ? 'Create Post' : 'Update Post'}
              </Button>

              <Button
                type="button"
                variant="outline"
                onClick={() => router.back()}
                disabled={isSubmittingOrLoading}
              >
                Cancel
              </Button>
            </div>

            <div className="flex items-center gap-2 text-sm text-gray-500">
              {isSubmittingOrLoading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Saving...</span>
                </>
              ) : (
                <>
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Ready to save</span>
                </>
              )}
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default PostForm;
