import React from 'react';
import SimpleProtectedRoute from './SimpleProtectedRoute';

// Import all components
import Dashboard from "layouts/dashboard";
import Cameras from "layouts/cameras";
import Analytics from "layouts/analytics";
import Tables from "layouts/tables";
import Billing from "layouts/billing";
import RTL from "layouts/rtl";
import Profile from "layouts/profile";
import CameraDetail from "layouts/camera-detail";

// Protected Dashboard
export const ProtectedDashboard = (props) => (
  <SimpleProtectedRoute>
    <Dashboard {...props} />
  </SimpleProtectedRoute>
);

// Protected Cameras
export const ProtectedCameras = (props) => (
  <SimpleProtectedRoute>
    <Cameras {...props} />
  </SimpleProtectedRoute>
);

// Protected Analytics
export const ProtectedAnalytics = (props) => (
  <SimpleProtectedRoute>
    <Analytics {...props} />
  </SimpleProtectedRoute>
);

// Protected Tables
export const ProtectedTables = (props) => (
  <SimpleProtectedRoute>
    <Tables {...props} />
  </SimpleProtectedRoute>
);

// Protected Billing
export const ProtectedBilling = (props) => (
  <SimpleProtectedRoute>
    <Billing {...props} />
  </SimpleProtectedRoute>
);

// Protected RTL
export const ProtectedRTL = (props) => (
  <SimpleProtectedRoute>
    <RTL {...props} />
  </SimpleProtectedRoute>
);

// Protected Profile
export const ProtectedProfile = (props) => (
  <SimpleProtectedRoute>
    <Profile {...props} />
  </SimpleProtectedRoute>
);

// Protected Camera Detail
export const ProtectedCameraDetail = (props) => (
  <SimpleProtectedRoute>
    <CameraDetail {...props} />
  </SimpleProtectedRoute>
); 