import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { blogAPI } from '@/lib/api';
import { Post, Category, Tag, CreatePostData, UpdatePostData } from '@/types';
import toast from 'react-hot-toast';

interface BlogState {
  // State
  posts: Post[];
  featuredPosts: Post[];
  categories: Category[];
  tags: Tag[];
  currentPost: Post | null;
  myPosts: Post[];
  isLoading: boolean;
  isCreating: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: string | null;
  pagination: {
    count: number;
    next: string | null;
    previous: string | null;
    currentPage: number;
  };
  filters: {
    search: string;
    category: number | null;
    tag: number | null;
    status: 'all' | 'draft' | 'published';
  };

  // Actions
  // Fetch posts
  fetchPosts: (params?: Record<string, string | number>) => Promise<void>;
  fetchFeaturedPosts: () => Promise<void>;
  fetchPost: (id: number) => Promise<void>;
  fetchPostBySlug: (slug: string) => Promise<void>;
  fetchMyPosts: (params?: Record<string, string | number>) => Promise<void>;
  fetchCategories: () => Promise<void>;
  fetchTags: () => Promise<void>;

  // CRUD operations
  createPost: (data: CreatePostData) => Promise<boolean>;
  updatePost: (id: number, data: UpdatePostData) => Promise<boolean>;
  deletePost: (id: number) => Promise<boolean>;
  publishPost: (id: number) => Promise<boolean>;
  unpublishPost: (id: number) => Promise<boolean>;

  // Filters and search
  setSearch: (search: string) => void;
  setCategoryFilter: (categoryId: number | null) => void;
  setTagFilter: (tagId: number | null) => void;
  setStatusFilter: (status: 'all' | 'draft' | 'published') => void;
  clearFilters: () => void;

  // State management
  setCurrentPost: (post: Post | null) => void;
  clearError: () => void;
  resetState: () => void;
}

const initialState: Omit<BlogState,
  | 'fetchPosts'
  | 'fetchFeaturedPosts'
  | 'fetchPost'
  | 'fetchPostBySlug'
  | 'fetchMyPosts'
  | 'fetchCategories'
  | 'fetchTags'
  | 'createPost'
  | 'updatePost'
  | 'deletePost'
  | 'publishPost'
  | 'unpublishPost'
  | 'setSearch'
  | 'setCategoryFilter'
  | 'setTagFilter'
  | 'setStatusFilter'
  | 'clearFilters'
  | 'setCurrentPost'
  | 'clearError'
  | 'resetState'
> = {
  posts: [],
  featuredPosts: [],
  categories: [],
  tags: [],
  currentPost: null,
  myPosts: [],
  isLoading: false,
  isCreating: false,
  isUpdating: false,
  isDeleting: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
  },
  filters: {
    search: '',
    category: null,
    tag: null,
    status: 'all' as const,
  },
};

export const useBlogStore = create<BlogState>()(
  devtools(
    (set, get) => ({
      ...initialState,

      // Fetch posts
      fetchPosts: async (params = {}) => {
        set({ isLoading: true, error: null });
        try {
          const response = await blogAPI.getPosts(params);
          const { results, count, next, previous } = response.data;

          // Extract current page from next/previous URLs
          let currentPage = 1;
          if (next) {
            const url = new URL(next);
            const page = url.searchParams.get('page');
            if (page) {
              currentPage = parseInt(page) - 1;
            }
          } else if (previous) {
            const url = new URL(previous);
            const page = url.searchParams.get('page');
            if (page) {
              currentPage = parseInt(page) + 1;
            }
          }

          set({
            posts: results,
            pagination: {
              count,
              next,
              previous,
              currentPage,
            },
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.message || 'Failed to fetch posts',
            isLoading: false
          });
          toast.error('Failed to load posts');
        }
      },

      fetchFeaturedPosts: async () => {
        try {
          const response = await blogAPI.getFeaturedPosts();
          set({ featuredPosts: response.data });
        } catch (error: any) {
          console.error('Failed to fetch featured posts:', error);
        }
      },

      fetchPost: async (id: number) => {
        set({ isLoading: true, error: null });
        try {
          const response = await blogAPI.getPost(id);
          set({ currentPost: response.data, isLoading: false });
        } catch (error: any) {
          set({
            error: error.message || 'Failed to fetch post',
            isLoading: false
          });
          toast.error('Failed to load post');
        }
      },

      fetchPostBySlug: async (slug: string) => {
        console.log('🔍 fetchPostBySlug called with slug:', slug);
        set({ isLoading: true, error: null });
        try {
          const response = await blogAPI.getPostBySlug(slug);
          console.log('✅ fetchPostBySlug successful:', response.data.title);
          set({ currentPost: response.data, isLoading: false });
        } catch (error: any) {
          console.error('❌ fetchPostBySlug failed:', error);
          set({
            error: error.message || 'Failed to fetch post',
            isLoading: false
          });
          toast.error('Failed to load post');
        }
      },

      fetchMyPosts: async (params = {}) => {
        set({ isLoading: true, error: null });
        try {
          const response = await blogAPI.getMyPosts(params);
          const { results, count, next, previous } = response.data;

          let currentPage = 1;
          if (next) {
            const url = new URL(next);
            const page = url.searchParams.get('page');
            if (page) {
              currentPage = parseInt(page) - 1;
            }
          } else if (previous) {
            const url = new URL(previous);
            const page = url.searchParams.get('page');
            if (page) {
              currentPage = parseInt(page) + 1;
            }
          }

          set({
            myPosts: results,
            pagination: {
              count,
              next,
              previous,
              currentPage,
            },
            isLoading: false,
          });
        } catch (error: any) {
          set({
            error: error.message || 'Failed to fetch your posts',
            isLoading: false
          });
          toast.error('Failed to load your posts');
        }
      },

      fetchCategories: async () => {
        try {
          const response = await blogAPI.getCategories();
          // Handle paginated response
          const categories = response.data.results || response.data;
          set({ categories });
        } catch (error: any) {
          console.error('Failed to fetch categories:', error);
        }
      },

      fetchTags: async () => {
        try {
          const response = await blogAPI.getTags();
          // Handle paginated response
          const tags = response.data.results || response.data;
          set({ tags });
        } catch (error: any) {
          console.error('Failed to fetch tags:', error);
        }
      },

      // CRUD operations
      createPost: async (data: CreatePostData) => {
        set({ isCreating: true, error: null });
        try {
          const response = await blogAPI.createPost(data);
          const newPost = response.data;

          // Optimistic update - add to posts list
          set(state => ({
            posts: [newPost, ...state.posts],
            myPosts: [newPost, ...state.myPosts],
            isCreating: false,
          }));

          toast.success('Post created successfully!');
          return true;
        } catch (error: any) {
          set({
            error: error.message || 'Failed to create post',
            isCreating: false
          });
          toast.error('Failed to create post');
          return false;
        }
      },

      updatePost: async (id: number, data: UpdatePostData) => {
        set({ isUpdating: true, error: null });
        try {
          console.log('🔄 Updating post with ID:', id);
          console.log('📝 Update data:', data);

          const response = await blogAPI.updatePost(id, data);
          const updatedPost = response.data;

          console.log('✅ Post update successful');
          console.log('📝 Updated post data:', updatedPost);

          // Optimistic update - update in all lists
          set(state => {
            // Preserve author information if it's missing in the response
            const postWithAuthor = state.currentPost?.id === id && state.currentPost?.author
              ? { ...updatedPost, author: state.currentPost.author }
              : updatedPost;

            return {
              posts: state.posts.map(post =>
                post.id === id ? postWithAuthor : post
              ),
              myPosts: state.myPosts.map(post =>
                post.id === id ? postWithAuthor : post
              ),
              featuredPosts: state.featuredPosts.map(post =>
                post.id === id ? postWithAuthor : post
              ),
              currentPost: state.currentPost?.id === id ? postWithAuthor : state.currentPost,
              isUpdating: false,
            };
          });

                    toast.success('Post updated successfully!');
          return true;
        } catch (error: any) {
          console.error('❌ Post update failed:', error);
          console.error('❌ Error response:', error.response);
          console.error('❌ Error status:', error.response?.status);

          set({
            error: error.message || 'Failed to update post',
            isUpdating: false
          });
          toast.error('Failed to update post');
          return false;
        }
      },

      deletePost: async (id: number) => {
        set({ isDeleting: true, error: null });
        try {
          await blogAPI.deletePost(id);

          // Optimistic update - remove from all lists
          set(state => ({
            posts: state.posts.filter(post => post.id !== id),
            myPosts: state.myPosts.filter(post => post.id !== id),
            featuredPosts: state.featuredPosts.filter(post => post.id !== id),
            currentPost: state.currentPost?.id === id ? null : state.currentPost,
            isDeleting: false,
          }));

          toast.success('Post deleted successfully!');
          return true;
        } catch (error: any) {
          set({
            error: error.message || 'Failed to delete post',
            isDeleting: false
          });
          toast.error('Failed to delete post');
          return false;
        }
      },

      publishPost: async (id: number) => {
        try {
          await blogAPI.publishPost(id);

          // Optimistic update
          set(state => ({
            posts: state.posts.map(post =>
              post.id === id ? { ...post, status: 'published' as const } : post
            ),
            myPosts: state.myPosts.map(post =>
              post.id === id ? { ...post, status: 'published' as const } : post
            ),
            currentPost: state.currentPost?.id === id
              ? { ...state.currentPost, status: 'published' as const }
              : state.currentPost,
          }));

          toast.success('Post published successfully!');
          return true;
        } catch (error: any) {
          toast.error('Failed to publish post');
          return false;
        }
      },

      unpublishPost: async (id: number) => {
        try {
          await blogAPI.unpublishPost(id);

          // Optimistic update
          set(state => ({
            posts: state.posts.map(post =>
              post.id === id ? { ...post, status: 'draft' as const } : post
            ),
            myPosts: state.myPosts.map(post =>
              post.id === id ? { ...post, status: 'draft' as const } : post
            ),
            currentPost: state.currentPost?.id === id
              ? { ...state.currentPost, status: 'draft' as const }
              : state.currentPost,
          }));

          toast.success('Post unpublished successfully!');
          return true;
        } catch (error: any) {
          toast.error('Failed to unpublish post');
          return false;
        }
      },

      // Filters and search
      setSearch: (search: string) => {
        set(state => ({
          filters: { ...state.filters, search },
          pagination: { ...state.pagination, currentPage: 1 },
        }));
      },

      setCategoryFilter: (categoryId: number | null) => {
        set(state => ({
          filters: { ...state.filters, category: categoryId },
          pagination: { ...state.pagination, currentPage: 1 },
        }));
      },

      setTagFilter: (tagId: number | null) => {
        set(state => ({
          filters: { ...state.filters, tag: tagId },
          pagination: { ...state.pagination, currentPage: 1 },
        }));
      },

      setStatusFilter: (status: 'all' | 'draft' | 'published') => {
        set(state => ({
          filters: { ...state.filters, status },
          pagination: { ...state.pagination, currentPage: 1 },
        }));
      },

      clearFilters: () => {
        set(state => ({
          filters: initialState.filters,
          pagination: { ...state.pagination, currentPage: 1 },
        }));
      },

      // State management
      setCurrentPost: (post: Post | null) => {
        set({ currentPost: post });
      },

      clearError: () => {
        set({ error: null });
      },

      resetState: () => {
        set(initialState);
      },
    }),
    {
      name: 'blog-store',
    }
  )
);
