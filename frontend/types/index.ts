// User Types
export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  is_email_verified: boolean;
  profile_picture?: string;
  phone_number?: string;
  created_at: string;
  updated_at: string;
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
}

export interface AuthResponse {
  token: string;
  user: User;
}

export interface EmailVerificationData {
  token: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordResetData {
  token: string;
  new_password: string;
}

// Blog Types
export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  post_count: number;
  created_at: string;
}

export interface Tag {
  id: number;
  name: string;
  slug: string;
  post_count: number;
  created_at: string;
}

export interface Post {
  id: number;
  title: string;
  slug: string;
  content: string;
  excerpt: string;
  author: User;
  category?: Category;
  tags: Tag[];
  status: 'draft' | 'published';
  featured_image?: string;
  created_at: string;
  updated_at: string;
  published_at?: string;
  reading_time: number;
}

export interface CreatePostData {
  title: string;
  content: string;
  excerpt?: string;
  status: 'draft' | 'published';
  category_id?: number;
  tag_ids?: number[];
  featured_image?: File;
}

export interface UpdatePostData {
  title?: string;
  content?: string;
  excerpt?: string;
  status?: 'draft' | 'published';
  category_id?: number;
  tag_ids?: number[];
  featured_image?: File;
}

// API Response Types
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Form Types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'textarea' | 'select' | 'file';
  placeholder?: string;
  required?: boolean;
  validation?: {
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    message?: string;
  };
  options?: { value: string; label: string }[];
}

// UI Types
export interface ToastMessage {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export interface LoadingState {
  isLoading: boolean;
  error?: string;
}

// Navigation Types
export interface NavItem {
  label: string;
  href: string;
  icon?: React.ComponentType;
  requiresAuth?: boolean;
}
