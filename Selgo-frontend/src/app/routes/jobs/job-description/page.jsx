import React from 'react';
import JobDescriptionMain from '@/components/jobs/job-discription/JobDiscriptionMain';
// App.js or your route component
const JobDescriptionPage = () => {
  // When you're ready to use real data, you can pass it like this:
  // const customJobData = { ... your data from wherever ... };
  // return <JobDescriptionPage jobData={customJobData} />;
  
  // For now, using the default placeholder data:
  return <JobDescriptionMain />;
};

export default JobDescriptionPage;