import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoadingSpinner from './LoadingSpinner';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  const [authChecked, setAuthChecked] = useState(false);

  console.log('🔒 ProtectedRoute:', {
    isAuthenticated,
    isLoading,
    pathname: location.pathname,
    authChecked
  });

  useEffect(() => {
    // Only check once when authentication status is determined
    if (!isLoading) {
      setAuthChecked(true);
    }
  }, [isLoading]);

  // Show loading only briefly while checking
  if (isLoading || !authChecked) {
    console.log('🔒 ProtectedRoute: Loading state');
    return <LoadingSpinner />;
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    console.log('🔒 ProtectedRoute: Redirecting to login');
    return (
      <Navigate
        to="/authentication/sign-in"
        state={{ from: location }}
        replace
      />
    );
  }

  // Render protected content
  console.log('🔒 ProtectedRoute: Rendering protected content');
  return <>{children}</>;
};

export default ProtectedRoute; 