'use client';

import React, { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';
import { CheckCircle } from 'lucide-react';
import LoginForm from '@/components/auth/LoginForm';

const LoginPage: React.FC = () => {
  const [showVerificationSuccess, setShowVerificationSuccess] = useState(false);
  const searchParams = useSearchParams();

  useEffect(() => {
    const verified = searchParams.get('verified');
    if (verified === 'true') {
      setShowVerificationSuccess(true);
      // Hide the message after 5 seconds
      setTimeout(() => {
        setShowVerificationSuccess(false);
      }, 5000);
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md mx-auto">
        {showVerificationSuccess && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 text-center">
            <div className="flex items-center justify-center mb-2">
              <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
              <span className="text-sm font-medium text-green-800">
                Email Verified Successfully!
              </span>
            </div>
            <p className="text-sm text-green-700">
              Your email has been verified. You can now sign in to your account.
            </p>
          </div>
        )}
        <LoginForm />
      </div>
    </div>
  );
};

export default LoginPage;
