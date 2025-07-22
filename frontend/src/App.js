import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "assets/theme";

// Protected Route component
import ProtectedRoute from "components/ProtectedRoute";

// Loading Spinner component
import LoadingSpinner from "components/LoadingSpinner";

// Authentication layouts
import SignIn from "layouts/authentication/sign-in";
import SignUp from "layouts/authentication/sign-up";

// Import ForgotPassword component
import ForgotPassword from "layouts/authentication/forgot-password";

// Import ResetPassword component
import ResetPassword from "layouts/authentication/reset-password";

// Import ChangePassword component
import ChangePassword from "layouts/authentication/change-password";

// Test component
import TestAuth from "components/TestAuth";

// Debug component
import DebugRoute from "components/DebugRoute";

// Debug Protected Route component
import DebugProtectedRoute from "components/DebugProtectedRoute";

// AI Camera Counting System layouts
import Cameras from "layouts/cameras";
import Analytics from "layouts/analytics";
import CameraDetail from "layouts/camera-detail";

// Vision UI Dashboard React layouts
import Dashboard from "layouts/dashboard";
import Tables from "layouts/tables";
import Billing from "layouts/billing";
import RTL from "layouts/rtl";
import Profile from "layouts/profile";

// Vision UI Dashboard React components
import Sidenav from "examples/Sidenav";

// Vision UI Dashboard React example components
import PageLayout from "examples/LayoutContainers/PageLayout";

// Routes
import routes from "routes";

// Auth context
import { AuthProvider, useAuth } from "contexts/AuthContext";

// Component to conditionally render layout
function AppLayout({ children }) {
  const location = useLocation();
  const { isAuthenticated, isLoading } = useAuth();
  
  // Check if current path is authentication page
  const isAuthPage = location.pathname.includes('/authentication/') || 
                     location.pathname === '/test-auth' ||
                     location.pathname === '/debug-route' ||
                     location.pathname === '/debug-protected';
  
  // Check if current path is public page (not authenticated)
  const isPublicPage = location.pathname === '/' || isAuthPage;
  
  // If it's a public page, render without Sidenav
  if (isPublicPage) {
    return (
      <PageLayout>
        {children}
      </PageLayout>
    );
  }
  
  // If it's a protected page and user is authenticated, render with Sidenav
  if (isAuthenticated) {
    return (
      <PageLayout>
        <Sidenav
          color="info"
          brandName="Vision UI Dashboard"
          routes={routes}
        />
        {children}
      </PageLayout>
    );
  }
  
  // If user is not authenticated on protected page, let ProtectedRoute handle it
  // This prevents infinite loading by not showing loading spinner here
  return (
    <PageLayout>
      {children}
    </PageLayout>
  );
}

function AppContent() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AuthProvider>
          <AppLayout>
            <Routes>
            {/* Public routes */}
            <Route path="/authentication/sign-in" element={<SignIn />} />
            <Route path="/authentication/sign-up" element={<SignUp />} />
            <Route path="/authentication/forgot-password" element={<ForgotPassword />} />
            <Route path="/authentication/reset-password" element={<ResetPassword />} />
            <Route path="/authentication/change-password" element={<ChangePassword />} />
            <Route path="/test-auth" element={<TestAuth />} />
            <Route path="/debug-route" element={<DebugRoute />} />
            <Route path="/debug-protected" element={
              <DebugProtectedRoute>
                <div>This is protected content</div>
              </DebugProtectedRoute>
            } />
            
            {/* Protected routes - Using comprehensive ProtectedRoute */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/cameras" element={
              <ProtectedRoute>
                <Cameras />
              </ProtectedRoute>
            } />
            <Route path="/analytics" element={
              <ProtectedRoute>
                <Analytics />
              </ProtectedRoute>
            } />
            <Route path="/tables" element={
              <ProtectedRoute>
                <Tables />
              </ProtectedRoute>
            } />
            <Route path="/billing" element={
              <ProtectedRoute>
                <Billing />
              </ProtectedRoute>
            } />
            <Route path="/rtl" element={
              <ProtectedRoute>
                <RTL />
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute>
                <Profile />
              </ProtectedRoute>
            } />
            <Route path="/cameras/:id" element={
              <ProtectedRoute>
                <CameraDetail />
              </ProtectedRoute>
            } />
            
            {/* Default redirects */}
            <Route path="/" element={<Navigate to="/authentication/sign-in" replace />} />
            <Route path="*" element={<Navigate to="/authentication/sign-in" replace />} />
          </Routes>
          </AppLayout>
        </AuthProvider>
      </Router>
    </ThemeProvider>
  );
}

export default AppContent;
