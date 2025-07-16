// File: selgo-frontend/services/jobService.js

import axios from 'axios';


// Replace the hardcoded URL with:
const JOB_API_URL = process.env.NEXT_PUBLIC_JOB_API_URL || 'http://localhost:8002/api/v1';

// Create axios instance with default config
const jobClient = axios.create({
  baseURL: JOB_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for authentication
jobClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor for error handling
jobClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or redirect to login
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/routes/auth/signin';
    }
    return Promise.reject(error);
  }
);

const jobService = {
  // Job Search and Listing
  searchJobs: async (searchParams) => {
    try {
      const response = await jobClient.get('/jobs/search', { params: searchParams });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getFeaturedJobs: async (limit = 10) => {
    try {
      const response = await jobClient.get('/jobs/featured', { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getRecentJobs: async (limit = 20) => {
    try {
      const response = await jobClient.get('/jobs/recent', { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getJobById: async (jobId) => {
    try {
      const response = await jobClient.get(`/jobs/${jobId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getJobBySlug: async (slug) => {
    try {
      const response = await jobClient.get(`/jobs/slug/${slug}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getSimilarJobs: async (jobId, limit = 5) => {
    try {
      const response = await jobClient.get(`/jobs/${jobId}/similar`, { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Job Recommendations
  getJobRecommendations: async (limit = 10) => {
    try {
      const response = await jobClient.get('/recommendations', { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  trackRecommendationInteraction: async (jobId, interactionType) => {
    try {
      const response = await jobClient.post(`/recommendations/${jobId}/interaction`, null, {
        params: { interaction_type: interactionType }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // User Job Preferences
  getJobPreferences: async () => {
    try {
      const response = await jobClient.get('/recommendations/preferences');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  updateJobPreferences: async (preferences) => {
    try {
      const response = await jobClient.post('/recommendations/preferences', preferences);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Job Alerts
  createJobAlert: async (alertData) => {
    try {
      const response = await jobClient.post('/job-alerts', alertData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getUserJobAlerts: async () => {
    try {
      const response = await jobClient.get('/job-alerts');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  updateJobAlert: async (alertId, alertData) => {
    try {
      const response = await jobClient.put(`/job-alerts/${alertId}`, alertData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  deleteJobAlert: async (alertId) => {
    try {
      const response = await jobClient.delete(`/job-alerts/${alertId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  toggleJobAlert: async (alertId) => {
    try {
      const response = await jobClient.post(`/job-alerts/${alertId}/toggle`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Job Actions (Save, Apply, etc.)
  saveJob: async (jobId) => {
    try {
      const response = await jobClient.post(`/jobs/${jobId}/save`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  unsaveJob: async (jobId) => {
    try {
      const response = await jobClient.delete(`/jobs/${jobId}/save`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getSavedJobs: async () => {
    try {
      const response = await jobClient.get('/jobs/saved');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getViewedJobs: async (limit = 20) => {
    try {
      const response = await jobClient.get('/jobs/viewed', { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Job Profile Management
  createOrGetProfile: async (profileData = null) => {
    try {
      const response = await jobClient.post('/profile', profileData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getProfile: async () => {
    try {
      const response = await jobClient.get('/profile');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  updateProfile: async (profileData) => {
    try {
      const response = await jobClient.put('/profile', profileData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  deleteProfile: async () => {
    try {
      const response = await jobClient.delete('/profile');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Work Experience
  addWorkExperience: async (experienceData) => {
    try {
      const response = await jobClient.post('/profile/experience', experienceData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getWorkExperiences: async () => {
    try {
      const response = await jobClient.get('/profile/experience');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  updateWorkExperience: async (experienceId, experienceData) => {
    try {
      const response = await jobClient.put(`/profile/experience/${experienceId}`, experienceData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  deleteWorkExperience: async (experienceId) => {
    try {
      const response = await jobClient.delete(`/profile/experience/${experienceId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Education
  addEducation: async (educationData) => {
    try {
      const response = await jobClient.post('/profile/education', educationData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Skills
  addSkill: async (skillName, proficiencyLevel, yearsOfExperience = null) => {
    try {
      const response = await jobClient.post('/profile/skills', {
        skill_name: skillName,
        proficiency_level: proficiencyLevel,
        years_of_experience: yearsOfExperience
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  searchSkills: async (query, limit = 10) => {
    try {
      const response = await jobClient.get('/profile/skills/search', {
        params: { q: query, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Languages
  addLanguage: async (languageName, proficiencyLevel) => {
    try {
      const response = await jobClient.post('/profile/languages', {
        language_name: languageName,
        proficiency_level: proficiencyLevel
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  searchLanguages: async (query, limit = 10) => {
    try {
      const response = await jobClient.get('/profile/languages/search', {
        params: { q: query, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // CV Management
  buildCV: async (cvBuilderData) => {
    try {
      const response = await jobClient.post('/cv/build', cvBuilderData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  generateCVFromProfile: async () => {
    try {
      const response = await jobClient.post('/cv/generate-from-profile');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  uploadCV: async (file, title = null) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (title) {
        formData.append('title', title);
      }

      const response = await jobClient.post('/cv/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getUserCVs: async () => {
    try {
      const response = await jobClient.get('/cv');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  downloadCV: async (cvId) => {
    try {
      const response = await jobClient.get(`/cv/${cvId}/download`, {
        responseType: 'blob',
      });
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cv_${cvId}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
      
      return { message: 'CV downloaded successfully' };
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  deleteCV: async (cvId) => {
    try {
      const response = await jobClient.delete(`/cv/${cvId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
  

  // Salary Comparison
  compareSalary: async (comparisonRequest) => {
    try {
      const response = await jobClient.post('/salary/compare', comparisonRequest);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  addSalaryData: async (salaryData) => {
    try {
      const response = await jobClient.post('/salary/add', salaryData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getSalaryInsights: async (jobTitle) => {
    try {
      const response = await jobClient.get(`/salary/insights/${encodeURIComponent(jobTitle)}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Articles
  getArticles: async (categoryId = null, page = 1, limit = 20) => {
    try {
      const params = { page, limit };
      if (categoryId) params.category_id = categoryId;
      
      const response = await jobClient.get('/articles', { params });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getFeaturedArticles: async (limit = 6) => {
    try {
      const response = await jobClient.get('/articles/featured', { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  searchArticles: async (query, page = 1, limit = 20) => {
    try {
      const response = await jobClient.get('/articles/search', {
        params: { q: query, page, limit }
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getArticleById: async (articleId) => {
    try {
      const response = await jobClient.get(`/articles/${articleId}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getArticleCategories: async () => {
    try {
      const response = await jobClient.get('/articles/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getPopularSearches: async () => {
    try {
      const response = await jobClient.get('/articles/popular-searches');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Analytics and Tracking
  trackJobInteraction: async (jobId, interactionType, sessionId = null, timeSpent = null) => {
    try {
      const response = await jobClient.post('/analytics/track', {
        job_id: jobId,
        interaction_type: interactionType,
        session_id: sessionId,
        time_spent: timeSpent
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getUserActivityAnalytics: async (days = 30) => {
    try {
      const response = await jobClient.get('/analytics/user/activity', { params: { days } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Job Categories
  getJobCategories: async () => {
    try {
      const response = await jobClient.get('/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Companies
  getJobsByCompany: async (companyId, limit = 10) => {
    try {
      const response = await jobClient.get(`/jobs/company/${companyId}`, { params: { limit } });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Utility Functions
  getFilterOptions: async () => {
    try {
      const response = await jobClient.get('/jobs/filter-options');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  getJobStatistics: async () => {
    try {
      const response = await jobClient.get('/jobs/statistics');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  // Company Management
getCompanies: async (params = {}) => {
  try {
    const queryParams = new URLSearchParams(params);
    const response = await jobClient.get(`/companies?${queryParams}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

getCompanyById: async (companyId, includeJobs = true) => {
  try {
    const response = await jobClient.get(`/companies/${companyId}?include_jobs=${includeJobs}`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

followCompany: async (companyId) => {
  try {
    const response = await jobClient.post(`/companies/${companyId}/follow`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

unfollowCompany: async (companyId) => {
  try {
    const response = await jobClient.delete(`/companies/${companyId}/follow`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

getFollowedCompanies: async () => {
  try {
    const response = await jobClient.get('/companies/followed/list');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Job Statistics and Filter Options
getJobStatistics: async () => {
  try {
    const response = await jobClient.get('/jobs/statistics');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

getFilterOptions: async () => {
  try {
    const response = await jobClient.get('/jobs/filter-options');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Job Feed for Homepage
getJobFeed: async (feedParams = {}) => {
  try {
    const response = await jobClient.get('/jobs/feed', { params: feedParams });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Advanced Job Management
bulkJobAction: async (jobIds, action) => {
  try {
    const response = await jobClient.post('/jobs/bulk-action', {
      job_ids: jobIds,
      action: action
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Enhanced Recommendations
getJobRecommendationsAdvanced: async (limit = 10) => {
  try {
    const response = await jobClient.get('/recommendations', { params: { limit } });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

updateJobPreferences: async (preferences) => {
  try {
    const response = await jobClient.post('/recommendations/preferences', preferences);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

trackRecommendationInteraction: async (jobId, interactionType) => {
  try {
    const response = await jobClient.post(`/recommendations/${jobId}/interaction`, null, {
      params: { interaction_type: interactionType }
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// User Activity Analytics
getUserActivityAnalytics: async (days = 30) => {
  try {
    const response = await jobClient.get('/analytics/user/activity', { params: { days } });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Track job interactions for analytics
trackJobInteraction: async (jobId, interactionType, sessionId = null, timeSpent = null) => {
  try {
    const payload = {
      job_id: jobId,
      interaction_type: interactionType
    };
    
    if (sessionId) payload.session_id = sessionId;
    if (timeSpent) payload.time_spent = timeSpent;
    
    const response = await jobClient.post('/analytics/track', payload);
    return response.data;
  } catch (error) {
    // Don't throw errors for analytics tracking
    console.warn('Failed to track job interaction:', error);
  }
},

// Enhanced Profile Methods
getProfileStrength: async () => {
  try {
    const profile = await jobService.getProfile();
    return profile.profile_completion || 0;
  } catch (error) {
    return 0;
  }
},

// CV Builder Methods
buildCVFromProfile: async (cvBuilderData) => {
  try {
    const response = await jobClient.post('/cv/build', cvBuilderData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

generateCVFromProfile: async () => {
  try {
    const response = await jobClient.post('/cv/generate-from-profile');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

downloadCV: async (cvId) => {
  try {
    const response = await jobClient.get(`/cv/${cvId}/download`, {
      responseType: 'blob',
    });
    
    // Create download link
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `cv_${cvId}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    
    return { message: 'CV downloaded successfully' };
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Enhanced Article Methods
getFeaturedArticles: async (limit = 6) => {
  try {
    const response = await jobClient.get('/articles/featured', { params: { limit } });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

getTrendingArticles: async (days = 7, limit = 10) => {
  try {
    const response = await jobClient.get('/articles/trending', { 
      params: { days, limit } 
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Session Management for Analytics
generateSessionId: () => {
  return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
},

// Track page view time
trackPageViewTime: (() => {
  let startTime = null;
  let currentJobId = null;
  
  return {
    start: (jobId) => {
      currentJobId = jobId;
      startTime = Date.now();
    },
    
    end: async () => {
      if (startTime && currentJobId) {
        const timeSpent = Math.floor((Date.now() - startTime) / 1000);
        await jobService.trackJobInteraction(
          currentJobId, 
          'page_view', 
          jobService.generateSessionId(), 
          timeSpent
        );
        startTime = null;
        currentJobId = null;
      }
    }
  };
})(),

// Helper method to check if user has viewed a job recently
hasViewedJob: async (jobId) => {
  try {
    const viewedJobs = await jobService.getViewedJobs(10);
    return viewedJobs.some(job => job.id === jobId);
  } catch (error) {
    return false;
  }
},

// Helper method to get job application status
getJobApplicationStatus: async (jobId) => {
  try {
    // This would need to be implemented in backend
    const response = await jobClient.get(`/jobs/${jobId}/application-status`);
    return response.data;
  } catch (error) {
    return { applied: false, status: null };
  }
},

// Helper method for job recommendations with reasons
getJobRecommendationsWithReasons: async (limit = 10) => {
  try {
    const recommendations = await jobService.getJobRecommendationsAdvanced(limit);
    
    // Track that recommendations were viewed
    recommendations.forEach(rec => {
      jobService.trackJobInteraction(rec.job_id, 'recommendation_view');
    });
    
    return recommendations;
  } catch (error) {
    // Fallback to regular job search
    return await jobService.getRecentJobs(limit);
  }
},


// Get profile dashboard with salary data
getProfileDashboard: async () => {
  try {
    const response = await jobClient.get('/profile/dashboard');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Get salary comparison for current profile
getProfileSalaryComparison: async () => {
  try {
    const response = await jobClient.get('/profile/salary-comparison');
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

// Quick profile creation with work experience
createQuickProfile: async (profileData) => {
  try {
    const response = await jobClient.post('/profile', profileData);
    return response.data;
  } catch (error) {
    throw error.response?.data || error;
  }
},

};



export default jobService;