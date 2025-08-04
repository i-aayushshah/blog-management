'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { Eye, EyeOff, Mail, Lock, AlertCircle, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { LoginCredentials } from '@/types';
import { isValidEmail } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

const LoginForm: React.FC = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [showResendVerification, setShowResendVerification] = useState(false);
  const [unverifiedEmail, setUnverifiedEmail] = useState('');
  const [showResendSection, setShowResendSection] = useState(false);
  const [resendEmail, setResendEmail] = useState('');
  const router = useRouter();
  const login = useAuthStore((state) => state.login);
  const resendVerification = useAuthStore((state) => state.resendVerification);

  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
  } = useForm<LoginCredentials>();

  const onSubmit = async (data: LoginCredentials) => {
    setIsLoading(true);

    try {
      const success = await login(data);
      if (success) {
        router.push('/');
      }
    } catch (error: any) {
      // Check if the error is due to unverified email
      if (error?.response?.data?.error?.includes('verify your email')) {
        setUnverifiedEmail(data.email);
        setShowResendVerification(true);
        setError('root', {
          type: 'manual',
          message: 'Please verify your email before logging in. You can request a new verification email below.',
        });
      } else {
        setError('root', {
          type: 'manual',
          message: 'Invalid email or password',
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendVerification = async () => {
    if (!unverifiedEmail) return;

    setIsLoading(true);
    try {
      const success = await resendVerification(unverifiedEmail);
      if (success) {
        // Show success message and hide the resend section after a delay
        setTimeout(() => {
          setShowResendVerification(false);
        }, 3000);
      }
    } catch (error) {
      // Error handling is done in the store
    } finally {
      setIsLoading(false);
    }
  };

  const handleResendVerificationFromSection = async () => {
    if (!resendEmail) return;

    setIsLoading(true);
    try {
      const success = await resendVerification(resendEmail);
      if (success) {
        // Show success message and hide the resend section after a delay
        setTimeout(() => {
          setShowResendSection(false);
          setResendEmail('');
        }, 3000);
      }
    } catch (error) {
      // Error handling is done in the store
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white shadow-lg rounded-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-600 mt-2">Sign in to your account</p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div>
            <Input
              label="Email"
              type="email"
              placeholder="Enter your email"
              icon={<Mail className="h-4 w-4" />}
              error={errors.email?.message}
              {...register('email', {
                required: 'Email is required',
                validate: (value) => isValidEmail(value) || 'Please enter a valid email',
              })}
            />
          </div>

          <div>
            <div className="relative">
              <Input
                label="Password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                icon={<Lock className="h-4 w-4" />}
                error={errors.password?.message}
                {...register('password', {
                  required: 'Password is required',
                  minLength: {
                    value: 8,
                    message: 'Password must be at least 8 characters',
                  },
                })}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? (
                  <EyeOff className="h-4 w-4" />
                ) : (
                  <Eye className="h-4 w-4" />
                )}
              </button>
            </div>
          </div>

          {errors.root && (
            <div className="text-sm text-red-600 text-center">
              {errors.root.message}
            </div>
          )}

          {showResendVerification && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <div className="flex items-start">
                <AlertCircle className="h-5 w-5 text-yellow-500 mr-2 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <h3 className="text-sm font-medium text-yellow-800 mb-2">
                    Email Not Verified
                  </h3>
                  <p className="text-sm text-yellow-700 mb-3">
                    Your email address <strong>{unverifiedEmail}</strong> has not been verified yet.
                    {unverifiedEmail && (
                      <>
                        <br />
                        <span className="text-xs text-yellow-600">
                          💡 If you registered a while ago, your verification link may have expired.
                          You can request a new verification email below.
                        </span>
                      </>
                    )}
                  </p>
                  <div className="flex space-x-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      onClick={handleResendVerification}
                      loading={isLoading}
                      disabled={isLoading}
                      className="text-yellow-700 border-yellow-300 hover:bg-yellow-100"
                    >
                      <RefreshCw className="h-4 w-4 mr-1" />
                      Resend Verification Email
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setShowResendVerification(false)}
                      className="text-yellow-600 hover:text-yellow-700"
                    >
                      Dismiss
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}

          <Button
            type="submit"
            className="w-full"
            loading={isLoading}
            disabled={isLoading}
          >
            Sign In
          </Button>
        </form>

        {/* Resend Verification Section */}
        <div className="mt-6 border-t pt-6">
          <button
            type="button"
            onClick={() => setShowResendSection(!showResendSection)}
            className="w-full flex items-center justify-between text-sm text-gray-600 hover:text-gray-800 transition-colors"
          >
            <span>Need to resend verification email?</span>
            {showResendSection ? (
              <ChevronUp className="h-4 w-4" />
            ) : (
              <ChevronDown className="h-4 w-4" />
            )}
          </button>

          {showResendSection && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-medium text-gray-900 mb-3">
                Resend Verification Email
              </h3>
              <p className="text-xs text-gray-600 mb-3">
                Enter your email address to receive a new verification link.
              </p>
              <div className="space-y-3">
                <Input
                  label="Email"
                  type="email"
                  placeholder="Enter your email address"
                  icon={<Mail className="h-4 w-4" />}
                  value={resendEmail}
                  onChange={(e) => setResendEmail(e.target.value)}
                />
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleResendVerificationFromSection}
                  loading={isLoading}
                  disabled={isLoading || !resendEmail}
                  className="w-full"
                >
                  <RefreshCw className="h-4 w-4 mr-1" />
                  Send Verification Email
                </Button>
              </div>
            </div>
          )}
        </div>

        <div className="mt-6 text-center space-y-2">
          <Link
            href="/forgot-password"
            className="text-sm text-blue-600 hover:text-blue-500 block"
          >
            Forgot your password?
          </Link>

          <Link
            href="/verify-email"
            className="text-sm text-blue-600 hover:text-blue-500 block"
          >
            Need to verify your email?
          </Link>
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Don&apos;t have an account?{' '}
            <Link
              href="/register"
              className="text-blue-600 hover:text-blue-500 font-medium"
            >
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
