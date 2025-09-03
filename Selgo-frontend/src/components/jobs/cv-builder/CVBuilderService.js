


import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_JOB_API_URL || 'http://localhost:8002/api/v1';

const CVBuilderService = {
  // Build CV from form data
  buildCV: async (cvData) => {
    try {
      // Transform the data to match backend expectations
      const transformedData = {
        contact_info: cvData.contact_info ? {
          email: cvData.contact_info.email || '',
          phone: cvData.contact_info.phone || '',
          location: cvData.contact_info.location || null,
          website: cvData.contact_info.website || null,
          linkedin_url: cvData.contact_info.linkedin_url || null
        } : null,
        
        work_experience: cvData.work_experience && cvData.work_experience.experiences ? {
          experiences: cvData.work_experience.experiences.map(exp => ({
            job_title: exp.job_title || '',
            company_name: exp.company_name || '',
            company_website: exp.company_website || null,
            location: exp.location || null,
            start_date: exp.start_date ? new Date(exp.start_date).toISOString() : new Date().toISOString(),
            end_date: exp.end_date ? new Date(exp.end_date).toISOString() : null,
            is_current: exp.is_current || false,
            description: exp.description || '',
            achievements: exp.achievements || null,
            display_order: exp.display_order || 0
          }))
        } : null,
        
        education: cvData.education && cvData.education.educations ? {
          educations: cvData.education.educations.map(edu => ({
            degree: edu.degree || '',
            field_of_study: edu.field_of_study || '',
            institution: edu.institution || '',
            location: edu.location || null,
            start_date: edu.start_date ? new Date(edu.start_date).toISOString() : new Date().toISOString(),
            end_date: edu.end_date ? new Date(edu.end_date).toISOString() : null,
            is_current: edu.is_current || false,
            gpa: edu.gpa || null,
            description: edu.description || null,
            display_order: edu.display_order || 0
          }))
        } : null,
        
        languages: cvData.languages && cvData.languages.languages ? {
          languages: cvData.languages.languages.map(lang => ({
            language_id: 1, // Default language ID - in production, you'd get this from a languages API
            proficiency_level: lang.proficiency_level ? lang.proficiency_level.toLowerCase() : 'beginner'
          }))
        } : null,
        
        summary: cvData.summary ? {
          professional_summary: cvData.summary.professional_summary || ''
        } : null
      };

      console.log('Sending CV data:', transformedData);

      const response = await axios.post(`${API_URL}/cv/build`, transformedData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('accessToken') || 'mock_token'}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error building CV:', error.response?.data || error);
      throw error;
    }
  },

  // Download generated CV
  downloadCV: async (cvId) => {
    try {
      const response = await axios.get(`${API_URL}/cv/${cvId}/download`, {
        responseType: 'blob',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken') || 'mock_token'}`
        }
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
      
      return { success: true };
    } catch (error) {
      console.error('Error downloading CV:', error);
      throw error;
    }
  },

  // Upload existing CV
  uploadCV: async (file, title) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      if (title) {
        formData.append('title', title);
      }

      const response = await axios.post(`${API_URL}/cv/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Authorization': `Bearer ${localStorage.getItem('accessToken') || 'mock_token'}`
        }
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading CV:', error);
      throw error;
    }
  }
};

export default CVBuilderService;