'use client';

import React, { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import { CheckCircle, XCircle, Loader2 } from 'lucide-react';
import Button from '@/components/ui/Button';
import toast from 'react-hot-toast';

const VerifyEmailTokenPage: React.FC = () => {
  const [isVerifying, setIsVerifying] = useState(true);
  const [isSuccess, setIsSuccess] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();
  const params = useParams();

  useEffect(() => {
    const verifyToken = async () => {
      const token = params.token as string;

      if (!token) {
        setError('Invalid verification link');
        setIsVerifying(false);
        return;
      }

      try {
        // Call the API directly instead of using the auth store to avoid double verification
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/verify-email/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token }),
        });

        if (response.ok) {
          // Show success toast
          toast.success('Email verified successfully! You can now sign in to your account.');
          // Redirect immediately to login page with success message
          router.push('/login?verified=true');
        } else {
          const errorData = await response.json();
          setError(errorData.error || 'Verification failed. The link may be expired or invalid.');
        }
      } catch (err: any) {
        setError('Verification failed. Please try again.');
      } finally {
        setIsVerifying(false);
      }
    };

    verifyToken();
  }, [params.token, router]);

  if (isVerifying) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white shadow-lg rounded-lg p-8 text-center">
            <div className="mb-6">
              <Loader2 className="h-16 w-16 text-blue-500 mx-auto animate-spin" />
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Verifying Your Email
            </h1>

            <p className="text-gray-600">
              Please wait while we verify your email address...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="w-full max-w-md mx-auto">
          <div className="bg-white shadow-lg rounded-lg p-8 text-center">
            <div className="mb-6">
              <CheckCircle className="h-16 w-16 text-green-500 mx-auto" />
            </div>

            <h1 className="text-2xl font-bold text-gray-900 mb-4">
              Email Verified Successfully!
            </h1>

            <p className="text-gray-600 mb-6">
              Your email address has been verified. You can now sign in to your account.
            </p>

            <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
              <div className="flex items-center">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                <span className="text-sm text-green-700">
                  Redirecting to login page in 3 seconds...
                </span>
              </div>
            </div>

            <div className="space-y-3">
              <Link href="/login">
                <Button className="w-full">
                  Sign In Now
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white shadow-lg rounded-lg p-8 text-center">
          <div className="mb-6">
            <XCircle className="h-16 w-16 text-red-500 mx-auto" />
          </div>

          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Verification Failed
          </h1>

          <p className="text-gray-600 mb-6">
            {error}
          </p>

          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <XCircle className="h-5 w-5 text-red-500 mr-2" />
              <span className="text-sm text-red-700">
                The verification link may be expired or invalid.
              </span>
            </div>
          </div>

          <div className="space-y-3">
            <Link href="/verify-email">
              <Button className="w-full">
                Try Again
              </Button>
            </Link>

            <Link href="/login">
              <Button variant="outline" className="w-full">
                Back to Login
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmailTokenPage;
