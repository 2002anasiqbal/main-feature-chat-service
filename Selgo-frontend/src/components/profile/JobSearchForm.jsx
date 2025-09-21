"use client";
import React, { useState } from 'react';

const JobSearchForm = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    workSituation: '',
    position: '',
    company: '',
    preferredLocation: '',
    skills: ''
  });

  const handleInputChange = (field, value) => {
    setFormData({
      ...formData,
      [field]: value
    });
  };

  const handleNext = () => {
    setCurrentStep(currentStep + 1);
  };

  const handleBack = () => {
    setCurrentStep(currentStep - 1);
  };

  const showRecommendedJobs = () => {
    // In a real application, this would navigate to job recommendations
    alert('Showing recommended jobs based on your profile!');
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white rounded-lg shadow-md p-6 w-full max-w-md">
        {currentStep === 1 && (
          <>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">What is your current work situation?</h1>
            <p className="text-gray-800 mb-6">
              If you do several of these at the same time, choose
              the one that you think best describes you.
            </p>
            
            <div className="space-y-4">
              <label className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="workSituation"
                  value="at work"
                  checked={formData.workSituation === "at work"}
                  onChange={() => handleInputChange("workSituation", "at work")}
                  className="h-5 w-5 text-teal-500"
                />
                <span className="text-gray-800">I am at work</span>
              </label>
              
              <label className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="workSituation"
                  value="student"
                  checked={formData.workSituation === "student"}
                  onChange={() => handleInputChange("workSituation", "student")}
                  className="h-5 w-5 text-teal-500"
                />
                <span className="text-gray-800">I am a student</span>
              </label>
              
              <label className="flex items-center space-x-3">
                <input
                  type="radio"
                  name="workSituation"
                  value="unemployed"
                  checked={formData.workSituation === "unemployed"}
                  onChange={() => handleInputChange("workSituation", "unemployed")}
                  className="h-5 w-5 text-teal-500"
                />
                <span className="text-gray-800">I am unemployed</span>
              </label>
            </div>
          </>
        )}

        {currentStep === 2 && (
          <>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">What is your current position?</h1>
            <p className="text-gray-800 mb-6">
              If you do several of these at the same time, choose
              the one that you think best describes you.
            </p>
            
            <div className="space-y-4">
              <div>
                <label className="block mb-1 text-gray-800">I work as</label>
                <input
                  type="text"
                  value={formData.position}
                  onChange={(e) => handleInputChange("position", e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded text-gray-800"
                  placeholder="Your position"
                />
              </div>
              
              <div>
                <label className="block mb-1 text-gray-800">At</label>
                <input
                  type="text"
                  value={formData.company}
                  onChange={(e) => handleInputChange("company", e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded text-gray-800"
                  placeholder="Company name"
                />
              </div>
            </div>
          </>
        )}

        {currentStep === 3 && (
          <>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Where would you most like to work?</h1>
            <p className="text-gray-800 mb-6">
              If you do several of these at the same time, choose
              the one that you think best describes you.
            </p>
            
            <div>
              <label className="block mb-1 text-gray-800">Search in counties and municipalities?</label>
              <input
                type="text"
                value={formData.preferredLocation}
                onChange={(e) => handleInputChange("preferredLocation", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded text-gray-800"
                placeholder="Location"
              />
            </div>
          </>
        )}

        {currentStep === 4 && (
          <>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Where would you most like to work?</h1>
            <p className="text-gray-800 mb-6">
              If you do several of these at the same time, choose
              the one that you think best describes you.
            </p>
            
            <div>
              <label className="block mb-1 text-gray-800">Search Skills (Optional)</label>
              <input
                type="text"
                value={formData.skills}
                onChange={(e) => handleInputChange("skills", e.target.value)}
                className="w-full p-2 border border-gray-300 rounded text-gray-800"
                placeholder="Your skills"
              />
            </div>
          </>
        )}

        {currentStep === 5 && (
          <>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">The information is saved to your Job profile on FINN.</h1>
            <p className="text-gray-800 mb-6">
              If you do several of these at the same time, choose
              the one that you think best describes you.
            </p>
          </>
        )}

        <div className="flex justify-between mt-8">
          {currentStep > 1 && (
            <button
              onClick={handleBack}
              className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 text-gray-800"
            >
              Back
            </button>
          )}
          
          {currentStep < 5 ? (
            <button
              onClick={handleNext}
              className="px-4 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 ml-auto"
            >
              Next
            </button>
          ) : (
            <button
              onClick={showRecommendedJobs}
              className="px-4 py-2 bg-teal-500 text-white rounded hover:bg-teal-600 ml-auto"
            >
              Show recommended jobs
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default JobSearchForm;