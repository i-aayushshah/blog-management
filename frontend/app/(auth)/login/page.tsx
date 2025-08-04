import React from 'react';
import LoginForm from '@/components/auth/LoginForm';

export const metadata = {
  title: 'Login - Blog Management',
  description: 'Sign in to your account',
};

const LoginPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <LoginForm />
    </div>
  );
};

export default LoginPage;
