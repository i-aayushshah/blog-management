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
  resendVerification: (email: string) => Promise<boolean>;
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

          console.log('🔐 Login successful, user data:', user);

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
          // Re-throw the error so the component can handle it
          throw error;
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
        console.log('🔐 Logout called, clearing user data');

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

      // Resend verification email action
      resendVerification: async (email: string) => {
        set({ isLoading: true });

        try {
          await authAPI.resendVerification({ email });

          set({ isLoading: false });
          toast.success('Verification email sent successfully!');
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
          await authAPI.resetPassword({
            token,
            password: newPassword,
            password_confirm: newPassword
          });

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
                } catch (error: any) {
          console.log('⚠️ Auth check failed, but preserving user data:', error);
          console.log('🔍 Current user state before error:', get().user);

          // Don't clear user data immediately on auth check failure
          // Only clear if it's a persistent auth issue
          set({
            isAuthenticated: false,
            isLoading: false,
          });

          // Only clear token and user if it's a 401/403 error
          if (error.response?.status === 401 || error.response?.status === 403) {
            console.log('🔐 Clearing auth due to 401/403 error');
            set({
              user: null,
              token: null,
              isAuthenticated: false,
              isLoading: false,
            });
            removeAuthToken();
          } else {
            // For other errors, keep the user data but mark as not authenticated
            console.log('⚠️ Keeping user data for non-auth errors');
          }

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
        console.log('🔐 clearAuth called, clearing all auth data');
        removeAuthToken();
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        });
      },

      // Debug function to log current state
      debugState: () => {
        const state = get();
        console.log('🔍 Auth Store State:', {
          user: state.user,
          token: state.token ? '***' : null,
          isAuthenticated: state.isAuthenticated,
          isLoading: state.isLoading,
        });
      },

      // Check persisted data
      checkPersistedData: () => {
        if (typeof window !== 'undefined') {
          const persisted = localStorage.getItem('blog-auth-storage');
          console.log('🔍 Persisted auth data:', persisted);
          if (persisted) {
            try {
              const parsed = JSON.parse(persisted);
              console.log('🔍 Parsed persisted data:', parsed);
            } catch (e) {
              console.error('❌ Error parsing persisted data:', e);
            }
          }
        }
      },

      // Restore user data from token
      restoreUserFromToken: async () => {
        const { token, user } = get();

        // If we have a token but no user data, fetch the user data
        if (token && !user) {
          console.log('🔍 Restoring user data from token...');
          try {
            const response = await authAPI.checkAuth();
            const { user: userData } = response.data;

            set({
              user: userData,
              isAuthenticated: true,
            });

            console.log('✅ User data restored:', userData);
            return true;
          } catch (error) {
            console.error('❌ Failed to restore user data:', error);
            // Clear invalid token
            set({
              user: null,
              token: null,
              isAuthenticated: false,
            });
            removeAuthToken();
            return false;
          }
        }
        return true;
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
