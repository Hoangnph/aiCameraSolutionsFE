/*!

=========================================================
* Vision UI Free React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/vision-ui-free-react
* Copyright 2021 Creative Tim (https://www.creative-tim.com/)
* Licensed under MIT (https://github.com/creativetimofficial/vision-ui-free-react/blob/master LICENSE.md)

* Design and Coded by Simmmple & Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the software.

*/

import React from "react";
import { createRoot } from "react-dom/client";

// Immediate Client-Side Protection - Runs before React loads
(function() {
  const protectedPaths = ['/dashboard', '/cameras', '/analytics', '/tables', '/billing', '/profile', '/rtl'];
  const currentPath = window.location.pathname;
  
  console.log('🚨 Immediate Auth Check:', {
    currentPath,
    isProtected: protectedPaths.some(path => currentPath.startsWith(path))
  });
  
  if (protectedPaths.some(path => currentPath.startsWith(path))) {
    const token = localStorage.getItem('authToken');
    const user = localStorage.getItem('user');
    
    console.log('🚨 Immediate Auth Check - Protected Path:', {
      hasToken: !!token,
      hasUser: !!user
    });
    
    if (!token || !user) {
      console.log('🚨 Immediate Redirect: No auth, redirecting to login');
      window.location.href = '/authentication/sign-in';
      return;
    }
  }
})();

// Vision UI Dashboard React App
import App from "App";

// Soft UI Context Provider
import { VisionUIControllerProvider } from "context";

const root = createRoot(document.getElementById("root"));
root.render(
  <VisionUIControllerProvider>
    <App />
  </VisionUIControllerProvider>
);

