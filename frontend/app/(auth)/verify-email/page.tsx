import React from 'react';
import Link from 'next/link';
import { Mail, CheckCircle } from 'lucide-react';
import Button from '@/components/ui/Button';

export const metadata = {
  title: 'Verify Email - Blog Management',
  description: 'Verify your email address',
};

const VerifyEmailPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md mx-auto">
        <div className="bg-white shadow-lg rounded-lg p-8 text-center">
          <div className="mb-6">
            <Mail className="h-16 w-16 text-blue-500 mx-auto" />
          </div>
          
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Check Your Email
          </h1>
          
          <p className="text-gray-600 mb-6">
            We&apos;ve sent a verification link to your email address. 
            Please check your inbox and click the link to verify your account.
          </p>
          
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-blue-500 mr-2" />
              <span className="text-sm text-blue-700">
                Don&apos;t see the email? Check your spam folder.
              </span>
            </div>
          </div>
          
          <div className="space-y-3">
            <Link href="/login">
              <Button className="w-full">
                Back to Login
              </Button>
            </Link>
            
            <p className="text-sm text-gray-500">
              Already verified?{' '}
              <Link href="/login" className="text-blue-600 hover:text-blue-500 font-medium">
                Sign in here
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default VerifyEmailPage; 