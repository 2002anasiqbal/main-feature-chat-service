"use client";
import { useState } from 'react';

const CVBuilder = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    contactInfo: {
      email: '',
      phone: ''
    },
    workExperience: [],
    education: [],
    languages: [],
    summary: ''
  });

  // Handle contact info changes
  const handleContactInfoChange = (field, value) => {
    setFormData({
      ...formData,
      contactInfo: {
        ...formData.contactInfo,
        [field]: value
      }
    });
  };

  // Add work experience
  const addWorkExperience = () => {
    const newWorkExperience = {
      id: Date.now(),
      company: '',
      position: '',
      startDate: '',
      endDate: '',
      description: ''
    };
    setFormData({
      ...formData,
      workExperience: [...formData.workExperience, newWorkExperience]
    });
  };

  // Update work experience
  const updateWorkExperience = (id, field, value) => {
    const updatedWorkExperience = formData.workExperience.map(exp => 
      exp.id === id ? { ...exp, [field]: value } : exp
    );
    setFormData({
      ...formData,
      workExperience: updatedWorkExperience
    });
  };

  // Remove work experience
  const removeWorkExperience = (id) => {
    const filteredWorkExperience = formData.workExperience.filter(exp => exp.id !== id);
    setFormData({
      ...formData,
      workExperience: filteredWorkExperience
    });
  };

  // Add education
  const addEducation = () => {
    const newEducation = {
      id: Date.now(),
      institution: '',
      degree: '',
      field: '',
      startDate: '',
      endDate: ''
    };
    setFormData({
      ...formData,
      education: [...formData.education, newEducation]
    });
  };

  // Update education
  const updateEducation = (id, field, value) => {
    const updatedEducation = formData.education.map(edu => 
      edu.id === id ? { ...edu, [field]: value } : edu
    );
    setFormData({
      ...formData,
      education: updatedEducation
    });
  };

  // Remove education
  const removeEducation = (id) => {
    const filteredEducation = formData.education.filter(edu => edu.id !== id);
    setFormData({
      ...formData,
      education: filteredEducation
    });
  };

  // Add language
  const addLanguage = () => {
    const newLanguage = {
      id: Date.now(),
      name: '',
      proficiency: 'Beginner'
    };
    setFormData({
      ...formData,
      languages: [...formData.languages, newLanguage]
    });
  };

  // Update language
  const updateLanguage = (id, field, value) => {
    const updatedLanguages = formData.languages.map(lang => 
      lang.id === id ? { ...lang, [field]: value } : lang
    );
    setFormData({
      ...formData,
      languages: updatedLanguages
    });
  };

  // Remove language
  const removeLanguage = (id) => {
    const filteredLanguages = formData.languages.filter(lang => lang.id !== id);
    setFormData({
      ...formData,
      languages: filteredLanguages
    });
  };

  // Update summary
  const updateSummary = (value) => {
    setFormData({
      ...formData,
      summary: value
    });
  };

  // Navigate to next step
  const nextStep = () => {
    if (currentStep < 5) {
      setCurrentStep(currentStep + 1);
    }
  };

  // Navigate to previous step
  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  // Create CV
  const createCV = () => {
    console.log('CV Data:', formData);
    alert('CV created successfully!');
    // In a real app, this would generate a PDF or similar
  };

  // Render the appropriate step
  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <div className="p-6 w-full bg-white rounded-lg shadow-sm text-gray-800">
            <h2 className="text-xl font-semibold mb-4 w-full">Contact Information</h2>
            <div className="space-y-4 w-full">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.contactInfo.email}
                  onChange={(e) => handleContactInfoChange('email', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  placeholder="example@email.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input
                  type="tel"
                  value={formData.contactInfo.phone}
                  onChange={(e) => handleContactInfoChange('phone', e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-md"
                  placeholder="+1 (123) 456-7890"
                />
              </div>
              <div className="flex justify-end mt-4">
                <button 
                  onClick={nextStep}
                  className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        );
      case 2:
        return (
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Work Experience</h2>
            <p className="text-gray-600 mb-4">You are almost there! When did you start? Add a date to be able to use the Job profile as a CV.</p>
            
            {formData.workExperience.map((exp) => (
              <div key={exp.id} className="mb-6 p-4 border border-gray-200 rounded-md">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-medium">Work Experience</h3>
                  <button 
                    onClick={() => removeWorkExperience(exp.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                    <input
                      type="text"
                      value={exp.company}
                      onChange={(e) => updateWorkExperience(exp.id, 'company', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
                    <input
                      type="text"
                      value={exp.position}
                      onChange={(e) => updateWorkExperience(exp.id, 'position', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                    <input
                      type="date"
                      value={exp.startDate}
                      onChange={(e) => updateWorkExperience(exp.id, 'startDate', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input
                      type="date"
                      value={exp.endDate}
                      onChange={(e) => updateWorkExperience(exp.id, 'endDate', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                    <textarea
                      value={exp.description}
                      onChange={(e) => updateWorkExperience(exp.id, 'description', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                      rows="3"
                    ></textarea>
                  </div>
                </div>
              </div>
            ))}
            
            <button 
              onClick={addWorkExperience}
              className="flex items-center justify-center bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 mb-6"
            >
              <span className="mr-2">Fill out</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </button>
            
            <div className="flex justify-between mt-4">
              <button 
                onClick={prevStep}
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-100"
              >
                Previous
              </button>
              <button 
                onClick={nextStep}
                className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
              >
                Next
              </button>
            </div>
          </div>
        );
      case 3:
        return (
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Education</h2>
            <p className="text-gray-600 mb-4">Have you completed an education? Tell what and where you have studied.</p>
            
            {formData.education.map((edu) => (
              <div key={edu.id} className="mb-6 p-4 border border-gray-200 rounded-md">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-medium">Education Entry</h3>
                  <button 
                    onClick={() => removeEducation(edu.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Institution</label>
                    <input
                      type="text"
                      value={edu.institution}
                      onChange={(e) => updateEducation(edu.id, 'institution', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Degree</label>
                    <input
                      type="text"
                      value={edu.degree}
                      onChange={(e) => updateEducation(edu.id, 'degree', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Field of Study</label>
                    <input
                      type="text"
                      value={edu.field}
                      onChange={(e) => updateEducation(edu.id, 'field', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                      <input
                        type="date"
                        value={edu.startDate}
                        onChange={(e) => updateEducation(edu.id, 'startDate', e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                      <input
                        type="date"
                        value={edu.endDate}
                        onChange={(e) => updateEducation(edu.id, 'endDate', e.target.value)}
                        className="w-full p-2 border border-gray-300 rounded-md"
                      />
                    </div>
                  </div>
                </div>
              </div>
            ))}
            
            <button 
              onClick={addEducation}
              className="flex items-center justify-center bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 mb-6"
            >
              <span className="mr-2">Add education</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </button>
            
            <div className="flex justify-between mt-4">
              <button 
                onClick={prevStep}
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-100"
              >
                Previous
              </button>
              <button 
                onClick={nextStep}
                className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
              >
                Next
              </button>
            </div>
          </div>
        );
      case 4:
        return (
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Language</h2>
            <p className="text-gray-600 mb-4">Hello,Hello,good day. Add which languages you know well, or just a little.</p>
            
            {formData.languages.map((lang) => (
              <div key={lang.id} className="mb-6 p-4 border border-gray-200 rounded-md">
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-medium">Language</h3>
                  <button 
                    onClick={() => removeLanguage(lang.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Remove
                  </button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Language Name</label>
                    <input
                      type="text"
                      value={lang.name}
                      onChange={(e) => updateLanguage(lang.id, 'name', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Proficiency</label>
                    <select
                      value={lang.proficiency}
                      onChange={(e) => updateLanguage(lang.id, 'proficiency', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-md"
                    >
                      <option value="Beginner">Beginner</option>
                      <option value="Intermediate">Intermediate</option>
                      <option value="Advanced">Advanced</option>
                      <option value="Fluent">Fluent</option>
                      <option value="Native">Native</option>
                    </select>
                  </div>
                </div>
              </div>
            ))}
            
            <button 
              onClick={addLanguage}
              className="flex items-center justify-center bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 mb-6"
            >
              <span className="mr-2">Add language</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </button>
            
            <div className="flex justify-between mt-4">
              <button 
                onClick={prevStep}
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-100"
              >
                Previous
              </button>
              <button 
                onClick={nextStep}
                className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
              >
                Next
              </button>
            </div>
          </div>
        );
      case 5:
        return (
          <div className="p-6 bg-white rounded-lg shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Summary</h2>
            <p className="text-gray-600 mb-4">Hello,Hello,good day. Add which languages you know well, or just a little.</p>
            
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-1">Professional Summary</label>
              <textarea
                value={formData.summary}
                onChange={(e) => updateSummary(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md"
                rows="5"
                placeholder="Write a brief professional summary highlighting your skills and experience..."
              ></textarea>
            </div>
            
            <button 
              onClick={addLanguage}
              className="flex items-center justify-center bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600 mb-6"
            >
              <span className="mr-2">Add summary</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
              </svg>
            </button>
            
            <div className="flex justify-between mt-4">
              <button 
                onClick={prevStep}
                className="border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-100"
              >
                Previous
              </button>
              <button 
                onClick={createCV}
                className="bg-teal-500 text-white px-4 py-2 rounded-md hover:bg-teal-600"
              >
                Create CV
              </button>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="w-full p-4 text-gray-800">
      <h1 className="text-3xl font-bold mb-8">CV Builder</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="md:col-span-1 bg-white p-4 rounded-lg shadow-sm">
          <ul className="space-y-2">
            <li className={`p-2 rounded ${currentStep === 1 ? 'bg-teal-100 text-teal-700' : ''}`}>
              <button 
                onClick={() => setCurrentStep(1)}
                className="w-full text-left flex items-center"
              >
                <span className={`mr-2 font-semibold ${currentStep === 1 ? 'text-teal-700' : 'text-gray-700'}`}>1.</span>
                <span className={currentStep === 1 ? 'text-teal-700' : 'text-gray-700'}>Contact Info</span>
              </button>
            </li>
            <li className={`p-2 rounded ${currentStep === 2 ? 'bg-teal-100 text-teal-700' : ''}`}>
              <button 
                onClick={() => setCurrentStep(2)}
                className="w-full text-left flex items-center"
              >
                <span className={`mr-2 font-semibold ${currentStep === 2 ? 'text-teal-700' : 'text-gray-700'}`}>2.</span>
                <span className={currentStep === 2 ? 'text-teal-700' : 'text-gray-700'}>Work Experience</span>
              </button>
            </li>
            <li className={`p-2 rounded ${currentStep === 3 ? 'bg-teal-100 text-teal-700' : ''}`}>
              <button 
                onClick={() => setCurrentStep(3)}
                className="w-full text-left flex items-center"
              >
                <span className={`mr-2 font-semibold ${currentStep === 3 ? 'text-teal-700' : 'text-gray-700'}`}>3.</span>
                <span className={currentStep === 3 ? 'text-teal-700' : 'text-gray-700'}>Education</span>
              </button>
            </li>
            <li className={`p-2 rounded ${currentStep === 4 ? 'bg-teal-100 text-teal-700' : ''}`}>
              <button 
                onClick={() => setCurrentStep(4)}
                className="w-full text-left flex items-center"
              >
                <span className={`mr-2 font-semibold ${currentStep === 4 ? 'text-teal-700' : 'text-gray-700'}`}>4.</span>
                <span className={currentStep === 4 ? 'text-teal-700' : 'text-gray-700'}>Language</span>
              </button>
            </li>
            <li className={`p-2 rounded ${currentStep === 5 ? 'bg-teal-100 text-teal-700' : ''}`}>
              <button 
                onClick={() => setCurrentStep(5)}
                className="w-full text-left flex items-center"
              >
                <span className={`mr-2 font-semibold ${currentStep === 5 ? 'text-teal-700' : 'text-gray-700'}`}>5.</span>
                <span className={currentStep === 5 ? 'text-teal-700' : 'text-gray-700'}>Summary</span>
              </button>
            </li>
          </ul>
        </div>
        
        <div className="md:col-span-3">
          {renderStep()}
        </div>
      </div>
    </div>
  );
};

export default CVBuilder;