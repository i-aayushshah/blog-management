'use client';

import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Mail, RefreshCw } from 'lucide-react';
import { useAuthStore } from '@/store/authStore';
import { isValidEmail } from '@/lib/utils';
import Button from '@/components/ui/Button';
import Input from '@/components/ui/Input';

interface ResendVerificationData {
  email: string;
}

const ResendVerificationForm: React.FC = () => {
  const [isSent, setIsSent] = useState(false);
  const resendVerification = useAuthStore((state) => state.resendVerification);
  const isLoading = useAuthStore((state) => state.isLoading);

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
  } = useForm<ResendVerificationData>();

  const email = watch('email');

  const onSubmit = async (data: ResendVerificationData) => {
    const success = await resendVerification(data.email);
    if (success) {
      setIsSent(true);
    }
  };

  if (isSent) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-4 text-center">
        <div className="flex items-center justify-center mb-2">
          <Mail className="h-5 w-5 text-green-500 mr-2" />
          <span className="text-sm font-medium text-green-800">
            Email Sent Successfully!
          </span>
        </div>
        <p className="text-sm text-green-700 mb-3">
          We've sent a new verification email to <strong>{email}</strong>
        </p>
        <Button
          variant="outline"
          size="sm"
          onClick={() => setIsSent(false)}
          className="text-green-600 border-green-300 hover:bg-green-50"
        >
          Send Another Email
        </Button>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <Input
          label="Email Address"
          type="email"
          placeholder="Enter your email address"
          icon={<Mail className="h-4 w-4" />}
          error={errors.email?.message}
          {...register('email', {
            required: 'Email is required',
            validate: (value) => isValidEmail(value) || 'Please enter a valid email',
          })}
        />
      </div>

      <Button
        type="submit"
        className="w-full"
        loading={isLoading}
        disabled={isLoading}
      >
        <RefreshCw className="h-4 w-4 mr-2" />
        Resend Verification Email
      </Button>
    </form>
  );
};

export default ResendVerificationForm;
