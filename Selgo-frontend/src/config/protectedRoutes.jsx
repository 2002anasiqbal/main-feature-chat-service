// // List of routes that require authentication
// const protectedRoutes = [
//     "/routes/create-ad/*",
//     "/routes/messages",

//     "/routes/notifications",
    
// ];

// export default protectedRoutes;

// config/protectedRoutes.js

// Routes that require authentication
const protectedRoutes = [
  // Create ad routes - ALL motorcycle ad creation requires login
  '/routes/create-ad',
  '/routes/create-ad/*',
  '/routes/motor-cycle/create-ad',
  '/routes/motor-cycle/create-ad/*', // This protects all category-specific create pages
  '/routes/boat/create-ad',
  '/routes/boat/create-ad/*',
  
  // Edit routes  
  '/routes/motor-cycle/edit/*',
  '/routes/boat/edit/*',
  
  // User profile and account
  '/routes/profile',
  '/routes/profile/*',
  '/routes/account',
  '/routes/account/*',
  '/routes/my-ads',
  '/routes/my-ads/*',
  
  // Messaging
  '/routes/messages',
  '/routes/messages/*',
  
  // Favorites/Saved items
  '/routes/favorites',
  '/routes/saved',
  
  // Admin routes (if applicable)
  '/routes/admin',
  '/routes/admin/*',
  
  // Any other protected routes
  '/routes/dashboard',
  '/routes/settings',
];

// Routes that should redirect authenticated users away (like login/signup)
const guestOnlyRoutes = [
  '/routes/auth/signin',
  '/routes/auth/signup',
  '/routes/auth/forgot-password',
  '/routes/auth/reset-password'
];

// Public routes (no authentication required)
const publicRoutes = [
  '/',
  '/routes/boat',
  '/routes/boat/*',
  '/routes/motor-cycle',
  '/routes/motor-cycle/*',
  '/routes/job',
  '/routes/job/*',
  '/routes/property',
  '/routes/property/*',
  '/routes/about',
  '/routes/contact',
  '/routes/help',
  '/routes/terms',
  '/routes/privacy'
];

export default protectedRoutes;
export { guestOnlyRoutes, publicRoutes };