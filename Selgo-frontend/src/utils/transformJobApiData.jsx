// Utility function to transform API response data into the format expected by the component
export const transformJobApiData = (apiData) => {
    // This function would transform whatever structure comes from your API
    // into the structure expected by the JobDescriptionPage component
    
    return {
      title: apiData.jobTitle || 'No title',
      company: apiData.companyName || '',
      deadline: apiData.applicationDeadline || 'No deadline specified',
      employmentType: apiData.employmentType || 'Not specified',
      description: apiData.shortDescription || '',
      mainDescription: Array.isArray(apiData.fullDescription) 
        ? apiData.fullDescription 
        : apiData.fullDescription?.split('\n\n') || [],
      tasks: Array.isArray(apiData.responsibilities) 
        ? apiData.responsibilities 
        : apiData.responsibilities?.split('\n').map(item => item.trim().replace(/^[-•]/, '').trim()) || [],
      qualifications: Array.isArray(apiData.qualifications) 
        ? apiData.qualifications 
        : apiData.qualifications?.split('\n').map(item => item.trim().replace(/^[-•]/, '').trim()) || [],
      personalCharacteristics: Array.isArray(apiData.characteristics) 
        ? apiData.characteristics 
        : apiData.characteristics?.split('\n').map(item => item.trim().replace(/^[-•]/, '').trim()) || [],
      whyCompany: Array.isArray(apiData.whyJoinUs) 
        ? apiData.whyJoinUs 
        : apiData.whyJoinUs?.split('\n\n') || [],
      aboutEmployer: Array.isArray(apiData.aboutCompany) 
        ? apiData.aboutCompany 
        : apiData.aboutCompany?.split('\n\n') || [],
      networks: apiData.socialMedia || [],
      sector: apiData.industrySector || 'Not specified',
      companyRepresentative: apiData.representativeInfo || '',
      keywords: apiData.jobTags || [],
      finnCode: apiData.referenceCode || '',
      lastModified: apiData.lastUpdated || '',
      contact: {
        person: apiData.contactPerson || '',
        telephone: apiData.contactPhone || ''
      }
    };
  };
  
  // Example usage:
  // import { transformJobApiData } from './utils/jobDataTransformer';
  // 
  // const fetchAndTransformJobData = async (jobId) => {
  //   const apiResponse = await fetch(`/api/jobs/${jobId}`);
  //   const apiData = await apiResponse.json();
  //   return transformJobApiData(apiData);
  // };