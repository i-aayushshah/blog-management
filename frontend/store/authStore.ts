import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, LoginCredentials, RegisterCredentials, AuthResponse } from '@/types';
import { authAPI, setAuthToken, removeAuthToken } from '@/lib/api';
import { toast } from 'react-hot-toast';

interface AuthState {
  // State
  user: User | null;
  token: string | null;
  isLoading: boolean;
  isAuthenticated: boolean;

  // Actions
  login: (credentials: LoginCredentials) => Promise<boolean>;
  register: (credentials: RegisterCredentials) => Promise<boolean>;
  logout: () => void;
  verifyEmail: (token: string) => Promise<boolean>;
  forgotPassword: (email: string) => Promise<boolean>;
  resetPassword: (token: string, newPassword: string) => Promise<boolean>;
  updateProfile: (data: Partial<User>) => Promise<boolean>;
  checkAuth: () => Promise<boolean>;
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial state
      user: null,
      token: null,
      isLoading: false,
      isAuthenticated: false,

      // Login action
      login: async (credentials: LoginCredentials) => {
        set({ isLoading: true });

        try {
          const response = await authAPI.login(credentials);
          const { token, user } = response.data;

          // Store token
          setAuthToken(token);

          // Update state
          set({
            user,
            token,
            isAuthenticated: true,
            isLoading: false,
          });

          toast.success('Login successful!');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Register action
      register: async (credentials: RegisterCredentials) => {
        set({ isLoading: true });

        try {
          const response = await authAPI.register(credentials);

          set({ isLoading: false });
          toast.success('Registration successful! Please check your email for verification.');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Logout action
      logout: async () => {
        try {
          await authAPI.logout();
        } catch (error) {
          // Continue with logout even if API call fails
        }

        // Clear token
        removeAuthToken();

        // Clear state
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });

        toast.success('Logged out successfully');
      },

      // Verify email action
      verifyEmail: async (token: string) => {
        set({ isLoading: true });

        try {
          await authAPI.verifyEmail({ token });

          set({ isLoading: false });
          toast.success('Email verified successfully! You can now login.');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Forgot password action
      forgotPassword: async (email: string) => {
        set({ isLoading: true });

        try {
          await authAPI.forgotPassword({ email });

          set({ isLoading: false });
          toast.success('Password reset email sent successfully!');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Reset password action
      resetPassword: async (token: string, newPassword: string) => {
        set({ isLoading: true });

        try {
          await authAPI.resetPassword({ token, new_password: newPassword });

          set({ isLoading: false });
          toast.success('Password reset successfully! You can now login with your new password.');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Update profile action
      updateProfile: async (data: Partial<User>) => {
        set({ isLoading: true });

        try {
          const response = await authAPI.updateProfile(data);
          const updatedUser = response.data;

          set({
            user: updatedUser,
            isLoading: false,
          });

          toast.success('Profile updated successfully!');
          return true;
        } catch (error) {
          set({ isLoading: false });
          return false;
        }
      },

      // Check authentication status
      checkAuth: async () => {
        const { token } = get();

        if (!token) {
          set({ isAuthenticated: false });
          return false;
        }

        set({ isLoading: true });

        try {
          const response = await authAPI.checkAuth();
          const { user } = response.data;

          set({
            user,
            isAuthenticated: true,
            isLoading: false,
          });

          return true;
        } catch (error) {
          set({
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
          });

          removeAuthToken();
          return false;
        }
      },

      // Set user
      setUser: (user: User) => {
        set({ user });
      },

      // Set token
      setToken: (token: string) => {
        setAuthToken(token);
        set({ token, isAuthenticated: true });
      },

      // Clear authentication
      clearAuth: () => {
        removeAuthToken();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },
    }),
    {
      name: 'blog-auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
