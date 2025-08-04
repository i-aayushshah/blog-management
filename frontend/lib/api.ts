import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { toast } from 'react-hot-toast';
import { 
  LoginCredentials, 
  RegisterCredentials, 
  EmailVerificationData, 
  PasswordResetRequest, 
  PasswordResetData,
  User,
  CreatePostData,
  UpdatePostData
} from '@/types';

// API Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    // Get token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('blog_auth_token') : null;

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    const { response } = error;

    if (response) {
      const { status, data } = response;

      // Handle different error status codes
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          if (typeof window !== 'undefined') {
            localStorage.removeItem('blog_auth_token');
            window.location.href = '/login';
          }
          toast.error('Session expired. Please login again.');
          break;

        case 403:
          toast.error('You do not have permission to perform this action.');
          break;

        case 404:
          toast.error('Resource not found.');
          break;

        case 422:
          // Validation errors
          if (data && typeof data === 'object') {
            const errorMessages = Object.values(data).flat();
            errorMessages.forEach((message: unknown) => {
              if (typeof message === 'string') {
                toast.error(message);
              }
            });
          } else {
            toast.error('Validation failed. Please check your input.');
          }
          break;

        case 500:
          toast.error('Server error. Please try again later.');
          break;

        default:
          if (data?.error) {
            toast.error(data.error);
          } else if (data?.message) {
            toast.error(data.message);
          } else {
            toast.error('An unexpected error occurred.');
          }
      }
    } else {
      // Network error
      toast.error('Network error. Please check your connection.');
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  // Authentication
  register: (data: RegisterCredentials) => api.post('/auth/register/', data),
  login: (data: LoginCredentials) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  verifyEmail: (data: EmailVerificationData) => api.post('/auth/verify-email/', data),
  resendVerification: (data: { email: string }) => api.post('/auth/resend-verification/', data),
  forgotPassword: (data: PasswordResetRequest) => api.post('/auth/forgot-password/', data),
  resetPassword: (data: PasswordResetData) => api.post('/auth/reset-password/', data),
  getProfile: () => api.get('/auth/profile/'),
  updateProfile: (data: Partial<User>) => api.put('/auth/profile/', data),
  checkAuth: () => api.get('/auth/check-auth/'),
};

export const blogAPI = {
  // Posts
  getPosts: (params?: Record<string, string | number>) => api.get('/blog/posts/', { params }),
  getPost: (id: number) => api.get(`/blog/posts/${id}/`),
  createPost: (data: CreatePostData) => api.post('/blog/posts/', data),
  updatePost: (id: number, data: UpdatePostData) => api.put(`/blog/posts/${id}/`, data),
  deletePost: (id: number) => api.delete(`/blog/posts/${id}/`),
  getMyPosts: (params?: Record<string, string | number>) => api.get('/blog/posts/my_posts/', { params }),
  publishPost: (id: number) => api.post(`/blog/posts/${id}/publish/`),
  unpublishPost: (id: number) => api.post(`/blog/posts/${id}/unpublish/`),
  getFeaturedPosts: () => api.get('/blog/posts/featured/'),

  // Categories
  getCategories: (params?: Record<string, string | number>) => api.get('/blog/categories/', { params }),
  getCategoryPosts: (id: number, params?: Record<string, string | number>) => api.get(`/blog/categories/${id}/posts/`, { params }),

  // Tags
  getTags: (params?: Record<string, string | number>) => api.get('/blog/tags/', { params }),
  getTagPosts: (id: number, params?: Record<string, string | number>) => api.get(`/blog/tags/${id}/posts/`, { params }),
};

// Utility functions
export const setAuthToken = (token: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('blog_auth_token', token);
  }
};

export const removeAuthToken = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('blog_auth_token');
  }
};

export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('blog_auth_token');
  }
  return null;
};

export default api;
